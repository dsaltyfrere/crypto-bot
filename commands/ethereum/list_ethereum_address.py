from telegram import Update
from telegram.ext import ContextTypes
from utils import reply
from models.ethereum.address import EthereumAddress

import logging
logger = logging.getLogger(__name__)

async def list_ethereum_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")

    addresses = EthereumAddress.select()
    if len(addresses) < 1:
        response = f"No addresses on watchlist"
        await reply(update, response)
        return

    response = f"*Ethereum Watchlist:*\n"
    for address in addresses: 
        response += f"{address.ethereum_address}"

    await reply(update, response)