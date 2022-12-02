import requests
import logging
import os

from models.bitcoin.pool_hashrate import BitcoinPoolHashrate

logger = logging.getLogger(__name__)
BASE_URL = "https://mempool.space/api/v1"

async def get_pools_hashrate(context):
    logger.info(f"Fetching pools hashrate")
    url = f"{BASE_URL}/mining/hashrate/pools/1m"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            json_response = response.json()

            BitcoinPoolHashrate.create(
                timestamp = json_response['timestamp'],
                average_hashrate = json_response['avgHashrate'],
                share = json_response['share'],
                pool_name = json_response['poolName']
            )
            
        else:
            logger.error(f"Response.status_code for {url} was {response.status_code}")
    except Exception as exc:
        logger.error(exc, exc_info=True)