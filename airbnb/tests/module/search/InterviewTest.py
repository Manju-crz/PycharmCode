from interactor.mks.driver import BaseAUT as base
from airbnb.pages.modules.search import SearchHomePage
from airbnb.pages.modules.search import SearchResultPage
from mks.utility import MksDates as mydate

LOCATION_NAME = "Sicily, Italy"
CHECKIN_DATE = mydate.get_date_of_today()
CHECKOUT_DATE = mydate.add_days_to_today(90)
ADULTS_COUNT = 1
CHILDREN_COUNT = 2
INFANTS_COUNT = 0

SearchHomePage.validate_page_title()
SearchHomePage.submit_search_hotels_form(LOCATION_NAME, CHECKIN_DATE, CHECKOUT_DATE, ADULTS_COUNT, CHILDREN_COUNT,
                                         INFANTS_COUNT)
SearchResultPage.validate_products_navigation(1, 3)
base.end_connection()
