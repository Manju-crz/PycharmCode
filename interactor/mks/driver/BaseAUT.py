from mks.driver.connectors.Connector import Connection

AUT_URL = "https://www.airbnb.co.in/"
PAGE_LOAD_TIMEOUT = 20
IMPLICIT_ELEMENT_TIMEOUT = 10
connection = Connection()
driver = connection.getdriver()


def end_connection():
    connection.closedriver()
