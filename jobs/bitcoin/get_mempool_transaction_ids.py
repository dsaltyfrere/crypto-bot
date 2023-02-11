import requests
import logging

from models.bitcoin.mempool_transaction_id import MempoolTransactionId

logger = logging.getLogger(__name__)
BASE_URL = "https://mempool.space/api/v1"

async def get_mempool_transaction_ids(context):
    logger.info(f"Fetching mempool transaction ids")
    url = f"{BASE_URL}/mempool/txids"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            json_response = response.json()

            for transaction in json_response:
                if MempoolTransactionId.get_or_none(MempoolTransactionId.mempool_transaction_id == transaction) is None:
                    mt_id = MempoolTransactionId.create(
                        mempool_transaction_id = transaction
                    )

                    mt_id.save()
        else:
            logger.error(f"Response.status_code for {url} was {response.status_code}")

    except Exception as exc:
        logger.error(exc, exc_info=True)