from telegram import Update
from telegram.ext import ContextTypes
from utils import reply
from models.ethereum.address import EthereumAddress
from models.ethereum.address_token_balance import EthereumAddressTokenBalance
from moralis import evm_api

import logging
import os


logger = logging.getLogger(__name__)
api_key = os.getenv("MORALIS_API_KEY", None)

async def add_ethereum_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")
    args = context.args
    if len(args) < 1:
        response = f"Not enough arguments provided"
        await reply(update, response)
    else:
        if EthereumAddress.select().where(EthereumAddress.ethereum_address == args[0]).exists():
            response = f"Can't add duplicate ethereum address"
            await reply(update, response)
        else:
            alias = args[1] if len(args) > 1 else None
            ea = EthereumAddress.create(
                ethereum_address = args[0],
                ethereum_address_alias = alias
            )
            ea.save()
            params = {
                "address": f"{args[0]}",
                "chain": os.getenv("ETHEREUM_CHAIN", None)
            }

            result = evm_api.token.get_wallet_token_balances(
                api_key = api_key,
                params=params
            )
            for token in result:
                eatb = EthereumAddressTokenBalance(
                    ethereum_address = args[0],
                    ethereum_token_address = token['token_address'],
                    ethereum_token_name = token['name'],
                    ethereum_token_symbol = token['symbol'],
                    ethereum_token_logo = token['logo'],
                    ethereum_token_thumbnail = token['thumbnail'],
                    ethereum_token_decimals = token['decimals'],
                    ethereum_token_balance = token['balance']
                )
                eatb.save()
            response =f"Monitoring {args[0]}"
            if ea.ethereum_address_alias:
                response += f" ({ea.ethereum_address_alias})"
            await reply(update, response)