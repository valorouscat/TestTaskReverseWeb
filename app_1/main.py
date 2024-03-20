from seleniumwire import webdriver
from fake_useragent import UserAgent
from dotenv import load_dotenv, find_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import csv
import logging
import os
from selenium.webdriver.common.by import By

import utils




def main():
    logging.basicConfig(filename='logs.log',
                        filemode='w',
                        level=logging.INFO,
                        format='%(asctime)s - %(name)-8s - %(lineno)-3s - %(levelname)s - %(message)s',
                        encoding='utf-8')

    logger = logging.getLogger('main')
    
    load_dotenv(find_dotenv())

    PROXY_HOST = os.getenv('PROXY_HOST')
    PROXY_PORT = os.getenv('PROXY_PORT')
    PROXY_LOGIN = os.getenv('PROXY_LOGIN')
    PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')

    seleniumwire_logger = logging.getLogger('seleniumwire')
    seleniumwire_logger.setLevel(logging.ERROR)

    options = webdriver.ChromeOptions()
    seleniumwire_option = {
        'proxy': {
            'https': f'https://{PROXY_LOGIN}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'
        }
    }
    options.add_experimental_option('excludeSwitches', ['enable-logging', "enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f'user-agent={UserAgent().random}')

    # driver = webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_option)
    with webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_option) as driver:
        
        # Main page
        # go to site
        try:
            driver.get('https://www.nseindia.com/')
        except Exception as error:
            logger.exception(f"Can't go to site: {error}")
            utils.screenshot(driver, 'go_to_site')
            return

        # hover and click
        try: 
            header_menu = utils.find_elements(driver, (By.CSS_SELECTOR, '.navbar-light .navbar-nav .nav-link'))
            menu_to_hover = [item for item in header_menu if 'MARKET DATA' in item.text][0]
            logger.info(f"Hover over {menu_to_hover.text}")
            ActionChains(driver).move_to_element(menu_to_hover).perform()
            menu_to_click = [item for item in header_menu if 'Pre-Open Market' in item.text][0]
            logger.info(f"Click on {menu_to_click.text}")
            menu_to_click.click()
        except Exception as error:
            logger.exception(f"Can't hover and click dropdown: {error}")
            utils.screenshot(driver, 'hover_and_click_dropdown')
            return

        # Pre-open market page
        # scrape data
        try:
            with open('data.csv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                logger.info("Get name")
                items = utils.find_elements(driver, (By.CSS_SELECTOR, 'a.symbol-word-break'))
                logger.info("Get price")
                price = utils.find_elements(driver, (By.CSS_SELECTOR, '.customTable-width > .customHeight-table > tbody .bold'))
                logger.info("Write data")
                for item_name, item_price in zip(items, price):
                    writer.writerow([item_name.text, item_price.text])
        except Exception as error:
            logger.exception(f"Can't scrape data: {error}")
            utils.screenshot(driver, 'scrape_data')
            return

        # Main page
        # go to site 
        try:
            driver.get('https://www.nseindia.com/')
        except Exception as error:
            logger.exception(f"Can't go to site: {error}")
            utils.screenshot(driver, 'go_to_site')
            return

        # click to tab
        try:
            tabs_boxes = utils.find_elements(driver, (By.CSS_SELECTOR, '.tabs_boxes .nav-tabs .nav-link'))
            tab_to_click = [item for item in tabs_boxes if "NIFTY BANK" in item.text][0]
            logger.info(f"Click on {tab_to_click.text}")
            tab_to_click.click()
        except Exception as error:
            logger.exception(f"Can't click on tab: {error}")
            utils.screenshot(driver, 'click_to_tab')
            return

        # click to view all
        try:
            right_box = utils.find_elements(driver, (By.CSS_SELECTOR, '.right_box'))
            wanted_box = [item for item in right_box if item.is_displayed()][0]
            view_all = utils.find_element(driver, (By.CSS_SELECTOR, '.right_box .link-wrap a'), parent=wanted_box)
            driver.execute_script("arguments[0].scrollIntoView();", wanted_box)
            logger.info(f"Scroll to element")
            utils.find_elements(driver, (By.CSS_SELECTOR, 'a.symbol-word-break'))
            logger.info(f"Click on {view_all.text}")
            view_all.click()
        except Exception as error:
            logger.exception(f"Can't click on view all: {error}")
            utils.screenshot(driver, 'click_to_view_all')
            return

        # Live equity market page
        # select dropdown
        try:
            dropdown = utils.find_element(driver, (By.ID, 'equitieStockSelect'))
            utils.find_elements(driver, (By.CSS_SELECTOR, 'a.symbol-word-break'))
            for item in Select(dropdown).options:
                if "NIFTY ALPHA 50" in item.text:
                    logger.info(f"Choose dropdown: NIFTY ALPHA 50")
                    item.click()
                    break
        except Exception as error:
            logger.exception(f"Can't choose dropdown: {error}")
            utils.screenshot(driver, 'choose_dropdown')
            return

        # scroll over table
        try:
            table = utils.find_elements(driver, (By.CSS_SELECTOR, 'a.symbol-word-break'))
            logger.info("Scroll over table")
            for item in table:
                driver.execute_script("arguments[0].scrollIntoView();", item)
        except Exception as error:
            logger.exception(f"Can't scroll over table: {error}")
            utils.screenshot(driver, 'scroll_over_table')
            return

if __name__ == '__main__':
    main()
