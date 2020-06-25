## CBS zipcode table

Persist the CBS zipcode table to your AWS DynamoDB instance and query zipcodes using a REST Api. 


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



[getting started]: https://www.serverless.com/framework/docs/getting-started/
[credentials]: https://www.serverless.com/framework/docs/providers/aws/guide/credentials/