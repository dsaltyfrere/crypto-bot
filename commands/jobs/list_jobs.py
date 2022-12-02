import logging
import os

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def list_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"list_job by {update.effective_user.username}")
    jobs = context.job_queue.jobs()
    response = '*Scheduled jobs:*\n'
    for job in jobs:
        response += f"\n*{job.name}*\nNext run at: *{job.next_t.strftime('%m/%d/%Y, %H:%M:%S')}* | Configured interval: *{job.trigger.interval}*"
        if job.name == "high_low":
            response += f" | Mode: {os.environ['HILO_MODE']}"
    
    await update.effective_message.reply_text(response)