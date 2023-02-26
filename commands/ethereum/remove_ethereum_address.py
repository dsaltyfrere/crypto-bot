from telegram import Update
from telegram.ext import ContextTypes
from utils import reply
from models.ethereum.address import EthereumAddress

import logging
logger = logging.getLogger(__name__)

async def remove_ethereum_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")
    args = context.args
    if len(args) < 1:
        response = f"Not enough arguments provided"
        await reply(update, response)
    else:
        if EthereumAddress.select().where(EthereumAddress.ethereum_address == args[0]).exists():
            to_remove = EthereumAddress.select().where(EthereumAddress.ethereum_address == args[0])
            response = f"Deleted {to_remove.ethereum_address} from watchlist."
            to_remove.delete_instance()
            await reply(update, response)
        else:
            response = f"{to_remove.ethereum_address} not on watchlist."
            await reply(update, response)