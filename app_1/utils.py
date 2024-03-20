from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import logging
import datetime


logger = logging.getLogger(__name__)

def screenshot(driver, item) -> None:
    """
    Generate a screenshot using the provided driver and item.

    Args:
        driver (object): The driver for capturing the screenshot.
        item (str): The item to be included in the screenshot filename.
    """
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    driver.save_screenshot(f'screenshot_{timestamp}_{item}.png')


def find_element(driver, locator, parent=None, time=10) -> WebElement | None:
    """
    Find and return an element located by the given locator within the specified parent element or the default driver. 
    If the element is not found within the specified time, an exception is raised.
    
    Args:
        locator: The locator used to find the element.
        parent: The parent element within which to search for the element (default is None).
        time: The time to wait for the element to be located (default is 10).
    """
    try:
        if parent:
            logger.info(f"Find element by locator {locator} in parent {parent}")
            return WebDriverWait(parent, time).until(EC.presence_of_element_located(locator),
                                                    message=f"Can't find element by locator {locator} in parent {parent}")
        else:
            logger.info(f"Find element by locator {locator}")
            return WebDriverWait(driver, time).until(EC.presence_of_element_located(locator),
                                                            message=f"Can't find element by locator {locator}")
    except Exception as error:
        if parent:
            logger.exception(f"Can't find element by locator {locator} in parent {parent}: {error}")
            screenshot(driver, locator)
        else:
            logger.exception(f"Can't find element by locator {locator}: {error}")
            screenshot(driver, locator)


def find_elements(driver, locator, parent=None, time=10) -> list[WebElement] | None:
    """
    Find and return an elements located by the given locator within the specified parent element or the default driver. 
    If the elements is not found within the specified time, an exception is raised.
    
    Args:
        locator: The locator used to find the elements.
        parent: The parent element within which to search for the element (default is None).
        time: The time to wait for the element to be located (default is 10).
    """
    try:
        if parent:
            logger.info(f"Find elements by locator {locator} in parent {parent}")
            return WebDriverWait(parent, time).until(EC.presence_of_all_elements_located(locator),
                                                        message=f"Can't find elements by locator {locator} in parent {parent}")
        else:
            logger.info(f"Find elements by locator {locator}")
            return WebDriverWait(driver, time).until(EC.presence_of_all_elements_located(locator),
                                                            message=f"Can't find elements by locator {locator}")
    except Exception as error:
        if parent:
            logger.exception(f"Can't find elements by locator {locator} in parent {parent}: {error}")
            screenshot(driver, locator)
        else:
            logger.exception(f"Can't find elements by locator {locator}: {error}")
            screenshot(driver, locator)