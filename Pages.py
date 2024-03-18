from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import logging
import csv

from BaseApp import BasePage, screenshot
import locators


logger = logging.getLogger(__name__)


class MainPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def hover_and_click_dropdown(self, hover: str, click: str) -> None:
        """
        Hover over a dropdown menu item and click on a specified item within the dropdown.

        Agrs:
            param hover: The text of the dropdown menu item to hover over.
            param click: The text of the item within the dropdown to click on.
        """
        try:
            header_menu = self.find_elements(locators.MainPageLocators.HEADER_MENU)
            menu_to_hover = [item for item in header_menu if hover in item.text][0]
            logger.info(f"Hover over {menu_to_hover.text}")
            ActionChains(self.driver).move_to_element(menu_to_hover).perform()
            menu_to_click = [item for item in header_menu if click in item.text][0]
            logger.info(f"Click on {menu_to_click.text}")
            menu_to_click.click()
        except Exception as error:
            logger.exception(f"Can't hover and click dropdown: {error}")
            screenshot(self.driver, 'hover_and_click_dropdown')

    def click_to_tab(self, tab: str) -> None:
        """
        Click on a specified tab.

        Agrs:
            param tab: The text of the tab to click on.
        """
        try:
            tabs_boxes = self.find_elements(locators.MainPageLocators.TABS_BOXES)
            tab_to_click = [item for item in tabs_boxes if tab in item.text][0]
            logger.info(f"Click on {tab_to_click.text}")
            tab_to_click.click()
        except Exception as error:
            logger.exception(f"Can't click on tab: {error}")
            screenshot(self.driver, 'click_to_tab')

    def click_to_view_all(self) -> None:
        """
        Click to view all items in the right box
        """
        try:
            right_box = self.find_elements(locators.MainPageLocators.RIGHT_BOX)
            wanted_box = [item for item in right_box if item.is_displayed()][0]
            view_all = self.find_element(locators.MainPageLocators.VIEW_ALL, parent=wanted_box)
            self.scroll_to_element(wanted_box)
            self.find_elements(locators.MainPageLocators.RIGHT_BOX_ITEMS)
            logger.info(f"Click on {view_all.text}")
            view_all.click()
        except Exception as error:
            logger.exception(f"Can't click on view all: {error}")
            screenshot(self.driver, 'click_to_view_all')

class PreOpenMarketPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def scrape_data(self) -> None:
        """
        Scrapes data from a web page and writes it to a CSV file.
        """
        try:
            with open('data.csv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                logger.info("Get name")
                items = self.find_elements(locators.PreOpenMarketPageLocators.ITEMS_NAME)
                logger.info("Get price")
                price = self.find_elements(locators.PreOpenMarketPageLocators.ITEMS_PRIVE)
                logger.info("Write data")
                for item_name, item_price in zip(items, price):
                    writer.writerow([item_name.text, item_price.text])
        except Exception as error:
            logger.exception(f"Can't scrape data: {error}")
            screenshot(self.driver, 'scrape_data')

class LiveEquityMarketPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def select_dropdown(self, name: str) -> None:
        """
        Selects the dropdown option with the specified name.

        Args:
            name (str): The name of the dropdown option to select.
        """
        try:
            dropdown = self.find_element(locators.LiveEquityMarketPageLocators.DROPDOWN_LIST)
            self.find_elements(locators.LiveEquityMarketPageLocators.ITEMS_NAME)
            for item in Select(dropdown).options:
                if name in item.text:
                    logger.info(f"Choose dropdown: {name}")
                    item.click()
                    break
        except Exception as error:
            logger.exception(f"Can't choose dropdown: {error}")
            screenshot(self.driver, 'choose_dropdown')

    def scroll_over_table(self) -> None:
        """
        A function that scrolls over a table by finding the table element and scrolling to each item within the table. 
        """
        try:
            table = self.find_elements(locators.LiveEquityMarketPageLocators.ITEMS_NAME)
            logger.info("Scroll over table")
            for item in table:
                self.scroll_to_element(item)
        except Exception as error:
            logger.exception(f"Can't scroll over table: {error}")
            screenshot(self.driver, 'scroll_over_table')

    