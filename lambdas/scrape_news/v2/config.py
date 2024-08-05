import os
import boto3
import logging

# Configuration
table_name = os.getenv('DYNAMODB_TABLE', 'NewsHeadlines')
timeout = int(os.getenv('REQUEST_TIMEOUT', 10))

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')  #TODO : add region_name to config
table = dynamodb.Table(table_name)

# Logger setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS SSM Parameter Store client
ssm = boto3.client('ssm', region_name='us-west-2')  #TODO : add region_name to config

def get_parameter(name):
    try:
        response = ssm.get_parameter(Name=name, WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        logger.error(f"Error getting parameter {name}: {e}")
        return None

# Fetching parameters
table_name = get_parameter('DYNAMODB_TABLE')
# Retrieve timeout parameter and ensure it's valid 
timeout_str = get_parameter('REQUEST_TIMEOUT')
if timeout_str is None:
    logger.warning("REQUEST_TIMEOUT not found. Using default timeout value.")
    timeout = 30  # Default value
else:
    try:
        timeout = int(timeout_str)
    except ValueError:
        logger.error(f"Invalid value for REQUEST_TIMEOUT: {timeout_str}. Using default timeout value.")
        timeout = 30  # Default value

news_websites = {
    "https://www.sbnation.com/": 'h2.c-entry-box--compact__title a',  
    "https://www.goal.com": 'a[data-testid="card-title-url"]',        
    "https://www.bleacherreport.com/": 'a[href^="https://bleacherreport.com/articles/"]', 
    "https://www.espn.com/": 'a[href*="/story/"]', 
    # "https://www.sports.yahoo.com/": 'h3 a',  TODO
    # "https://www.reuters.com/sports/": 'h3.story-title a', TODO : rectify => HTTP error fetching https://www.reuters.com/sports/: 401
    "https://www.foxsports.com/": 'a[href*="/stories/"]', 
    "https://www.skysports.com/": 'h3.sdc-site-tile__headline a.sdc-site-tile__headline-link',  
    "https://www.yardbarker.com/": 'div.grid-x.rfi-body div.cell h2 a', 
    "https://www.nbcsports.com/": '.SideBarArticleStack-items-item .PagePromo .PagePromo-media a'
}
