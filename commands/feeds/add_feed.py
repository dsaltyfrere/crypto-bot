from telegram import Update
from telegram.ext import ContextTypes
from utils import reply
from models.feed import Feed

import logging
logger = logging.getLogger(__name__)

async def add_feed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")
    args = context.args
    if len(args) < 2:
        response = f"Not enough arguments provided"
        await reply(update, response)
    else:
        if Feed.select().where(Feed.feed_url == args[1]).exists():
            response = f"Can't add feed with duplicate URL"
            await reply(update, response)
        elif Feed.select().where(Feed.feed_name == args[0]).exists():
            response = f"Can't add feed with duplicate name"
            await reply(update, response)
        else:
            Feed.create(
                feed_name = args[0],
                feed_url = args[1],
                preview = False
            )
            response = f"Subscribed to [{args[0]}]({args[1]})"
            logger.info(response)
            await reply(update, response)
        