import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)
fear_img_url = "https://alternative.me/crypto/fear-and-greed-index.png"

async def fear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"fear request by {update.effective_user.username}")
    await context.bot.photo(
        update.message.chat_id,
        fear_img_url
    )
