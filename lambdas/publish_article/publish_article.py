import json
import boto3
import requests
from botocore.exceptions import ClientError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')

# Constants
S3_BUCKET_NAME = 'paraphrased-articles-bucket'
DYNAMODB_TABLE_NAME = 'GeneratedArticles'
WORDPRESS_API_URL = 'https://your-wordpress-site.com/wp-json/wp/v2/posts'
WORDPRESS_USERNAME = 'your-wordpress-username'
WORDPRESS_PASSWORD = 'your-wordpress-password'

def publish_article(event, context):
    # Extract article URI from the event
    try:
        article_uri = event['Records'][0]['s3']['object']['key']
        logger.info(f'Retrieved article URI: {article_uri}')
    except KeyError as e:
        logger.error(f'Error retrieving article URI: {e}')
        return

    # Retrieve article content from S3
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=article_uri)
        article_content = response['Body'].read().decode('utf-8')
        logger.info('Article content retrieved successfully')
    except ClientError as e:
        logger.error(f'Error retrieving article from S3: {e}')
        update_dynamodb_status(article_uri, 'FAILED')
        return

    # Prepare the WordPress post data
    post_data = {
        'title': 'Your Article Title',
        'content': article_content,
        'status': 'publish'
    }

    # Publish the article to WordPress
    try:
        response = requests.post(
            WORDPRESS_API_URL,
            json=post_data,
            auth=(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
        )
        response.raise_for_status()
        logger.info('Article published successfully')
        update_dynamodb_status(article_uri, 'PUBLISHED')
    except requests.exceptions.RequestException as e:
        logger.error(f'Error publishing article to WordPress: {e}')
        update_dynamodb_status(article_uri, 'FAILED')
        return

def update_dynamodb_status(article_uri, status):
    try:
        dynamodb_client.update_item(
            TableName=DYNAMODB_TABLE_NAME,
            Key={'ArticleURI': {'S': article_uri}},
            UpdateExpression='SET PublicationStatus = :status',
            ExpressionAttributeValues={':status': {'S': status}}
        )
        logger.info(f'Updated DynamoDB status to {status} for article URI: {article_uri}')
    except ClientError as e:
        logger.error(f'Error updating DynamoDB status: {e}')

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
