from telegram import Update
from telegram.ext import ContextTypes
from utils import reply
from models.ethereum.address import EthereumAddress
from models.ethereum.address_token_balance import EthereumAddressTokenBalance
from telegram.constants import ParseMode

import logging
logger = logging.getLogger(__name__)

async def list_ethereum_address_erc20_balances(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from {update.effective_user.username}: {update.effective_message.text}")

    addresses = EthereumAddress.select()
    if len(addresses) < 1:
        response = f"No addresses on watchlist"
        await reply(update, response)
        return


    for address in addresses:
        response = f"<a href='https://etherscan.io/address/{address.ethereum_address}'>{address.ethereum_address}</a>\n"
        erc20_balances = EthereumAddressTokenBalance.select().where(EthereumAddressTokenBalance.ethereum_address == address.ethereum_address)
        balances = f"There are {len(erc20_balances)} tokens in portfolio:"
        for erc20_balance in erc20_balances:
            html_link = f"<a href='https://etherscan.io/address/{erc20_balance.ethereum_token_address}'>{erc20_balance.ethereum_token_name}</a>"
            if erc20_balance.ethereum_token_balance is not None and erc20_balance.ethereum_token_decimals is not None:
                html_balance = "{:.2f}\n".format(float(erc20_balance.ethereum_token_balance) / erc20_balance.ethereum_token_decimals)
            else:
                html_balance = f"0\n"
            
            balances += f"{html_balance} {html_link}"
        to_send = response + balances
        logger.info(to_send)
        await update.effective_message.reply_text(
            to_send,
            parse_mode = ParseMode.HTML
        )

