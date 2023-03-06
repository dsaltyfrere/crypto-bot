import os
import logging

from moralis import evm_api
from models.ethereum.address import EthereumAddress
from models.ethereum.address_token_balance import EthereumAddressTokenBalance
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

api_key = os.getenv("MORALIS_API_KEY", None)


async def get_erc20_balance_by_wallet(context):
    addresses = EthereumAddress.select()
    params = {
        "address": "",
        "chain": os.getenv("ETHEREUM_CHAIN", None)
    }
    for address in addresses:
        logger.info(f"get_wallet_token_balance for {address.ethereum_address}")
        params["address"] = address.ethereum_address

        result = evm_api.token.get_wallet_token_balances(
            api_key = api_key,
            params=params
        )
        logger.debug(result)

        for token in result:
            """
            Iterate over all tokens received.
            Check if we already have a record for the token and the balance in the address is > 0
            If not, save it
            If we do, check whether incremented or decremented
            """
            if float(float(token['balance']) / float(pow(10, token['decimals']))) > 1:
                if EthereumAddressTokenBalance.select().where((EthereumAddressTokenBalance.ethereum_address == address.ethereum_address) & (EthereumAddressTokenBalance.ethereum_token_address == token['token_address'])).exists() is False:
                    logger.info(f"New token purchase found for {address.ethereum_address} | {token['token_address']} | {token['name']}")

                    try:
                        eatb = EthereumAddressTokenBalance(
                            ethereum_address = address.ethereum_address,
                            ethereum_token_address = token['token_address'],
                            ethereum_token_name = token['name'],
                            ethereum_token_symbol = token['symbol'],
                            ethereum_token_logo = token['logo'],
                            ethereum_token_thumbnail = token['thumbnail'],
                            ethereum_token_decimals = token['decimals'],
                            ethereum_token_balance = token['balance'],
                            ethereum_chain = os.getenv("ETHEREUM_CHAIN", None)
                        )
                        eatb.save()
                    except Exception as exc:
                        logger.error(exc)

                    balance = f"{float(token['balance']) / pow(10, token['decimals'])}"
                    response = f"❗️New token purchase found for <a href='https://etherscan.io/address/{address.ethereum_address}'>{address.ethereum_address}</a>\n{balance} <a href='https://etherscan.io/address/{token['token_address']}'>{token['name']}</a>"
                    keyboard = [
                        [
                            InlineKeyboardButton("Buy token", callback_data="1")
                        ]
                    ]
                    
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    await context.bot.send_message(
                        chat_id = os.getenv("CHAT_ID", None),
                        text = response,
                        parse_mode = ParseMode.HTML,
                        disable_web_page_preview=True,
                        reply_markup = reply_markup
                    )
                else:
                    # A record exists, fetch it
                    eatb = EthereumAddressTokenBalance.get((EthereumAddressTokenBalance.ethereum_address == address.ethereum_address) & (EthereumAddressTokenBalance.ethereum_token_address == token['token_address']))

                    # Has the amount increased?
                    if float(eatb.ethereum_token_balance) < float(token['balance']):
                        # Increased
                        previous_balance = eatb.ethereum_token_balance
                        logger.info(f"Previous balance: {eatb.ethereum_token_balance}")
                        new_balance = token['balance']
                        logger.info(f"New balance: {new_balance} | Division: {new_balance} / {eatb.ethereum_token_decimals}: {float(new_balance) / float(eatb.ethereum_token_decimals)}")
                        difference = (float(new_balance) - float(previous_balance)) / pow(10, eatb.ethereum_token_decimals)
                        total = f"{float(eatb.ethereum_token_balance) / pow(10, float(eatb.ethereum_token_decimals))}"
                        logger.info(f"Difference: {difference}")
                        eatb.ethereum_token_balance = token['balance']
                        response = f"<a href='https://etherscan.io/address/{address.ethereum_address}'>{address.ethereum_address}</a>\nhas 🔼 purchased {difference} {eatb.ethereum_token_name}\nNow holds a total of {total} {eatb.ethereum_token_name}"
                        eatb.save()

                        await context.bot.send_message(
                            chat_id = os.getenv("CHAT_ID", None),
                            text = response,
                            parse_mode = ParseMode.HTML,
                            disable_web_page_preview=True
                        )
                    elif float(eatb.ethereum_token_balance) > float(token['balance']):
                        # Decreased
                        previous_balance = eatb.ethereum_token_balance
                        logger.info(f"Previous balance: {eatb.ethereum_token_balance}")
                        new_balance = token['balance']
                        logger.info(f"New balance: {new_balance} | Division: {new_balance} / {eatb.ethereum_token_decimals}: {float(new_balance) / float(eatb.ethereum_token_decimals)}")
                        difference = (float(new_balance) - float(previous_balance)) / pow(10, eatb.ethereum_token_decimals)
                        total = f"{float(eatb.ethereum_token_balance) / pow(10, float(eatb.ethereum_token_decimals))}"
                        logger.info(f"Difference: {difference}")
                        eatb.ethereum_token_balance = token['balance']
                        response = f"<a href='https://etherscan.io/address/{address.ethereum_address}'>{address.ethereum_address}</a>\nhas 🔽 sold {difference} {eatb.ethereum_token_name}\nNow holds a total of {total} {eatb.ethereum_token_name}"
                        eatb.save()

                        await context.bot.send_message(
                            chat_id = os.getenv("CHAT_ID", None),
                            text = response,
                            parse_mode = ParseMode.HTML,
                            disable_web_page_preview=True
                        )

            else:
                logger.info(f"Balance of {token['name']} is less than 0: {float(float(token['balance'])) / float(pow(10, token['decimals']))}")


