from telegram import Update
from telegram.ext import ContextTypes
from utils import reply
from models.bitcoin.address import BitcoinAddress

import logging
logger = logging.getLogger(__name__)

async def add_bitcoin_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Add a bitcoin address to monitor.
    Check whether sufficient parameters were supplied to the command
    If no - reply with error message
    If yes - add to database and monitor
    """
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")
    args = context.args
    if len(args) < 1:
        response = f"Not enough arguments provided"
        await reply(update, response)
    else:
        if BitcoinAddress.select().where(BitcoinAddress.bitcoin_address == args[0]).exists():
            response = f"Can't add duplicate bitcoin address"
            await reply(update, response)
        else:
            BitcoinAddress.create(
                bitcoin_address = args[0]
            )
            response =f"Monitoring {args[0]}"
            await reply(update, response)