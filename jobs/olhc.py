import requests
import logging
import os

from models.whalepool.olhc import Olhc
from jobs.rss_monitor import headers

logger = logging.getLogger(__name__)

async def olhc(context):
    for ticker in ['btcusd', 'ethusd']:
        response = requests.get(f'https://www.bitstamp.com/api/v2/ticker/{ticker}', headers=headers)
        if response.status_code != 200:
            logger.error(response.status_code)
            return
        
        open = int(float(response.json()['open']))
        high = int(float(response.json()['high']))
        low = int(float(response.json()['low']))
        logger.info(f"{ticker} | open: {open} - low: {low} - high: {high}")

        # Check if there is a last record, if there is none, created it and continue
        if Olhc.select().where(Olhc.ticker == ticker).count() == 0:
            logger.info(f'No records in db for {ticker}, must be first time use.')
            Olhc.create(
                open = open,
                high = high,
                low = low,
                ticker = ticker
            )
            continue
        
        last = Olhc.select().where(Olhc.ticker == ticker).order_by(Olhc.id.desc()).get()
        logger.info(f"last: {last.to_string}")
        symbol = '฿' if ticker == 'btcusd' else 'Ξ'
        
        if open != last.open:
            last = Olhc.create(
                open = open,
                high = high,
                low = low,
                ticker=ticker
            )
        
        elif high > last.high:
            p ='{0:,}'.format(high)
            Olhc.create(
                open = open,
                high = high,
                low = low,
                ticker=ticker
            )
            if Olhc.select().where((Olhc.ticker == ticker) & (Olhc.high >= high)).exists() is False:
                message = f"new {symbol} all time high: ${p}"
                logger.info(message)
                await context.bot.send_message(
                    chat_id=os.getenv("CHAT_ID", None),
                    text = message
                )
                return
            message = f"new {symbol} daily high: ${p}"
            logger.info(message)
            await context.bot.send_message(
                chat_id=os.getenv("CHAT_ID", None),
                text = message
            )
            return
        elif low < last.low:
            p ='{0:,}'.format(low)
            message = f"new {symbol} daily low high: ${p}"
            logger.info(message)
            Olhc.create(
                open = open,
                high = high,
                low = low,
                ticker=ticker
            )
            await context.bot.send_message(
                chat_id=os.getenv("CHAT_ID", None),
                text = message
            )