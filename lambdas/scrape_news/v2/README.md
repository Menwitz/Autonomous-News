# News Headlines Scraper

## Overview
This Lambda function scrapes headlines from a list of predefined news websites and stores them in an AWS DynamoDB table.

## Configuration
### Environment Variables
- `DYNAMODB_TABLE`: 
- `REQUEST_TIMEOUT`: 

### AWS Parameter Store
Store the above environment variables in AWS Systems Manager Parameter Store for secure access.

## Setup
1. Install the necessary Python packages:
    ```
    pip install -r requirements.txt
    ```

2. Configure your AWS credentials.

3. Run the scraper locally:
    ```
    python main.py
    ```

## Testing
Run the unit tests:
