import logging

from telegram import Update
from telegram.ext import ContextTypes
from models.whalepool.transaction_type import WhalepoolTransactionType

logger = logging.getLogger(__name__)

async def remove_whalepool_transaction_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        context.args[0]
        t = WhalepoolTransactionType.get_or_none(WhalepoolTransactionType.transaction_type == context.args[0])
        if t is not None:
            t.delete_instance()
            response = f'Deleted {context.args[0]}'
            await update.effective_message.reply_text(response)
        else:
            response = f'Could not find type {context.args[0]}.'
            await update.effective_message.reply_text(response)       
         
    except Exception as e:
        logger.error(e)