# Imports needed to make the project run

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class Google():
    def __init__(self,time,keyword,pages, base_url):
        self.time = time
        self.keyword = keyword
        self.pages = pages
        self.base_url = base_url
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def pre_Scraper(self, url, keyword, time):

        url = url[:32] + keyword + url[32:]

        self.driver.get(url)
        sleep(0.5)
        self.driver.find_element(By.ID, "hdtb-tls").click()
        sleep(0.5)
        self.driver.find_element(By.CLASS_NAME, "KTBKoe").click()

        if time == "Past hour":
            self.driver.find_element(By.LINK_TEXT, "Past hour").click()
            url = self.driver.current_url
        elif time == "Past 24 hours":
            self.driver.find_element(By.LINK_TEXT, "Past 24 hours").click()
            url = self.driver.current_url
        elif time == "Past week":
            self.driver.find_element(By.LINK_TEXT, "Past week").click()
            url = self.driver.current_url
        elif time == "Past month":
            self.driver.find_element(By.LINK_TEXT, "Past month").click()
            url = self.driver.current_url
        elif time == "Past year":
            self.driver.find_element(By.LINK_TEXT, "Past year").click()
            url = self.driver.current_url

        return url


    # A Function used for Scrapping the News for a certain Keyword

    def news_Scraper(self, pageSoruce):

        pageArticles = []

        page = BeautifulSoup(pageSoruce, 'lxml')
        articles = page.find_all('div', class_='xuvV6b BGxR7d')

        for article in articles:
            Title = article.find('div', class_='mCBkyc y355M ynAwRc MBeuO nDgy9d').get_text().replace("\n","").replace("...", "")
            Descirption = article.find('div', class_='GI74Re nDgy9d').get_text().replace("\n", "").replace("...", "")
            Time = article.find('div', class_='OSrXXb ZE0LJd').get_text()
            Link = article.find('a', href=True)['href']
            pageArticles.append((Title, Descirption, Time, Link))

        return pageArticles


    # Function used to go to the Next page of Google News, and getting the scrapped content in tupples

    def next_Pages(self, url, pages):

        newsArticles = []

        self.driver.get(url)
        sleep(0.5)

        for i in range(pages):
            try:
                newsArticles.append(self.news_Scraper(self.driver.page_source))
                next_Icon = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((By.ID, "pnnext"))
                )
                next_Icon.click()
            except:
                break
        return newsArticles

    # Function used to Start the Scraping Process

    def Start(self):
        basePageUrl = self.pre_Scraper(self.base_url, self.keyword, self.time)
        newsArticles = self.next_Pages(basePageUrl, self.pages)
        return newsArticles


