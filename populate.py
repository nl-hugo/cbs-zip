import argparse
import logging
import re
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import boto3
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

names = ['pc6', 'nr', 'buurt', 'wijk', 'gemeente']
pattern = r'pc6hnr(\d{8})_(?:.)*.csv'


def load_dynamo_data(data, stage='dev', region='eu-west-1'):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(f'cbs-zip-{stage}')
    logging.info(f'Write {len(data)} items to {table.table_name}')
    with table.batch_writer() as batch:
        for item in data:
            logging.debug(f'Item: {item}')
            batch.put_item(
                Item=item
            )


def get_zip_file(url):
    resp = urlopen(url)
    return resp.read()


def data_from_zip(file):
    df = pd.read_csv(BytesIO(file), sep=';', skiprows=1, names=names)
    cols = names.copy()
    val = cols.pop(1)  # nr

    # count the number of addresses per zipcode and buurt, sorted
    df_agg = df.groupby(cols).count().sort_values(['pc6', val], ascending=[True, False])
    df_agg.reset_index(inplace=True)

    # retain the buurt with most addresses for each zipcode
    df_agg.drop_duplicates(subset=['pc6'], keep='first', inplace=True)
    df_agg.drop([val], axis=1, inplace=True)
    logging.info(f'{len(df_agg)} entries')
    logging.info(df_agg.head())

    return df_agg


def populate(zipfile, stage, region):
    logging.debug(f'Populating {stage} in {region} with contents from {zipfile}')
    file_bytes = BytesIO(get_zip_file(zipfile))
    contents = ZipFile(file_bytes)

    for name in contents.namelist():
        logging.debug(f'File {name}')
        m = re.search(pattern, name)
        if m is not None:
            logging.debug(f'Found file {name}')
            df = data_from_zip(contents.read(name))
            df['version'] = m.group(1)
            load_dynamo_data(df.to_dict('records'), stage, region)


def handler():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stage", help="name of the staging environment (default='dev')", default='dev')
    parser.add_argument("-r", "--region", help="region of the DynamoDB table (default='eu-west-1')",
                        default='eu-west-1')
    args = parser.parse_args()

    with open('urls.txt') as f:
        [populate(line, args.stage, args.region) for line in f]


if __name__ == '__main__':
    handler()
