import json
import os
from selenium import webdriver
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
    options = webdriver.ChromeOptions()
    options.add_argument(f"--proxy-server=http://{proxy}")
    options.add_argument(f"--proxy-auth={proxy_user}:{proxy_pass}")

    driver = webdriver.Chrome()
    try:
        # Navigate to Twitter
        # driver.get("https://x.com/login")

        # Login
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.NAME, "text"))
        # ).send_keys(username, Keys.RETURN)
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.NAME, "password"))
        # ).send_keys(password, Keys.RETURN)

        # Navigate to Explore/Trending
        # driver.get("https://x.com/explore/tabs/trending")

        max_retries = 3
        retries = 0

        # while retries < max_retries:
        #     try:
        #         retry_button = WebDriverWait(driver, 100).until(
        #             EC.presence_of_element_located(
        #                 (By.XPATH, '//button[contains(text(), "Retry")]')
        #             )
        #         )
        #         retry_button.click()
        #         retries += 1
        #         print(f"Retry attempt {retries}.")
        #     except TimeoutException:
        #         break

        # page_source = driver.page_source
        file_path = os.path.join(os.path.dirname(__file__), "page_source.html")
        with open(file_path, "r", encoding="utf-8") as file:
            page_source = file.read()

        # Scrape top 5 trending topics
        topics = []
        soup = BeautifulSoup(page_source, "html.parser")
        elements = soup.select("span.r-18u37iz span.css-1jxf684")
        # elements = WebDriverWait(driver, 100).until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH, '//span[contains(@class, "css-901oao")]')
        #     )
        # )
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
