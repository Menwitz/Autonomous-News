import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper.py import fetch_headlines, batch_store_headlines, log_error
from config.py import news_websites

async def scrape_news_async():
    """
    Lambda handler function to scrape headlines from configured news websites.
    """
    headlines_data = []
    tasks = [fetch_headlines_async(url, selector) for url, selector in news_websites.items()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for url, result in zip(news_websites.keys(), results):
        if isinstance(result, Exception):
            log_error(f"Error processing {url}: {result}")
        else:
            for headline in result:
                headlines_data.append({'url': url, 'headline': headline, 'timestamp': datetime.utcnow().isoformat()})
    batch_store_headlines(headlines_data)

    return {
        'statusCode': 200,
        'body': json.dumps('Headlines scraped successfully')
    }

if __name__ == "__main__":
    asyncio.run(scrape_news_async())
