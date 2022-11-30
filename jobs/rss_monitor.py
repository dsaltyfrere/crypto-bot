import requests, xmltodict
import logging
import os

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from datetime import datetime

from models.feed import Feed
from models.entry import FeedEntry


logger = logging.getLogger(__name__)
headers = {'User-agent': 'Mozilla/5.0 (X11; Linux i686; rv:98.0) Gecko/20100101 Firefox/98.0'}

async def rss_monitor(context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        feeds = Feed.select().where(Feed.feed_enabled == True)

        for feed in feeds:
            try:
                response = requests.get(
                    feed.feed_url,
                    headers=headers,
                    timeout=10
                )
            except requests.exceptions.ReadTimeout as rt:
                logger.error(f"Read timeout for feed {feed.feed_name}")
                feed.feed_fetch_attempts = feed.feed_fetch_attempts + 1
                feed.save()
                continue
            except Exception as exc:
                logger.error("Something unexpected happened.")
                logger.error(exc, exc_info=True)
                feed.feed_fetch_attempts = feed.feed_fetch_attempts + 1
                feed.save()
                continue

            if response.status_code != 200:
                logger.error(f"Feed {feed.feed_name} returned HTTP_STATUS_CODE: {response.status_code}")
                feed.feed_fetch_attempts = feed.feed_fetch_attempts + 1
                feed.save()
                continue

            try:
                feed_content = xmltodict.parse(response.content)
            except Exception as e:
                logger.error(f"Couldn't parse response of {feed.feed_name}")
                feed.feed_fetch_attempts = feed.feed_fetch_attempts +1
                feed.save()
                continue

            if feed.feed_fetch_attempts >= 3:
                feed.enabled = False
                continue

            response_messages = []

            try:
                response_messages = feed_content['rss']['channel']['item']
            except KeyError as ke:
                logger.error(f"Couldn't process {feed.feed_name}")
                logger.debug(ke, exc_info=True)
            except Exception as exc:
                logger.debug(exc, exc_info=True)

            for message in response_messages:
                try:
                    entry = FeedEntry.get_or_none(FeedEntry.entry_link == message['link'], FeedEntry.entry_title == message['title'])
                except TypeError as te:
                    logger.error(f"Provided input to search for FeedEntry is invalid: feed {feed.feed_name}")
                
                if entry is None:
                    logger.info(f"New message for {feed.feed_name} found: {message['title']}")
                    feed_entry = FeedEntry.create(
                        feed = feed.id,
                        entry_title = message['title'],
                        entry_link = message['link'],
                        entry_published_at = message['pubDate'] if message['pubDate'] else None,
                        send = 0
                    )
                    feed_entry.save()
                    response = f"<b>{feed.feed_name}</b>: <a href='{feed_entry.entry_link}'>{feed_entry.entry_title}</a>\n{datetime.strptime(feed_entry.entry_published_at, feed.feed_datetime_regex).strftime('%d/%m/%Y %H:%M:%S')}."
                    await context.bot.send_message(
                        chat_id = os.getenv("CHAT_ID", None),
                        text = response,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview = feed.feed_preview
                    )

                    feed_entry.send = 1
                    feed_entry.save()
                    
    except Exception as exc:
        logger.error(exc, exc_info=True)

