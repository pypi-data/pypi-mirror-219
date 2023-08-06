# lambda_handler.py
import os
import json
from .lambda_executor import LambdaExecutor
from .s3_operations import S3Operations
from .dynamo_operations import DynamoOperations


input_bucket = os.environ['INPUT_BUCKET']
output_bucket = os.environ['OUTPUT_BUCKET']
table_name = os.environ['TABLE_NAME']

executor = LambdaExecutor(
    s3_operations=S3Operations(),
    dynamo_operations=DynamoOperations(),
    input_bucket=input_bucket,
    output_bucket=output_bucket,
    table_name=table_name,
    output_bucket_access_key=os.getenv('OUTPUT_BUCKET_ACCESS_KEY'),
    output_bucket_secret_access_key=os.getenv('OUTPUT_BUCKET_SECRET_ACCESS_KEY')
)

def handler(sns_event, context):
    print(f"table name: {os.environ['TABLE_NAME']}")
    print(f"input bucket: {os.environ['INPUT_BUCKET']}")
    print(f"output bucket: {os.environ['OUTPUT_BUCKET']}")
    if 'OUTPUT_BUCKET_ACCESS_KEY' in os.environ:
        print(os.environ['OUTPUT_BUCKET_ACCESS_KEY'])
    if 'OUTPUT_BUCKET_SECRET_ACCESS_KEY' in os.environ:
        print(os.environ['OUTPUT_BUCKET_SECRET_ACCESS_KEY'])
    #
    print("Event : " + str(sns_event))
    print("Context : " + str(context))
    for record in sns_event['Records']:
        message = json.loads(record['Sns']['Message'])
        print("Start Message : " + str(message))
        executor.execute(message)
        print("Done Message : " + str(message))
    print("Done Event : " + str(sns_event))
