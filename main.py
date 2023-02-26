#!/usr/bin/env python
import logging
import os
import pytz

from datetime import datetime
from telegram import __version__ as TG_VER
from telegram.ext import Application, CommandHandler, filters, AIORateLimiter, MessageHandler

from commands.start import start as start
from commands.fear import fear as fear

from commands.feeds.list_feeds import list_feeds as list
from commands.feeds.add_feed import add_feed as add
from commands.feeds.remove_feed import remove_feed as remove
from commands.feeds.edit_feed import edit_feed as edit, change_preview as preview

from commands.whalepool.symbol.add_whalepool_symbol import add_whalepool_symbol
from commands.whalepool.symbol.list_whalepool_symbol import list_whalepool_symbol
from commands.whalepool.symbol.remove_whalepool_symbol import remove_whalepool_symbol
from commands.whalepool.type.add_whalepool_transaction_type import add_whalepool_transaction_type
from commands.whalepool.type.list_whalepool_transaction_type import list_whalepool_transaction_type
from commands.whalepool.type.remove_whalepool_transaction_type import remove_whalepool_transaction_type

from commands.bitcoin.add_bitcoin_address import add_bitcoin_address
from commands.bitcoin.remove_bitcoin_address import remove_bitcoin_address
from commands.bitcoin.list_bitcoin_address import list_bitcoin_address

from commands.ethereum.add_ethereum_address import add_ethereum_address
from commands.ethereum.remove_ethereum_address import remove_ethereum_address
from commands.ethereum.list_ethereum_address import list_ethereum_address
from commands.ethereum.list_ethereum_address_erc20_balances import list_ethereum_address_erc20_balances

from commands.jobs.list_jobs import list_jobs
from commands.jobs.update_job import update_job

from models.base_model import db
from models.feeds.feed import Feed
from models.feeds.entry import FeedEntry

from models.bitcoin.block_fees import BitcoinBlockFees
from models.bitcoin.difficulty_adjustment import BitcoinDifficultyAdjustment
from models.bitcoin.pool import BitcoinPool
from models.bitcoin.pool_hashrate import BitcoinPoolHashrate

from models.bitcoin.lightning.lightning_network_stat import LightningNetworkStat

from models.bitcoin.address import BitcoinAddress
from models.bitcoin.address_utxo import BitcoinAddressUtxo
from models.bitcoin.address_utxo_status import BitcoinAddressUtxoStatus

from models.whalepool.symbol import WhalepoolTransactionSymbol
from models.whalepool.transaction import WhalepoolTransaction
from models.whalepool.transaction_type import WhalepoolTransactionType
from models.whalepool.high_low import HighLow
from models.whalepool.olhc import Olhc
from models.whalepool.ticker import Ticker


from models.ethereum.address import EthereumAddress
from models.ethereum.address_token_balance import EthereumAddressTokenBalance

from jobs.rss_monitor import rss_monitor
from jobs.whalepool import whalepool_alert
from jobs.olhc import olhc

from jobs.bitcoin.get_difficulty_adjustment import get_difficulty_adjustment
from jobs.bitcoin.get_block_fees import get_block_fees
from jobs.bitcoin.get_pools_hashrate import get_pools_hashrate
from jobs.bitcoin.get_pools import get_pools
from jobs.bitcoin.get_bitcoin_address_utxo import get_bitcoin_address_utxo
from jobs.bitcoin.lightning.get_network_stats import get_lightning_network_stats

from jobs.ethereum.get_erc20_balance_by_wallet import get_erc20_balance_by_wallet

from utils import error_handler


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

#Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger()

midnight_utc = datetime.now(pytz.utc).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(pytz.utc)

