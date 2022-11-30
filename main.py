#!/usr/bin/env python

import logging
import os

from telegram import __version__ as TG_VER

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

from telegram.ext import Application, CommandHandler
from commands.start import start

from models.base_model import db
from models.feed import Feed
from models.entry import FeedEntry

from commands.feeds.list_feeds import list_feeds as list
from commands.feeds.add_feed import add_feed as add
from commands.feeds.remove_feed import remove_feed as remove
from commands.feeds.edit_feed import edit_feed as edit

from jobs.rss_monitor import rss_monitor

#Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger()

db.create_tables([Feed, FeedEntry])

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", None)
    if token is None:
        raise RuntimeError(
            f"No TELEGRAM_BOT_TOKEN specified"
        )
    application = Application.builder().token(token).build()

    #Add handlers

    #RSS
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler(["list_feeds", "lf"], list))
    application.add_handler(CommandHandler(["remove_feed", "rf"], remove))
    application.add_handler(CommandHandler(["edit_feed", "ef"], edit))
    application.add_handler(CommandHandler(["add_feed", "af"], add))  


    # Jobs
    job_queue = application.job_queue

    job_queue.run_repeating(rss_monitor, int(os.getenv("RSS_INTERVAL", 90)), name='rss-monitor')  

    application.run_polling()

if __name__ == "__main__":
    main()