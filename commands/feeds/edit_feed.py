from telegram import Update
from telegram.ext import ContextTypes
from models.feeds.feed import Feed
from utils import reply

import logging
logger = logging.getLogger(__name__)

async def edit_feed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")
    args = context.args

    if len(args) < 2:
        response = f"Not enough arguments provided"
        await reply(update, response)
    else:
        feed_to_update = Feed.select().where(Feed.feed_name == args[0]).first()
        previous_url = feed_to_update.feed_url
        feed_to_update.feed_url = args[1]
        feed_to_update.save()
        response = f"updated url from [old link]({previous_url}) to [new link]({args[1]})"
        logger.info(response)
        await reply(update, response)

async def change_preview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")
    
    args = context.args

    if len(args) < 2:
        response = f"Not enough arguments supplied"
        await reply(update, response)
        return
    
    feed = Feed.select().where(Feed.feed_name == args[0])
    feed.feed_preview = True if args[1] == 'off' else False
    response = f"Preview set to <b>{context.args[1]}</b> for feed <b>{feed.name}</b>."
    await reply(update, response)
    
    