import os
import json
import logging
import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from .models import TrendingTopic
from dotenv import load_dotenv

load_dotenv()

proxy = os.getenv("PROXY_URL")
proxy_user = os.getenv("PROXY_USERNAME")
proxy_pass = os.getenv("PROXY_PASSWORD")
username = os.getenv("TWITTER_USERNAME")
password = os.getenv("TWITTER_PASSWORD")


def scrape_twitter_trending():
    options = {
        "proxy": {
            "http": f"http://{proxy_user}:{proxy_pass}@{proxy}",
            "https": f"https://{proxy_user}:{proxy_pass}@{proxy}",
            "no_proxy": "localhost,127.0.0.1",  # Excludes these from proxying
        }
    }

    driver = webdriver.Chrome(seleniumwire_options=options)
    try:
        # Navigate to Twitter
        driver.get("https://x.com/login")

        # Login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        ).send_keys(username, Keys.RETURN)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(password, Keys.RETURN)

        # Navigate to Explore/Trending
        driver.get("https://x.com/explore/tabs/trending")

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "span.r-18u37iz span.css-1jxf684")
                )
            )

            time.sleep(10)  # Sleep for 2 seconds to ensure the content is fully loaded

            page_source = driver.page_source

        except TimeoutException:
            logging.error("TimeoutException: Element not found")

        if page_source:
            # Scrape top 5 trending topics
            topics = []
            soup = BeautifulSoup(page_source, "html.parser")
            elements = soup.select("span.r-18u37iz span.css-1jxf684")

            for element in elements[:5]:
                topics.append({"name": element.text})

        driver.get("https://api.ipify.org?format=json")
        wait = WebDriverWait(driver, 10)
        pre_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
        ip_data = json.loads(pre_element.text)
        ip_address = ip_data.get("ip", "N/A")

        # Save to MongoDB
        record = TrendingTopic.save_topics(topics, ip_address)

        return record
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    finally:
        driver.quit()
