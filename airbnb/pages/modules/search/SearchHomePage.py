from selenium.webdriver.common.by import By
import time as tm
from interactor.mks.driver import BaseAUT as base
from mks.utility import MksDates as mydates

driver = base.driver

SEARCHFORM_TITLE_TXT = "Book unique places to stay and things to do."


class SearchForm:
    SEARCHFORM_TITLE_XPATH = "//h1"
    COOKIES_OK_BUTTON_XPATH = "//button[@class='optanon-allow-all accept-cookies-button']"
    LOCATION_SELECTBOX_EDITFIELD_XPATH = "//div[@class='_slilk2']//input[@role='combobox']"
    LOCATION_SELECTBOX_OPTIONS_XPATH = "//ul[@id='Koan-magic-carpet-koan-search-bar__listbox']//div[" \
                                       "@class='_1avdemu']//span "

    CALENDAR_XPATH = "//div[@aria-label='Calendar']"
    CALENDAR_MONTH_YEAR_LABEL_XPATH = "//div[@class='_1lds9wb']//strong"
    CALENDAR_MONTH_YEAR_NEXT_BUTTON_XPATH = "(//div[@aria-label='Calendar']//div[@role='button'])[2]"
    CALENDAR_DATES_XPATH = "//div[@class='_1lds9wb']//table[@role='presentation']//td[@role='button']"
    CHECKIN_CALENDAR_EDIT_FIELD_XPATH = "//input[@name='checkin']"
    CHECKOUT_CALENDAR_EDIT_FIELD_XPATH = "//input[@name='checkout']"

    GUEST_EXPANDER_EDITFIELD_XPATH = "//div[@class='_slilk2']//button[text()='Guests']"
    ADULTS_PLUS_ICON_XPATH = "(//div[contains(@aria-labelledby,'magic_carpet-marquee_search_bar-adults')]//button)[2]"
    CHILDREN_PLUS_ICON_XPATH = "(//div[contains(@aria-labelledby," \
                               "'magic_carpet-marquee_search_bar-children')]//button)[2] "
    INFANTS_PLUS_ICON_XPATH = "(//div[contains(@aria-labelledby,'magic_carpet-marquee_search_bar-infants')]//button)[2]"
    APPLY_BUTTON_XPATH = "//button[text()='Apply']"
    GUEST_SELECTED_LABEL_XPATH = "//button/div[@class='guest-label']"

    SEARCH_BUTTON_XPATH = "//button[@type='submit']"

    def __init__(self):
        pass

    def accept_cookies_popup(self):
        ok = driver.find_element_by_xpath(self.COOKIES_OK_BUTTON_XPATH)
        if ok.is_displayed():
            driver.find_element_by_xpath("//button[@class='optanon-allow-all accept-cookies-button']").click()
            tm.sleep(2)
        if ok.is_displayed():
            return False
        else:
            return True

    def select_location(self, location):
        edit_field = driver.find_element(By.XPATH, self.LOCATION_SELECTBOX_EDITFIELD_XPATH)
        edit_field.clear()
        edit_field.send_keys(location)
        tm.sleep(2)
        options = driver.find_elements(By.XPATH, self.LOCATION_SELECTBOX_OPTIONS_XPATH)
        for option in options:
            if option.text == location:
                option.click()
                tm.sleep(2)
                return True
        if edit_field.text == location:
            return True
        return False

    def expand_checkin_calendar(self):
        driver.find_element(By.XPATH, self.CHECKIN_CALENDAR_EDIT_FIELD_XPATH).click()
        tm.sleep(1)
        return driver.find_element(By.XPATH, self.CALENDAR_XPATH).is_displayed()

    def expand_checkout_calendar(self):
        driver.find_element(By.XPATH, self.CHECKOUT_CALENDAR_EDIT_FIELD_XPATH).click()
        tm.sleep(1)
        if driver.find_element(By.XPATH, self.CALENDAR_XPATH).is_displayed():
            return True
        else:
            False

    def click_opened_calendar_date(self, selectable_date):
        buttons = driver.find_elements(By.XPATH, self.CALENDAR_DATES_XPATH)
        for btn in buttons:
            if btn.get_attribute("aria-disabled") == "false" and int(str(btn.text).strip()) == int(
                    selectable_date):
                btn.click()
                return True
        return False

    def select_opened_calendar_date_month_year(self, selectable_date, month_name, year, among_next_months=12):
        for x in range(0, among_next_months):
            txt = driver.find_element(By.XPATH, self.CALENDAR_MONTH_YEAR_LABEL_XPATH).text
            if txt == month_name + " " + year and search_form.click_opened_calendar_date(selectable_date):
                return True
                break
            else:
                driver.find_element(By.XPATH, self.CALENDAR_MONTH_YEAR_NEXT_BUTTON_XPATH).click()
                tm.sleep(1)
        return False

    def select_calendar(self, date_to_select, is_check_in=False):
        if is_check_in:
            if self.expand_checkin_calendar() is not True:
                raise RuntimeError("Check in calendar has not displayed in the Ui to select date")
        else:
            if self.expand_checkout_calendar() is not True:
                raise RuntimeError("Check out calendar has not displayed in the Ui to select date")
        d, m, y = mydates.get_date_monthname_year_values_from_date(date_to_select)
        if search_form.select_opened_calendar_date_month_year(d, m, y):
            pass
        else:
            raise ValueError(
                'Looks like the given date %s is a past date or not lying within next 12 months' % date_to_select)

    def select_guests(self, adults=0, children=0, infants=0):
        driver.find_element(By.XPATH, self.GUEST_EXPANDER_EDITFIELD_XPATH).click()
        tm.sleep(1)
        for x in range(0, adults):
            driver.find_element(By.XPATH, self.ADULTS_PLUS_ICON_XPATH).click()
            tm.sleep(1)
        for x in range(0, children):
            driver.find_element(By.XPATH, self.CHILDREN_PLUS_ICON_XPATH).click()
            tm.sleep(1)
        for x in range(0, infants):
            driver.find_element(By.XPATH, self.INFANTS_PLUS_ICON_XPATH).click()
            tm.sleep(1)
        driver.find_element(By.XPATH, self.APPLY_BUTTON_XPATH).click()
        guest = driver.find_element(By.XPATH, self.GUEST_SELECTED_LABEL_XPATH).text
        if str(guest).strip() == str(adults + children + infants) + " guests":
            return True
        return False

    def get_search_form_title(self):
        return driver.find_element(By.XPATH, self.SEARCHFORM_TITLE_XPATH).text


search_form = SearchForm()


def submit_search_hotels_form(city_name, from_date, to_date, adults_count, children_count, infants_count):
    if search_form.accept_cookies_popup() is not True:
        raise RuntimeError("Even after accepting cookies popup, still the popup is displayed")
    if search_form.select_location(city_name) is not True:
        raise ValueError("Either given selectable value " + city_name + "is not existing in the drop down, or not "
                                                                        "selected successfully even after selected")
    search_form.select_calendar(from_date, True)
    search_form.select_calendar(to_date)
    if search_form.select_guests(adults_count, children_count) is not True:
        raise RuntimeError("All guests are not selected in the drop down box successfully")
    driver.find_element(By.XPATH, search_form.SEARCH_BUTTON_XPATH).click()


def validate_page_title():
    page_title = search_form.get_search_form_title()
    assert SEARCHFORM_TITLE_TXT == page_title.strip(), \
        "Found AirBnb home page header with the text '" + page_title + "', where expected is - " + SEARCHFORM_TITLE_TXT
