import requests
import logging
import os

from models.bitcoin.lightning.lightning_network_stat import LightningNetworkStat

logger = logging.getLogger(__name__)
BASE_URL = "https://mempool.space/api/v1"

async def get_lightning_network_stats(context):
    try:
        url = f"{BASE_URL}/lightning/statistics/24h"
        response = requests.get(url)

        if response.status_code == 200:
            json_response = response.json()

            LightningNetworkStat.create(
                stat_id = json_response['id'],
                added = json_response['added'],
                channel_count = json_response['channel_count'],
                node_count = json_response['node_count'],
                total_capacity = json_response['total_capacity'],
                tor_nodes = json_response['tor_nodes'],
                clearnet_nodes = json_response['clearnet_nodes'],
                unannounced_nodes = json_response['unannounced_nodes'],
                average_capacity = json_response['avg_capacity'],
                average_fee_rate = json_response['avg_fee_rate'],
                average_base_fee_mtokens = json_response['avg_base_fee_mtokens'],
                median_capacity = json_response['med_capacity'],
                median_fee_rate = json_response['med_fee_rate'],
                median_base_fee_mtokens = json_response['med_base_fee_mtokens'],
                clearnet_tor_nodes = json_response['clearnet_tor_nodes']
            )
        else:
            logger.error(f"Response.status_code for {url} was {response.status_code}")

    except Exception as exc:
        logger.error(exc, exc_info=True)