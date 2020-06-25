## CBS zipcode table (postcodetabel)

Persist the CBS zipcode table to your AWS DynamoDB instance and query zipcodes using a REST API. 

### Background
[CBS] is the dutch statistics bureau that manages enormous amounts of open data about neighborhoods in the Netherlands. 
A conversion table (postcodetabel) is needed to map addresses to geographical data. This project retrieves the table 
from the CBS website and stores it in a DynamoDB table which can be queries through a REST API. 

Check it out at: https://hcdl1kprn8.execute-api.eu-west-1.amazonaws.com/prod/zipcode/1011WD

    {
      "gemeente": 363,
      "pc6": "1011WD",
      "wijk": 36304,
      "version": "20190801",
      "buurt": 3630407
    }

All data (c) Statistics Netherlands ([CBS]) 

### Getting started
Set up your AWS [credentials] and follow the serverless [getting started] guide.

- Create the package
> sls package

- Deploy to AWS
> sls deploy --stage prod

- Populate the database. Note that the table is quite large, so this may take some time.
> python populate.py --stage prod --region eu-west-1

- Query the database
> curl https://[your-api-id].execute-api.eu-west-1.amazonaws.com/prod/zipcode/[your-zipcode]


## Useful commands

Help
> python populate.py -h

Run functions (local and on AWS)
> sls invoke local -f getZipcode -p tests/zipcode.json

> sls invoke -f getZipcode -p tests/zipcode.json


Run tests
> python -m pytest -v

Delete all AWS resources 
> sls remove


[CBS]: https://www.cbs.nl/en-gb
[getting started]: https://www.serverless.com/framework/docs/getting-started/
[credentials]: https://www.serverless.com/framework/docs/providers/aws/guide/credentials/