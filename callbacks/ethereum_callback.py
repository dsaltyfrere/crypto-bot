from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)


async def ethereum_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    TO BE IMPLEMENTED
    Broadcast message on RMQ to handle purchase
    """
    
    query = update.callback_query
    logger.info(f"Callback hit: {query.data}")