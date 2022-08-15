# Imports needed to make the project work

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep

class LinkedinAccountPoster():
    def __init__(self,username,password, companyPageUrl,postData):
        self.username = username
        self.password = password
        self.companyPageUrl = companyPageUrl
        self.postData = postData
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def login(self):
        self.driver.get('https://www.linkedin.com/home/?originalSubdomain=ca')

        usernameBox = self.driver.find_element(By.ID,'session_key')
        usernameBox.send_keys(self.username)

        sleep(0.5)
        passwordBox = self.driver.find_element(By.ID,'session_password')
        passwordBox.send_keys(self.password)
        sleep(2)
        passwordBox.send_keys(Keys.RETURN)


    def postCompanyPage(self):
        self.driver.get(self.companyPageUrl)
        sleep(2)

        display = self.driver.find_element(By.XPATH,'//*[@id = "main"]/div/div[1]/div/div[1]/button')
        display.click()
        sleep(1)

        postBox = self.driver.find_element(By.CLASS_NAME,'ql-editor.ql-blank')
        postBox.send_keys(self.postData)

        sleep(2)

        # self.driver.find_element(By.XPATH, "//button[contains(@class, 'share-actions__primary-action artdeco-button artdeco-button--2 artdeco-button--primary ember-view') and contains(., 'Post')]").click()

    def linkedinRun(self):
        self.login()
        self.postCompanyPage()
