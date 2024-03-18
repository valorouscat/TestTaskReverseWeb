from selenium.webdriver.common.by import By

class MainPageLocators:
    HEADER_MENU = (By.CSS_SELECTOR, '.navbar-light .navbar-nav .nav-link')
    TABS_BOXES = (By.CSS_SELECTOR, '.tabs_boxes .nav-tabs .nav-link')
    RIGHT_BOX = (By.CSS_SELECTOR, '.right_box')
    RIGHT_BOX_ITEMS = (By.CSS_SELECTOR, 'a.symbol-word-break')
    VIEW_ALL = (By.CSS_SELECTOR, '.right_box .link-wrap a')


class PreOpenMarketPageLocators:
    ITEMS_NAME = (By.CSS_SELECTOR, 'a.symbol-word-break')
    ITEMS_PRIVE = (By.CSS_SELECTOR, '.customTable-width > .customHeight-table > tbody .bold')

class LiveEquityMarketPageLocators:
    DROPDOWN_LIST = (By.ID, 'equitieStockSelect')
    DROPDOWN_OPTION = (By.CSS_SELECTOR, '.live_mkt_watch .head_selectbox .custom_select select')
    ITEMS_NAME = (By.CSS_SELECTOR, 'a.symbol-word-break')