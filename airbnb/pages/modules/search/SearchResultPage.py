from selenium.webdriver.common.by import By
import time as tm
from interactor.mks.driver import BaseAUT as base
from airbnb.pages.modules.search import HotelDescriptionPage

driver = base.driver


class HotelsList:
    HOTELS_LIST_TITLES_XPATH = "//a[@rel='noopener']//div[@class='_1dss1omb']"

    def __init__(self):
        pass

    def get_hotels_and_total_count(self):
        hotels_title = driver.find_elements(By.XPATH, self.HOTELS_LIST_TITLES_XPATH)
        return hotels_title, hotels_title.__sizeof__(),

    def click_hotel_based_on_position(self, position):
        listed_hotels, total_hotels_count = self.get_hotels_and_total_count()
        text = listed_hotels[position-1].text
        listed_hotels[position-1].click()
        return text


hotels = HotelsList()


def validate_products_navigation(*resulted_hotel_position):
    results, total_hotels_found = hotels.get_hotels_and_total_count()

    if total_hotels_found < max(resulted_hotel_position):
        raise ValueError(
            "The resulted position of the hotels provided as input is %d, and it is higher than the resulted count of "
            "hotel %d" % (
                total_hotels_found, max(resulted_hotel_position)))
    else:
        for position in resulted_hotel_position:
            expected_hotel_title = hotels.click_hotel_based_on_position(position)
            tm.sleep(3)
            windows = driver.window_handles
            driver.switch_to.window(windows[1])
            print("expected_hotel_title is ", expected_hotel_title)
            HotelDescriptionPage.validate_hotel(expected_hotel_title)
            driver.close()
            driver.switch_to.window(windows[0])
