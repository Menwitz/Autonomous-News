import json
import boto3
import os
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Retrieve OpenAI API key from environment variables
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
#print(openai.api_key )#DEBUG 

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

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
                "length": "70 words",
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

        response = client.chat.completions.create(model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a professional article writer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7,
        n=1,
        stop=None)
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f'Error generating article: {str(e)}')
        raise RuntimeError(f'Error generating article: {str(e)}')
