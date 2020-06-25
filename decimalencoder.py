import decimal
import json


class NumberStr(int):
    def __init__(self, o):
        self.o = o

    def __repr__(self):
        return str(self.o)


# This is a workaround for: http://bugs.python.org/issue16535
# https://github.com/serverless/examples/blob/master/aws-python-rest-api-with-dynamodb/todos/decimalencoder.py
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return NumberStr(obj)
        return super(DecimalEncoder, self).default(obj)
