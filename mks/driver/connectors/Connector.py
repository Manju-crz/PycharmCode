from selenium import webdriver
from interactor.mks.driver import BaseAUT as base
from mks.utility import MksFileSystem as fs

class Connection:

    def __init__(self):
        folder = fs.get_project_root()
        folder = str(folder) + "\\drivers\\chromedriver"
        print("folder is : " + folder)
        self.driver = webdriver.Chrome(executable_path=folder)
        self.driver.get(base.AUT_URL)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(base.PAGE_LOAD_TIMEOUT)
        self.driver.implicitly_wait(base.IMPLICIT_ELEMENT_TIMEOUT)

    def launchchrome(self):
        driver = webdriver.Chrome(executable_path="C:\\MyDATA\\PycharmCode\\drivers\\chromedriver")
        driver.get("https://www.airbnb.co.in/")
        print("driver.title is", driver.title)  # Title  of the page...

    def closedriver(self):
        print("Before close")
        self.driver.quit()
        print("After close")

    def getdriver(self):
        return self.driver