db.create_tables([
    Feed,
    FeedEntry,
    
    HighLow,
    Olhc,
    Ticker,

    WhalepoolTransactionType,
    WhalepoolTransaction,
    WhalepoolTransactionSymbol,

    BitcoinBlockFees,
    BitcoinPoolHashrate,
    BitcoinPool,
    BitcoinDifficultyAdjustment,

    LightningNetworkStat,

    EthereumAddress,
    EthereumAddressTokenBalance,

    BitcoinAddress,
    BitcoinAddressUtxo,
    BitcoinAddressUtxoStatus

])


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", None)
    if token is None:
        raise RuntimeError(
            f"No TELEGRAM_BOT_TOKEN specified"
        )

    application = Application.builder().token(token).rate_limiter(AIORateLimiter(overall_max_rate=20, overall_time_period=1, group_max_rate=15, group_time_period=60, max_retries=1)).build()
    filter = filters.User(username='phyrxia')

    #Add handlers
    application.add_handler(CommandHandler(["start", "help"], start, filters=filter))
    application.add_handler(CommandHandler(["fear", "f"], fear, filters=filter))
    #RSS
    application.add_handler(CommandHandler(["list_feeds", "lf"], list, filters=filter))
    application.add_handler(CommandHandler(["remove_feed", "rf"], remove, filters=filter))
    application.add_handler(CommandHandler(["edit_feed", "ef"], edit, filters=filter))
    application.add_handler(CommandHandler(["add_feed", "af"], add, filters=filter))
    application.add_handler(CommandHandler(["set_feed_preview", "sfp"], preview, filters=filter))

    # Whalepool
    application.add_handler(CommandHandler(["add_whalepool_symbol", "aws"], add_whalepool_symbol, filters=filter))
    application.add_handler(CommandHandler(["list_whalepool_symbol", "lws"], list_whalepool_symbol, filters=filter))
    application.add_handler(CommandHandler(["remove_whalepool_symbol", "rws"], remove_whalepool_symbol, filters=filter))
    application.add_handler(CommandHandler(["add_whalepool_transaction_type", "awtt"], add_whalepool_transaction_type, filters=filter))
    application.add_handler(CommandHandler(["list_whalepool_transaction_type", "lwtt"], list_whalepool_transaction_type, filters=filter))
    application.add_handler(CommandHandler(["rem_whalepool_transaction_type", "rwtt"], remove_whalepool_transaction_type, filters=filter))

    # Bitcoin
    application.add_handler(CommandHandler(["add_bitcoin_address", "aba"], add_bitcoin_address, filters=filter))
    application.add_handler(CommandHandler(["list_bitcoin_address", "lba"], list_bitcoin_address, filters=filter))
    application.add_handler(CommandHandler(["remove_bitcoin_address", "rba"], remove_bitcoin_address, filters=filter))

    # Ethereum
    application.add_handler(CommandHandler(["add_ethereum_address", "aea"], add_ethereum_address, filters=filter))
    application.add_handler(CommandHandler(["list_ethereum_address", "lea"], list_ethereum_address, filters=filter))
    application.add_handler(CommandHandler(["remove_ethereum_address", "rea"], remove_ethereum_address, filters=filter))

    application.add_handler(CommandHandler(["list_erc20_balances", "lerc20b"], list_ethereum_address_erc20_balances, filters=filter))


    # Jobs
    application.add_handler(CommandHandler(["list_jobs", "lj"], list_jobs, filters=filter))
    application.add_handler(CommandHandler(["update_job", "uj"], update_job, filters=filter))


    # Error handler
    application.add_error_handler(error_handler)

    # Job queue
    job_queue = application.job_queue

    # Run always
    job_queue.run_repeating(rss_monitor, int(os.getenv("RSS_INTERVAL", 90)), name='rss-monitor')
    job_queue.run_repeating(whalepool_alert, int(os.getenv("WHALEPOOL_DELAY", 90)), name="whalepool-alert")
    job_queue.run_repeating(olhc, int(os.getenv("HILO_DELAY", 90)), name='olhc')
    job_queue.run_repeating(get_difficulty_adjustment, 60*60, name='bitcoin-difficulty-adjustment')
    job_queue.run_repeating(get_bitcoin_address_utxo, 60, name='bitcoin-address-utxo')

    job_queue.run_repeating(get_erc20_balance_by_wallet, 180, name='ethereum-address-monitor')

    # Run monthly
    job_queue.run_monthly(get_pools, midnight_utc, day=1)
    job_queue.run_monthly(get_pools_hashrate, midnight_utc, day=1)
    
    # Run daily
    job_queue.run_daily(get_block_fees, midnight_utc, days=(0,))
    job_queue.run_daily(get_difficulty_adjustment, midnight_utc, days=(0,1,2,3,4,5,6))
    job_queue.run_daily(get_lightning_network_stats, midnight_utc, days=(0,1,2,3,4,5,6))
    
    application.run_polling()

if __name__ == "__main__":
    main()