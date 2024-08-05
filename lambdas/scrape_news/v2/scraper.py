import requests
from bs4 import BeautifulSoup
from datetime import datetime
from config import table, timeout, logger

# Request session with retry logic
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0'}
# Set headers with a user-agent to mimic a web browser
#headers = {
#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#}
#response = requests.get(url, headers=headers)


from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

def log_error(message):
    """Logs errors to AWS CloudWatch"""
    logger.error(message)

def is_valid_url(url):
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

def fetch_headlines(url, selector):
    """
    Fetches headlines from a given URL using the specified CSS selector.
    """
    if not is_valid_url(url):
        log_error(f"Invalid URL: {url}")
        return []
    try:
        response = session.get(url, timeout=timeout, verify=True if "nbc" in url else True, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup)
        headlines = soup.select(selector)
        # Extract headline and URL with conditional text fallback
        result = [
            {
                'headline': headline.get_text(strip=True) if headline.get_text(strip=True) else headline.get('aria-label', '').strip(),
                'url': headline.get('href', '')
            } 
        for headline in headlines
        ]
        return result
    

    except requests.Timeout:
        log_error(f"Timeout error fetching {url}")
    except requests.ConnectionError:
        log_error(f"Connection error fetching {url}")
    except requests.HTTPError as e:
        log_error(f"HTTP error fetching {url}: {e.response.status_code}")
    except Exception as e:
        log_error(f"Unexpected error fetching {url}: {e}")
    return []

def store_headline(url, headline):
    """
    Stores a single headline in DynamoDB.
    """
    try:
        table.put_item(
            Item={
                'url': url,
                'headline': headline,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        log_error(f"Credentials error: {e}")
    except Exception as e:
        log_error(f"Error storing headline: {e}")

def batch_store_headlines(headlines):
    """
    Stores multiple headlines in DynamoDB using batch operations.
    """
    try:
        with table.batch_writer() as batch:
            for item in headlines:
                batch.put_item(Item=item)
    except Exception as e:
        log_error(f"Error batch storing headlines: {e}")
