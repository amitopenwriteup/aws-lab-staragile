import boto3
import botocore
import os
import logging
# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Initialize S3 resource
s3 = boto3.resource('s3')
def lambda_handler(event, context):
    logger.info("New files uploaded to the source bucket.")
    # Retrieve the key and bucket name from the event
    try:
        key = event['Records'][0]['s3']['object']['key']
        source_bucket = event['Records'][0]['s3']['bucket']['name']
    except KeyError as e:
        logger.error("Missing key information in event: %s", e)
        return
    # Get the destination bucket from environment variables
    destination_bucket = os.getenv('destination_bucket')
    if not destination_bucket:
        logger.error("Destination bucket environment variable  is not set.")
        return
    # Define the source object
    source = {'Bucket': source_bucket, 'Key': key}
    try:
        # Copy the file
        s3.meta.client.copy(source, destination_bucket, key)
        logger.info("File '%s' copied from '%s' to '%s' successfully!", key, source_bucket, destination_bucket)
    except botocore.exceptions.ClientError as error:
        logger.error("Error copying file: %s", error)
    except botocore.exceptions.ParamValidationError as error:
        logger.error("Parameter validation error: %s", error)
