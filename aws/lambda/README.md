## Building dependencies
```sh
mkdir python
pip install -r requirements.txt -t python
zip -r <some_layer>.zip python/
``` 
1. Upload zip to s3

1. Create layer from s3

1. Upload function itself

## Common issues:
1. If lambda function is used as proxy by API Gateway, you __HAVE__ to return ```
{
    "isBase64Encoded": False,
    "statusCode": 200,
    "headers": None,
    "body": json.dumps({"asd": 'qwe'}), // BODY MUST BE A STRING
}
``` as a response. If response is malformed, you'll get a 502 status code
1. Function is not in `lambda_function.py` file
1. Tick `Lambda proxy integration Info - False` in API GW to fix malformed event input in lambda
1. Incorrect/missing permissions for lambda execution roles, lambda permissions to put objects to s3, API GW permissions to invoke Lambdas
1. S3 bucket access policies
