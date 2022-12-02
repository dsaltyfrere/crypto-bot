import requests
import logging
import os

from models.bitcoin.pool import BitcoinPool

logger = logging.getLogger(__name__)
BASE_URL = "https://mempool.space/api/v1"

async def get_pools(context):
    logger.info(f"Fetching bitcoin difficulty adjustment")
    url = f"{BASE_URL}/mining/pools/1w"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            json_response = response.json()

            BitcoinPool.create(
                pool_id = json_response['poolId'],
                pool_name = json_response['name'],
                pool_link = json_response['link'],
                pool_block_count = json_response['blockCount'],
                pool_rank = json_response['rank'],
                pool_empty_blocks = json_response['emptyBlocks'],
                pool_slug = json_response['slug']
            )
        else:
            logger.error()
    except Exception as exc:
        logger.error(exc, exc_info=True)