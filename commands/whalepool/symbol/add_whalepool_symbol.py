import logging

from telegram import Update
from telegram.ext import ContextTypes
from models.whalepool.symbol import WhalepoolTransactionSymbol

logger = logging.getLogger(__name__)

async def add_whalepool_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"add_whalepool_symbol by {update.effective_user.username}")
    try:
        args = context.args
        if len(args) < 1:
            await update.effective_message.reply_text(f"Not enough arguments supplied")
            return
        
        WhalepoolTransactionSymbol.create(
            symbol = args[0]
        )
        response = f"{args[0]} added as whalepool symbol."
        await update.effective_message.reply_text(response)
    except Exception as e:
        logger.error(e, exc_info=True)
