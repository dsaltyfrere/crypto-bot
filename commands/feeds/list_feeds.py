from telegram import Update
from telegram.ext import ContextTypes
from models.feed import Feed
from utils import reply

import logging
logger = logging.getLogger(__name__)

async def list_feeds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")
    feeds = Feed.select()
    if len(feeds) == 0:
        response = f"There are **no** active feeds"
        await reply(update, response)
    else:
        response = f"Subscribed to **{len(feeds)}** feeds\n"

        for feed in feeds:
            response += f"[{feed.feed_name}]({feed.feed_url})\n"
        logger.info(response)
        await reply(update, response)
        