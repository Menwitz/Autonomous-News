import json
import boto3
import botocore
from botocore.exceptions import ClientError
import logging
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Initialize S3 and DynamoDB clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GeneratedArticles')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.isalnum() and word.lower() not in stop_words]
    word_freq = Counter(filtered_words)
    return word_freq.most_common(10)

def generate_seo_metadata(content):
    keywords = extract_keywords(content)
    seo_metadata = {
        'title': content.split('.')[0],
        'description': content[:150] + '...',
        'keywords': [keyword[0] for keyword in keywords]
    }
    return seo_metadata

def lambda_handler(event, context):
    bucket_name = 'paraphrased-articles-bucket'
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            logger.info('No files found in the bucket.')
            return {'statusCode': 200, 'body': json.dumps('No files found in the bucket.')}

        for obj in response['Contents']:
            file_key = obj['Key']
            file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            content = file_obj['Body'].read().decode('utf-8')
            
            seo_metadata = generate_seo_metadata(content)
            
            table.put_item(Item={
                'ArticleID': file_key,
                'Title': seo_metadata['title'],
                'Description': seo_metadata['description'],
                'Keywords': seo_metadata['keywords']
            })
            logger.info(f'Successfully processed and stored metadata for {file_key}')
        
        return {'statusCode': 200, 'body': json.dumps('SEO metadata generated and stored successfully.')}

    except ClientError as e:
        logger.error(f'Error fetching objects from S3: {e}')
        return {'statusCode': 500, 'body': json.dumps(f'Error fetching objects from S3: {e}')}

    except Exception as e:
        logger.error(f'General error: {e}')
        return {'statusCode': 500, 'body': json.dumps(f'Error: {e}')}
