import requests
import pymongo
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
NEWS_API_KEY = "46669fcd994d4ab5a2e0b855f556d8d2"  # Make sure to define this in .env
DATABASE_NAME = "finance2"

client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

stocklist = sys.argv[1:]  # skip script name

def fetch_newsapi_articles(ticker):
    """
    Fetch latest news articles for a ticker using NewsAPI.
    """
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])[:10]
            return [(article["title"], article["url"]) for article in articles if article.get("title") and article.get("url")]
        else:
            print(f"NewsAPI Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Exception while calling NewsAPI: {e}")
        return []

def actual_fetching_and_saving_news(ticker):
    try:
        news_items = fetch_newsapi_articles(ticker)
        print("Successfully fetched news for", ticker)

        COLLECTION_NAME = "stock_news_" + ticker
        collection = db[COLLECTION_NAME]

        for title, link in news_items:
            try:
                collection.insert_one({"title": title, "link": link})
            except Exception as e:
                print(f"Error saving to MongoDB: {e}")

        print("News items have been stored")
    except Exception as e:
        print(f"An error occurred for {ticker}: {e}")

def bulk_fetch_and_store_news(stock_list):
    for ticker in stock_list:
        actual_fetching_and_saving_news(ticker)
        print("")
    return

bulk_fetch_and_store_news(stocklist)
