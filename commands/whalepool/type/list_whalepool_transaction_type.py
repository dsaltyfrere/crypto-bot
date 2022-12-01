import logging

from telegram import Update
from telegram.ext import ContextTypes
from models.whalepool.transaction_type import WhalepoolTransactionType

logger = logging.getLogger(__name__)

async def list_whalepool_transaction_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    types = WhalepoolTransactionType.select()
    response = f'Monitored whalepool types: \n'
    for type in types:
        response += f'{type.transaction_type}, '
    await update.effective_message.reply_text(response[:-2])