from telegram import Update
from telegram.ext import ContextTypes
from models.feed import Feed
from utils import reply

import logging
logger = logging.getLogger(__name__)

async def remove_feed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")
    args = context.args

    if len(args) < 1:
        response = f"Not enough arguments provided"
        await reply(update, response)
    else:
        if Feed.select().where(Feed.feed_name == args[0]).exists():
            feed_to_delete = Feed.select().where(Feed.feed_name == args[0]).first()
            response = f"{feed_to_delete.feed_name} deleted"
            feed_to_delete.delete_instance()
            await reply(update, response)
        elif Feed.select().where(Feed.feed_url == args[0]).exists():
            feed_to_delete = Feed.select().where(Feed.feed_url == args[0]).first()
            response = f"{feed_to_delete.feed_name} deleted"
            feed_to_delete.delete_instance()
            await reply(update, response)
        else:
            response = f"Feed {args[0]} not found"
            await reply(update, response)
            
            
        