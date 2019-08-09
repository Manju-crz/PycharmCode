from selenium.webdriver.common.by import By
import time as tm
from interactor.mks.driver import BaseAUT as base

driver = base.driver


class Hotel:
    HOTEL_TITLE_TEXT_XPATH = "//div[@id='summary']//h1"

    def __init__(self):
        pass

    def get_hotel_title_text(self):
        act_product_header = driver.find_element(By.XPATH, self.HOTEL_TITLE_TEXT_XPATH).text
        return act_product_header


hotel = Hotel()


def validate_hotel(hotel_title):
    act_page_title = driver.title
    assert hotel_title in act_page_title, \
        "Redirected page title from the resulted option is not matching with the product header and the expected is " + \
        hotel_title + ", and the found actual page header is " + act_page_title
    act_hotel_header = hotel.get_hotel_title_text()
    # assert hotel_title == act_hotel_header, "Redirected page's product displayed heder is not matching with " \
                                              # "the resulted page product header and the expected is " + \
                                              # hotel_title + ", and the found actual page header is " \
                                              # + act_hotel_header
