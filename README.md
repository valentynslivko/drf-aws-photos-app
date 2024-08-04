# Content
`image_proj` - drf app
`lambda` - aws lambda source + instructions
`cloudformation` - aws cloudformation template + instructions

## Usage
1. Create s3 bucket -> specify bucket name in the cloudformation template
1. Build Lambda layer -> upload layer to S3 bucket created in the previous step
1. Zip lambda & upload to the bucket
1. Apply cloudformation template

NOTE: ec2 deployment is not covered as it's pretty basic anyway