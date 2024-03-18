from seleniumwire import webdriver
from fake_useragent import UserAgent
import httpx
from dotenv import load_dotenv, find_dotenv
import logging
import json
import os

import Pages


load_dotenv(find_dotenv())


PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_LOGIN = os.getenv('PROXY_LOGIN')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
TWITTER_AUTH_TOKEN = os.getenv('TWITTER_AUTH_TOKEN')



logging.basicConfig(filename='logs.log',
                        filemode='w',
                        level=logging.INFO,
                        format='%(asctime)s - %(name)-8s - %(lineno)-3s - %(levelname)s - %(message)s',
                        encoding='utf-8')


def firts_task():
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

    driver = webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_option)

    main_page = Pages.MainPage(driver)
    main_page.go_to_site()
    main_page.hover_and_click_dropdown(hover='MARKET DATA', 
                                       click='Pre-Open Market')
    
    pre_open_market_page = Pages.PreOpenMarketPage(driver)
    pre_open_market_page.scrape_data()

    main_page.go_to_site()
    main_page.click_to_tab(tab="NIFTY BANK")
    main_page.click_to_view_all()
    
    live_equity_market = Pages.LiveEquityMarketPage(driver)
    live_equity_market.select_dropdown(name="NIFTY ALPHA 50")
    live_equity_market.scroll_over_table()

    driver.close()


def second_task():
    logger = logging.getLogger('second_task')

    proxy_url = f'http://{PROXY_LOGIN}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'

    proxies = {
        'https://': proxy_url
    }

    url = 'https://syndication.twitter.com/srv/timeline-profile/screen-name/elonmusk'

    cookies = {
        'auth_token': TWITTER_AUTH_TOKEN,
    }

    with httpx.Client(proxies=proxies) as client:
        r = client.get(url, cookies=cookies)
        logger.info(f'Status code: {r.status_code}')
        data = r.text
        data = data[data.find('{'):data.rfind('}')+1]
        data = json.loads(data)['props']['pageProps']['timeline']
        for i, item in enumerate(data['entries']):
            if i >= 10:
                break
            logger.info(item['content']['tweet']['full_text'])


if __name__ == '__main__':
    firts_task()
    second_task()