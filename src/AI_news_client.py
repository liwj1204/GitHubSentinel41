import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from logger import LOG

# 设置ChromeDriver路径

class AINewsClient:
    def __init__(self):
        self.news_directory = 'ai_news'

    def fetch_ai_news(self):
        chrome_driver_path = '/usr/local/bin/chromedriver'  # Replace with your local chromedriver path

        # Configure Selenium options
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # Create browser object
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            # VentureBeat AI page URL
            url = 'https://venturebeat.com/category/ai/'

            # Load the page using Selenium
            driver.get(url)

            # Find article titles and links
            articles = driver.find_elements(By.CSS_SELECTOR, 'a.ArticleListing__title-link')

            # Generate file name with current date
            current_date = datetime.now().strftime('%Y-%m-%d')
            file_name = f'{self.news_directory}/{current_date}.md'

            # Create AI_news directory if it doesn't exist
            os.makedirs(self.news_directory, exist_ok=True)

            # Write to file in Markdown format
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(f"# AI News - {current_date}\n\n")
                for article in articles:
                    title = article.text.strip()
                    link = article.get_attribute('href')
                    file.write(f"- **[{title}]({link})**\n")

            return file_name
        finally:
            # Close the browser
            driver.quit()

    def get_latest_news_file(self):
        LOG.info("Getting the latest AI news file")
        self.fetch_ai_news()
        if not os.path.exists(self.news_directory):
            LOG.warning(f"AI news directory {self.news_directory} does not exist")
            return None

        files = os.listdir(self.news_directory)
        if not files:
            LOG.warning("AI news directory is empty")
            return None

        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.news_directory, f)))
        return os.path.join(self.news_directory, latest_file)

    # Other existing methods remain unchanged