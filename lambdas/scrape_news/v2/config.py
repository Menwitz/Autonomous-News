import os
import boto3
import logging

# Configuration
table_name = os.getenv('DYNAMODB_TABLE', 'NewsHeadlines')
timeout = int(os.getenv('REQUEST_TIMEOUT', 10))

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

# Logger setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS SSM Parameter Store client
ssm = boto3.client('ssm')

def get_parameter(name):
    try:
        response = ssm.get_parameter(Name=name, WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        logger.error(f"Error getting parameter {name}: {e}")
        return None

# Fetching parameters
table_name = get_parameter('DYNAMODB_TABLE')
timeout = int(get_parameter('REQUEST_TIMEOUT', 10))

news_websites = {
    "https://www.sbnation.com/": 'h2.c-entry-box--compact__title',
    "https://goal.com": 'h3.article-title',
    "https://bleacherreport.com/": 'h3.atom-headline',
    "https://www.espn.com/": 'h1.headline',
    "https://sports.yahoo.com/": 'h3',
    "https://www.reuters.com/sports/": 'h3.story-title',
    "https://www.foxsports.com/": 'h1.headline',
    "https://www.skysports.com/": 'h1.news-list__headline',
    "https://www.yardbarker.com/": 'h3',
    "https://www.nbcsports.com/": 'h2.tease-card__headline'
}
