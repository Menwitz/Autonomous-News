# Setup Guide

## Prerequisites

1. **AWS Account**: Ensure you have an AWS account with necessary permissions to create and manage resources.
2. **AWS CLI**: Install and configure the AWS CLI with your credentials.
3. **Node.js and npm**: Install Node.js and npm for the web-based editor.
4. **Python 3.x**: Ensure Python 3.x is installed on your machine.
5. **OpenAI API Key**: Sign up for OpenAI and obtain an API key.
6. **WordPress Site**: Have a WordPress site set up with REST API access.

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/news-autonomous-platform.git
cd news-autonomous-platform
```

## 2. Set Up AWS Infrastructure

### Using CloudFormation

1. **Deploy CloudFormation Stacks**

   Navigate to the `infrastructure/cloudformation` directory and run the deploy script.

   ```bash
   cd infrastructure/cloudformation
   ./deploy.sh
   ```

   Ensure the CloudFormation templates (`dynamodb.yaml`, `s3.yaml`, `lambda.yaml`, `ses.yaml`, `cloudwatch.yaml`, `sns.yaml`) are correctly configured.

### Using Terraform

1. **Initialize Terraform**

   Navigate to the `infrastructure/terraform` directory and initialize Terraform.

   ```bash
   cd infrastructure/terraform
   terraform init
   ```

2. **Apply Terraform Configuration**

   Apply the configuration to create the necessary resources.

   ```bash
   terraform apply
   ```

## 3. Deploy Lambda Functions

Navigate to each Lambda function directory and deploy the functions.

1. **Scrape News Lambda**

   ```bash
   cd lambdas/scrape_news
   pip install -r requirements.txt -t .
   zip -r scrape_news.zip .
   aws lambda create-function --function-name scrape_news --zip-file fileb://scrape_news.zip --handler scrape_news.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role
   ```

2. **Generate Article Lambda**

   ```bash
   cd lambdas/generate_article
   pip install -r requirements.txt -t .
   zip -r generate_article.zip .
   aws lambda create-function --function-name generate_article --zip-file fileb://generate_article.zip --handler generate_article.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role
   ```

3. **Paraphrase Article Lambda**

   ```bash
   cd lambdas/paraphrase_article
   pip install -r requirements.txt -t .
   zip -r paraphrase_article.zip .
   aws lambda create-function --function-name paraphrase_article --zip-file fileb://paraphrase_article.zip --handler paraphrase_article.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role
   ```

4. **Publish Article Lambda**

   ```bash
   cd lambdas/publish_article
   pip install -r requirements.txt -t .
   zip -r publish_article.zip .
   aws lambda create-function --function-name publish_article --zip-file fileb://publish_article.zip --handler publish_article.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role
   ```

5. **Post to Social Media Lambda**

   ```bash
   cd lambdas/post_to_social_media
   pip install -r requirements.txt -t .
   zip -r post_to_social_media.zip .
   aws lambda create-function --function-name post_to_social_media --zip-file fileb://post_to_social_media.zip --handler post_to_social_media.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role
   ```

6. **Optimize SEO Lambda**

   ```bash
   cd lambdas/optimize_seo
   pip install -r requirements.txt -t .
   zip -r optimize_seo.zip .
   aws lambda create-function --function-name optimize_seo --zip-file fileb://optimize_seo.zip --handler optimize_seo.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role
   ```

## 4. Configure SES for Email Notifications

1. **Verify Email Addresses**

   Verify the sender and recipient email addresses in Amazon SES.

   ```bash
   aws ses verify-email-identity --email-address your-email@example.com
   aws ses verify-email-identity --email-address editor@example.com
   ```

2. **Create and Configure an SNS Topic**

   Create an SNS topic for email notifications.

   ```bash
   aws sns create-topic --name NewArticleNotification
   ```

   Subscribe the editor's email to the SNS topic.

   ```bash
   aws sns subscribe --topic-arn arn:aws:sns:your-region:your-account-id:NewArticleNotification --protocol email --notification-endpoint editor@example.com
   ```

## 5. Set Up the Web-Based Editor

1. **Navigate to the Web Editor Directory**

   ```bash
   cd web-editor
   ```

2. **Install Dependencies**

   ```bash
   npm install
   ```

3. **Configure AWS Amplify**

   Create an `aws-exports.js` file with your AWS configuration or use the Amplify CLI to set up the project.

   ```bash
   amplify init
   amplify add auth
   amplify push
   ```

4. **Start the Development Server**

   ```bash
   npm start
   ```

## 6. Configure OpenAI API

1. **Set Up OpenAI API Key**

   Ensure your Lambda functions that interact with the OpenAI API (generate_article.py, paraphrase_article.py) have access to the API key. You can store the API key in AWS Secrets Manager and fetch it within your Lambda functions.

   ```python
   import os
   import boto3
   from botocore.exceptions import ClientError

   def get_openai_api_key():
       secret_name = "openai/api_key"
       region_name = "your-region"

       # Create a Secrets Manager client
       session = boto3.session.Session()
       client = session.client(service_name='secretsmanager', region_name=region_name)

       try:
           get_secret_value_response = client.get_secret_value(SecretId=secret_name)
           secret = get_secret_value_response['SecretString']
           return secret
       except ClientError as e:
           raise e
   ```

## 7. Configure WordPress Integration

1. **Generate Application Password**

   In your WordPress site, generate an application password for the user that will post articles.

2. **Update Lambda Function**

   Update the `publish_article.py` Lambda function to include the WordPress site URL, username, and application password.

   ```python
   wordpress_url = 'https://your-wordpress-site.com/wp-json/wp/v2/posts'
   wordpress_user = 'your-wordpress-username'
   wordpress_password = 'your-wordpress-application-password'
   ```

## 8. Test the End-to-End Workflow

1. **Trigger the Workflow**

   Manually trigger the Lambda functions or set up CloudWatch Events to schedule the triggers for scraping, generating, paraphrasing, notifying editors, SEO optimization, and publishing.

2. **Verify Output**

   - Check DynamoDB for stored headlines and articles.
   - Check S3 for paraphrased and edited articles.
   - Verify email notifications sent via SES.
   - Review and edit articles using the web-based editor.
   - Verify published articles on the WordPress site.
   - Check social media posts.
