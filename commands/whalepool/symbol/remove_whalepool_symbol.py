import logging

from telegram import Update
from telegram.ext import ContextTypes
from models.whalepool.symbol import WhalepoolTransactionSymbol

logger = logging.getLogger(__name__)

async def remove_whalepool_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"remove_whalepool_symbol by {update.effective_user.username}")
    try:
        context.args[0]
        symbol = WhalepoolTransactionSymbol.get_or_none(symbol = context.args[0])
        if symbol is not None:
            response = f'Symbol {symbol.symbol} removed.'
            await update.effective_message.reply_text(response)
        else:
            response = f'Symbol {symbol.symbol} was not found.'
            await update.effective_message.reply_text(response)
    except Exception as e:
        logger.error(e)