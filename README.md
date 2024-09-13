# Content
`image_proj` - drf app
`lambda` - aws lambda source + instructions
`cloudformation` - aws cloudformation template + instructions

## Task definition
Цель

Познакомиться ближе с cloud вычеслениями, в частности AWS. Использую
serverless подход и AWS Lamda c API Gateway сделать пайплайн для обработки
изображений. Настроить DRF для создание RESTful api

Создать Django application для хранение юзеров и их profile photo:
1. Сделать все необходимые модели и миграции для приложения.
2. С помощь DRF настроить REST CRUD api для приложения.
3. Задеплоить приложение на EC2.
4. Настроить S3 bucket для хранения фото и статических файлов приложения
5. Настроить Lambda для обработки и обрезки загружаемы фото пользователей в
единый стандарт и загрузки фото на S3 хранилище

## Solution:
1. DRF app has a one-to-one relationship between user and profile, profile is created when new user is added in the DB.
1. DRF app has a viewset to patch a profile and provide an image link for processing.
1. Once image is submitted, POST request is sent to the deployed API GW instance, which requests Lambda function, which cuts the image. Image is being sent to API GW in base64 format and is unpacked by lambda function.
1. The result of the flow is either a 200 response with the link to the processed image on s3, or 400 error if image was incorrectly submitted, 500 error on the Pillow related errors

## Usage
1. Comment out `ChiApiGatewayAccount` part of the cloudformation template, create template with `aws cloudformation`, example: `aws cloudformation create-stack --stack-name chi-test-task-stack --template-body file:///<your_path>/drf-aws-photos-app/aws/cloudformation/template.yaml --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND`
1. Upload lambda function and lambda layers to s3. Example: `aws s3 cp test-task-chi-layer.zip s3://<your-bucket-name>`

1. Comment in `ChiApiGatewayAccount` resource and update the stack with `aws cloudformation create-stack --stack-name chi-test-task-stack --template-body file:///<your_path>/drf-aws-photos-app/aws/cloudformation/template.yaml --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND`
1. Go to the API Gateway -> resources -> all the way to the created endpoint (`/images` in this case) -> `Integration request` -> `Edit` -> Set `Lambda proxy integration` to false (uncheck) -> `Deploy API`. If you won't deploy the API you'll get 502 status codes

If you change any names in your infrastructure, you obviously gotta change the cloudformation template.

EC2 deployment is not covered as it's pretty basic anyway