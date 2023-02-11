from telegram import Update
from telegram.ext import ContextTypes
from utils import reply
from models.feeds.feed import Feed
from models.bitcoin.address import BitcoinAddress

import logging
logger = logging.getLogger(__name__)

async def list_bitcoin_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")

    addresses = BitcoinAddress.select()
    if len(addresses) < 1:
        response = f"No addresses on watchlist"
        await reply(update, response)
        return

    response = f"*Watchlist:*\n"
    for address in addresses: 
        response += f"{address.bitcoin_address}"

    await reply(update, response)