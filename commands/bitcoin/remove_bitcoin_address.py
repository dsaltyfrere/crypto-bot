from telegram import Update
from telegram.ext import ContextTypes
from utils import reply
from models.bitcoin.address import BitcoinAddress

import logging
logger = logging.getLogger(__name__)

async def remove_bitcoin_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Remove bitcoin address to monitor from the database.
    Check whether sufficient parameters are supplied.
    If not - reply with error message
    If yes - Remove from database and confirm
    """
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")
    args = context.args
    if len(args) < 1:
        response = f"Not enough arguments provided"
        await reply(update, response)
    else:
        if BitcoinAddress.select().where(BitcoinAddress.bitcoin_address == args[0]).exists():
            to_remove = BitcoinAddress.select().where(BitcoinAddress.bitcoin_address == args[0])
            response = f"Deleted {to_remove.bitcoin_address} from watchlist."
            to_remove.delete_instance()
            await reply(update, response)
        else:
            response = f"{to_remove.bitcoin_address} not on watchlist."
            await reply(update, response)