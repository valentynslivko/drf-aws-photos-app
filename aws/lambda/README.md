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
1. Function does not return ```
{"statusCode": 200, "body":"something"}
```
1. Function is not in `lambda_function.py` file
1. Tick `Lambda proxy integration Info - False` in API GW to fix malformed event input in lambda
