import json
import boto3
import requests
import os

# Initialize AWS services
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
ses = boto3.client('ses')

# Environment variables
QUILLBOT_API_KEY = os.environ['QUILLBOT_API_KEY']
DYNAMODB_TABLE = 'GeneratedArticles'
S3_BUCKET = 'paraphrased-articles-bucket'
SES_SENDER_EMAIL = 'your-sender-email@example.com'
SES_RECIPIENT_EMAILS = ['editor1@example.com', 'editor2@example.com']

def paraphrase_article(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE)
    
    # Retrieve articles from DynamoDB
    response = table.scan(FilterExpression=Attr('paraphrased_status').eq(False))
    articles = response['Items']
    
    for article in articles:
        article_id = article['article_id']
        content = article['content']
        
        try:
            # Paraphrase article using Quillbot API
            paraphrased_content = paraphrase_with_quillbot(content)
            
            # Save paraphrased content to S3
            s3_key = f"{article_id}_paraphrased.txt"
            s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=paraphrased_content)
            
            # Update DynamoDB with paraphrased status and S3 file key
            table.update_item(
                Key={'article_id': article_id},
                UpdateExpression="set paraphrased_status = :s, s3_key = :k",
                ExpressionAttributeValues={
                    ':s': True,
                    ':k': s3_key
                }
            )
            
            # Send email notification via SES
            send_email_notification(article_id, s3_key)
        
        except Exception as e:
            print(f"Error processing article {article_id}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Paraphrasing process completed')
    }

def paraphrase_with_quillbot(text):
    url = "https://api.quillbot.com/api/paraphraser"
    headers = {
        'Authorization': f'Bearer {QUILLBOT_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'lang': 'en'
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    paraphrased_text = response.json()['data']['paraphrased_text']
    return paraphrased_text

def send_email_notification(article_id, s3_key):
    subject = "New Paraphrased Article Ready"
    body_text = f"Article ID: {article_id}\nS3 Key: {s3_key}"
    
    ses.send_email(
        Source=SES_SENDER_EMAIL,
        Destination={
            'ToAddresses': SES_RECIPIENT_EMAILS
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': body_text
                }
            }
        }
    )
