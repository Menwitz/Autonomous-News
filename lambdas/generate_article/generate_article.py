import json
import boto3
import os
import openai
from datetime import datetime
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Retrieve OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

def lambda_handler(event, context):
    # Retrieve headlines from NewsHeadlines table
    headlines_table = dynamodb.Table('NewsHeadlines')
    articles_table = dynamodb.Table('GeneratedArticles')
    
    try:
        response = headlines_table.scan()
        headlines = response.get('Items', [])
        
        for headline in headlines:
            headline_text = headline['headline']
            article = generate_article(headline_text)
            store_article(articles_table, headline_text, article)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Articles generated and stored successfully')
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error retrieving headlines: {e.response["Error"]["Message"]}')
        }

def generate_article(headline):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Write a detailed article based on the following headline: {headline}",
            max_tokens=500
        )
        article = response.choices[0].text.strip()
        return article
    except Exception as e:
        raise RuntimeError(f'Error generating article: {str(e)}')

def store_article(table, headline, article):
    try:
        timestamp = datetime.utcnow().isoformat()
        url = f"https://example.com/{headline.replace(' ', '-').lower()}"
        table.put_item(
            Item={
                'url': url,
                'headline': headline,
                'article': article,
                'timestamp': timestamp
            }
        )
    except ClientError as e:
        raise RuntimeError(f'Error storing article: {e.response["Error"]["Message"]}')
