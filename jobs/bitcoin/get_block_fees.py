import requests
import logging
import os

from models.bitcoin.block_fees import BitcoinBlockFees

logger = logging.getLogger(__name__)
BASE_URL = "https://mempool.space/api/v1"

async def get_block_fees(context):
    logger.info(f"Fetching bitcoin block fees")
    url = f"{BASE_URL}/mining/blocks/fees/1w"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            json_response = response.json()

            BitcoinBlockFees.create(
                average_height = json_response['avgHeight'],
                timestamp = json_response['timestamp'],
                average_fees = json_response['avgFees']
            )
        else:
            logger.error(f"Response.status_code for {url} was {response.status_code}")
    except Exception as exc:
        logger.error(exc, exc_info=True)