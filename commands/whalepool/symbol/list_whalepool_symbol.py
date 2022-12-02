import logging

from telegram import Update
from telegram.ext import ContextTypes
from models.whalepool.symbol import WhalepoolTransactionSymbol

logger = logging.getLogger(__name__)

async def list_whalepool_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"list_whalepool_symbol by {update.effective_user.username}")
    symbols = WhalepoolTransactionSymbol.select()
    response = f'Filtered symbols: '
    for s in symbols:
        response += f'{s.symbol}, '
    await update.effective_message.reply_text(response[:-2])