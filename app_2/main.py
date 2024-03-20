import httpx
import logging
import os
from dotenv import load_dotenv, find_dotenv
import json


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
    TWITTER_AUTH_TOKEN = os.getenv('TWITTER_AUTH_TOKEN')  
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    TWITTER_CT0_TOKEN = os.getenv('TWITTER_CT0_TOKEN')

    proxy_url = f'http://{PROXY_LOGIN}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'

    proxies = {
        'https://': proxy_url
    }

    url = "https://twitter.com/i/api/graphql/eS7LO5Jy3xgmd3dbL044EA/UserTweets?variables=%7B%22userId%22%3A%2244196397%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"

    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}",
        "X-Csrf-Token": TWITTER_CT0_TOKEN
    }

    cookies = {
        "auth_token": TWITTER_AUTH_TOKEN,
        "ct0": TWITTER_CT0_TOKEN,
    }

    with httpx.Client(proxies=proxies) as client:
        try:
            r = client.get(url, headers=headers, cookies=cookies)
            logger.info(f'Status code: {r.status_code}')
        except Exception as error:
            logger.exception(f'Error: {error}')


        data = r.text
        data = json.loads(data)['data']['user']['result']['timeline_v2']['timeline']['instructions'][2]

        i = 1
        for item in data['entries']:
            if i > 10:
                break
            try:
                logger.info(item['content']['itemContent']['tweet_results']['result']['legacy']['full_text'].replace('\n', ' '))
                i += 1
            except KeyError:
                try:
                    for sub_items in item['content']['items']:
                        logger.info(sub_items['item']['itemContent']['tweet_results']['result']['legacy']['full_text'].replace('\n', ' '))
                        i += 1
                except KeyError:
                    pass
                except Exception as error:
                    logger.exception(f'Error during handling sub_items: {error}')
            except Exception as error:
                logger.exception(f'Error during handling items: {error}')

if __name__ == '__main__':
    main()