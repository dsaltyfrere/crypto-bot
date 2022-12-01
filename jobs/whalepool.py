import requests
import time
import logging
import os

from models.whalepool.symbol import WhalepoolTransactionSymbol
from models.whalepool.transaction import WhalepoolTransaction
from models.whalepool.transaction_type import WhalepoolTransactionType


WHALEPOOL_BASE_URL="https://api.whale-alert.io/v1/transactions"


logger = logging.getLogger(__name__)

async def whalepool_alert(context):
    timestamp = str(int((time.time() - 3500000 // 1000)))
    url = f'{WHALEPOOL_BASE_URL}?api_key={os.getenv("WHALEPOOL_API_KEY", None)}&min_value={os.getenv("WHALEPOOL_MIN_VALUE", "40000000")}&start={timestamp}'
    response = requests.get(url) 
    if response.status_code != 200:
        logger.error(f'Whalepool API appears down, response.status_code == {response.status_code}')
        return
    
    json = response.json()
    transactions = json.get('transactions')
    if transactions is None:
        logger.error("transactions object was None.")
        return
    
    for transaction in transactions:
        if WhalepoolTransactionType.select().where(WhalepoolTransactionType.transaction_type == transaction['transaction_type']).exists():
            if WhalepoolTransactionSymbol.select().where(WhalepoolTransactionSymbol.symbol == transaction["symbol"]).exists():
                if WhalepoolTransaction.select().where(WhalepoolTransaction.id == transaction["id"]).exists() is False:
                    trans = {
                        "id": transaction["id"],
                        "symbol": transaction["symbol"].upper(),
                        "type": transaction["transaction_type"],
                        "blockchain": transaction["blockchain"],
                        "amount": transaction["amount"],
                        "amount_usd": transaction["amount_usd"],
                        "hash": transaction["hash"]
                    }
                    emoji = "🔄"
                    action = "transferred"
                    if "owner" in transaction["from"].keys():
                        f = f"{transaction['from']['owner'].title()}"
                    else:
                        f = "unknown".title()
                    if "owner" in transaction["to"].keys():
                        t = f'{transaction["to"]["owner"].title()}'
                    else:
                        t = "unknown".title()
                    tail = f' from {f} to {t}'
                    trans["from_owner"] = f
                    trans["to_owner"] = t
                    if transaction["transaction_type"] == "mint":
                        emoji = "💵"
                        action = "minted"
                        tail = f' at {t}'
                    elif transaction["transaction_type"] == "burn":
                        emoji = "🔥"
                        action = "burned"
                        tail = f' at {f}'
                    amount = '{:,.2f}'.format(transaction["amount"]).replace('.', '\.')
                    amount_usd = '{:,.2f}'.format(transaction["amount_usd"]).replace('.', '\.')
                    message = f"{emoji} {amount.split('.')[0]} \# {transaction['symbol'].upper()} \({amount_usd.split('.')[0]} USD\) {action} {tail} [—link](https://whale-alert.io/transaction/{transaction['blockchain']}/{transaction['hash']})"
                    logger.info(message)
                    WhalepoolTransaction.create(
                        id = trans["id"],
                        symbol = trans["symbol"],
                        type = trans["type"],
                        blockchain = trans["blockchain"],
                        amount = trans["amount"],
                        amount_usd = trans["amount_usd"],
                        hash = trans["hash"],
                        from_owner = trans["from_owner"],
                        to_owner = trans["to_owner"]
                    )
                    await context.bot.send_message(
                        chat_id = os.getenv("CHAT_ID", None),
                        text = message
                    )