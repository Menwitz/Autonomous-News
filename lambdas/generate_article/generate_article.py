import json
import boto3
import os
import openai
from datetime import datetime
from botocore.exceptions import ClientError
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables
load_dotenv()

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
headlines_table = dynamodb.Table('NewsHeadlines')
articles_table = dynamodb.Table('GeneratedArticles')

# Retrieve OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event: dict, context: dict) -> dict:
    """
    AWS Lambda handler function.
    
    Args:
        event (dict): Event data
        context (dict): Context data
    
    Returns:
        dict: HTTP response with status code and message
    """
    try:
        headlines = retrieve_headlines()
        for headline in headlines:
            headline_text = headline['headline']
            article = generate_article(headline_text)
            store_article(articles_table, headline_text, article)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Articles generated and stored successfully')
        }
    except Exception as e:
        logger.error(f'Unhandled exception: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Unhandled exception: {str(e)}')
        }

def retrieve_headlines() -> List[Dict[str, str]]:
    """
    Retrieve headlines from the NewsHeadlines DynamoDB table.
    
    Returns:
        List[Dict[str, str]]: List of headlines
    
    Raises:
        RuntimeError: If there is an error retrieving headlines
    """
    try:
        response = headlines_table.scan()
        items = response.get('Items', [])
        
        # Handle pagination if needed
        while 'LastEvaluatedKey' in response:
            response = headlines_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))
        
        return items
    except ClientError as e:
        logger.error(f'Error retrieving headlines: {e.response["Error"]["Message"]}')
        raise RuntimeError(f'Error retrieving headlines: {e.response["Error"]["Message"]}')

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_article(headline: str) -> str:
    """
    Generate a detailed article using OpenAI API based on the headline.
    
    Args:
        headline (str): The headline to base the article on
    
    Returns:
        str: The generated article
    
    Raises:
        RuntimeError: If there is an error generating the article
    """
    try:
        instructions = {
            "model": "gpt-4-turbo",
            "instructions": {
                "headline": headline,
                "length": "1000 words",
                "mood": "informative",
                "style": "professional",
                "additional_requirements": "Include relevant data and quotes"
            }
        }

        prompt = (
            f"Using the following instructions, generate a detailed article:\n\n"
            f"Headline: {instructions['instructions']['headline']}\n"
            f"Length: {instructions['instructions']['length']}\n"
            f"Mood: {instructions['instructions']['mood']}\n"
            f"Style: {instructions['instructions']['style']}\n"
            f"Additional Requirements: {instructions['instructions']['additional_requirements']}\n"
            f"Article:"
        )

        response = openai.Completion.create(
            model="gpt-4-turbo",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7,
            n=1,
            stop=None
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f'Error generating article: {str(e)}')
        raise RuntimeError(f'Error generating article: {str(e)}')

def store_article(table: Any, headline: str, article: str) -> None:
    """
    Store the generated article in the GeneratedArticles DynamoDB table.
    
    Args:
        table (Any): The DynamoDB table object
        headline (str): The headline of the article
        article (str): The generated article
    
    Raises:
        RuntimeError: If there is an error storing the article
    """
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
        logger.error(f'Error storing article: {e.response["Error"]["Message"]}')
        raise RuntimeError(f'Error storing article: {e.response["Error"]["Message"]}')
