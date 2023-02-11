import datetime
import requests
import logging
import os

from models.bitcoin.address_utxo_status import BitcoinAddressUtxoStatus
from models.bitcoin.address_utxo import BitcoinAddressUtxo
from models.bitcoin.block_fees import BitcoinBlockFees
from models.bitcoin.address import BitcoinAddress
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)
BASE_URL = "https://mempool.space/api/"

async def get_bitcoin_address_utxo(context):
    logger.info(f"Fetching bitcoin address utxo's")

    bitcoin_addresses = BitcoinAddress.select()
    if len(bitcoin_addresses) < 1:
        logger.info(f"No bitcoin addressses defined")
        return
    for address in bitcoin_addresses:

        url = f"{BASE_URL}/addresss/{address.bitcoin_address}/utxo"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                json_response = response.json()

                for obj in json_response:
                    if not BitcoinAddressUtxo.select().where(BitcoinAddressUtxo.transaction_id == obj['txid']).exists():
                        status = obj['status']
                        bitcoin_address_utxo_status = BitcoinAddressUtxoStatus.create(
                            confirmed = status['confirmed'] ,
                            block_height = status['block_height'],
                            block_hash = status['block_hash'],
                            block_time = status['block_time']
                        )
                        bitcoin_address_utxo_status.save()
                        bitcoin_address_utxo = BitcoinAddressUtxo.create(
                            transaction_id = obj['txid'],
                            v_out = obj['vout'],
                            value = obj['value'],
                            status = bitcoin_address_utxo_status.id
                        )

                        bitcoin_address_utxo.save()
                        response = f"<b>New utxo found:</b>\n{bitcoin_address_utxo.transaction_id}"

                        await context.bot.send_message(
                            chat_id = os.getenv("CHAT_ID", None),
                            text = response,
                            parse_mode = ParseMode.HTML
                        )
            else:
                logger.error(f"Response.status_code for {url} was {response.status_code}")
        except Exception as exc:
            logger.error(exc, exc_info=True)