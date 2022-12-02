import datetime
import requests
import logging
import os

from models.bitcoin.block_fees import BitcoinBlockFees
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)
BASE_URL = "https://mempool.space/api/v1"

async def get_block_fees(context):
    logger.info(f"Fetching bitcoin block fees")
    url = f"{BASE_URL}/mining/blocks/fees/1w"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            json_response = response.json()

            bbf = BitcoinBlockFees.create(
                average_height = json_response['avgHeight'],
                timestamp = json_response['timestamp'],
                average_fees = json_response['avgFees']
            )

            bbf.save()
            response = f"<b>{datetime.datetime.fromtimestamp(bbf.timestamp / 1000)}</b>\n฿ average fees on height {bbf.average_height} : {round(bbf.average_fees, 2)}"
            await context.bot.send_message(
                chat_id = os.getenv("CHAT_ID", None),
                text = response,
                parse_mode = ParseMode.HTML
            )
        else:
            logger.error(f"Response.status_code for {url} was {response.status_code}")
    except Exception as exc:
        logger.error(exc, exc_info=True)