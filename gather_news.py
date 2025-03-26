import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import getpass
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "finance2"
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
stocklist = sys.argv[1:]  # skip script name

def scrape_yahoo_news_titles_and_links(ticker):
    """
    Scrape news titles and their links from Yahoo Finance's news section for a specific stock ticker.
    """
    # Headless Chrome setup for Render
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)

    try:
        url = f"https://finance.yahoo.com/quote/{ticker}/news/"
        driver.get(url)

        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'subtle-link')]"))
        )

        news_items = set()
        while len(news_items) < 50:
            link_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'subtle-link') and contains(@class, 'fin-size-small')]")
            for link_element in link_elements:
                title = link_element.get_attribute('aria-label')
                url = link_element.get_attribute('href')
                if title and url:
                    news_items.add((title, url))

            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(2)

            if len(news_items) >= 50 or not link_elements:
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

    return list(news_items)

def actual_scrapping_and_saving_links_titles(tick):
    try:
        news_titles = scrape_yahoo_news_titles_and_links(tick)
        print("Successfully scraped", tick)

        COLLECTION_NAME = "stock_news_" + tick
        collection = db[COLLECTION_NAME]

        for title, link in news_titles:
            try:
                collection.insert_one({"title": title, "link": link})
            except Exception as e:
                print(f"Error saving to MongoDB: {e}")

        print("News items have been stored")
    except Exception as e:
        print(f"An error occurred: {e}")

def bulk_scrapping_and_saving(stock_list):
    for ticker in stock_list:
        actual_scrapping_and_saving_links_titles(ticker)
        print("")
    return

bulk_scrapping_and_saving(stocklist)
