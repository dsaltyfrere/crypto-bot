import logging

from telegram import Update
from telegram.ext import ContextTypes
from models.whalepool.transaction_type import WhalepoolTransactionType

logger = logging.getLogger(__name__)

async def add_whalepool_transaction_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        context.args[0]
        WhalepoolTransactionType.create(
            transaction_type = context.args[0]
        )
        response = f'{context.args[0]} added as whalepool type.'
        await update.effective_message.reply_text(response)
    except Exception as e:
        logger.error(e)