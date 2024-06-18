import json
import boto3
import requests
import os
from botocore.exceptions import ClientError
from requests.auth import HTTPBasicAuth
import logging
import time

# Set up structured logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')

# Environment Variables
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
DYNAMODB_TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']
WORDPRESS_API_URL = os.environ['WORDPRESS_API_URL']
WORDPRESS_USERNAME = os.environ['WORDPRESS_USERNAME']
WORDPRESS_PASSWORD = os.environ['WORDPRESS_PASSWORD']

def publish_article(event, context):
    article_uri = extract_article_uri(event)
    if not article_uri:
        return

    article_content = get_article_content_from_s3(article_uri)
    if not article_content:
        update_dynamodb_status(article_uri, 'FAILED')
        return

    if publish_to_wordpress(article_content):
        update_dynamodb_status(article_uri, 'PUBLISHED')
    else:
        update_dynamodb_status(article_uri, 'FAILED')

def extract_article_uri(event):
    try:
        article_uri = event['Records'][0]['s3']['object']['key']
        logger.info({'action': 'extract_article_uri', 'status': 'success', 'article_uri': article_uri})
        return article_uri
    except KeyError as e:
        logger.error({'action': 'extract_article_uri', 'status': 'error', 'error': str(e)})
        return None

def get_article_content_from_s3(article_uri):
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=article_uri)
        article_content = response['Body'].read().decode('utf-8')
        logger.info({'action': 'get_article_content_from_s3', 'status': 'success', 'article_uri': article_uri})
        return article_content
    except ClientError as e:
        logger.error({'action': 'get_article_content_from_s3', 'status': 'error', 'error': str(e)})
        return None

def publish_to_wordpress(article_content):
    post_data = {
        'title': 'Your Article Title',
        'content': article_content,
        'status': 'publish'
    }
    retry_attempts = 3
    for attempt in range(retry_attempts):
        try:
            response = requests.post(
                WORDPRESS_API_URL,
                json=post_data,
                auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
            )
            response.raise_for_status()
            logger.info({'action': 'publish_to_wordpress', 'status': 'success'})
            return True
        except requests.exceptions.RequestException as e:
            logger.error({'action': 'publish_to_wordpress', 'status': 'error', 'attempt': attempt + 1, 'error': str(e)})
            time.sleep(2 ** attempt)  # Exponential backoff
    return False

def update_dynamodb_status(article_uri, status):
    try:
        dynamodb_client.update_item(
            TableName=DYNAMODB_TABLE_NAME,
            Key={'ArticleURI': {'S': article_uri}},
            UpdateExpression='SET PublicationStatus = :status',
            ExpressionAttributeValues={':status': {'S': status}}
        )
        logger.info({'action': 'update_dynamodb_status', 'status': 'success', 'article_uri': article_uri, 'publication_status': status})
    except ClientError as e:
        logger.error({'action': 'update_dynamodb_status', 'status': 'error', 'error': str(e)})

if __name__ == '__main__':
    # Sample event for local testing
    event = {
        'Records': [
            {
                's3': {
                    'object': {
                        'key': 'path/to/your/article.txt'
                    }
                }
            }
        ]
    }
    context = {}
    publish_article(event, context)
