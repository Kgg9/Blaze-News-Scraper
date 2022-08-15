# Imports needed to make the project run

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep

class TwitterAccountPost():
    def __init__(self, username, password,textData):

        self.username = username
        self.password = password
        self.textData = textData
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def postTweet(self):
        self.driver.get('https://tweetdeck.twitter.com/')
        sleep(1)

        self.driver.find_element(By.LINK_TEXT,"Log in").click()
        sleep(2)

        usernameBox = self.driver.find_element(By.CSS_SELECTOR,"input[name='text'][type='text']")
        usernameBox.send_keys(self.username)
        self.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div').click()
        sleep(1)

        passwordBox = self.driver.find_element(By.CSS_SELECTOR,"input[name='password'][type='password']")
        passwordBox.send_keys(self.password)

        self.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()
        sleep(3)

        self.driver.find_element(By.XPATH,'/html/body/div[3]/header/div/button/span').click()
        tweetBox = self.driver.find_element(By.CSS_SELECTOR,"textarea")
        tweetBox.send_keys(self.textData)
        sleep(0.5)

        # self.driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[12]/div/div/button').click()
        # sleep(5)
