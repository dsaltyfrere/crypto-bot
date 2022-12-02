import logging

from telegram import Update
from telegram.ext import ContextTypes
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

async def update_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"update_job by {update.effective_user.username}")
    try:
        context.args[0]
    except IndexError:
        message = 'No job name supplied.'
        await update.effective_message.reply_text(message)
        raise
    try:
        context.args[1]
    except IndexError:
        message = 'No interval supplied.'
        await update.effective_message.reply_text(message)
        raise
    if context.args[1].isnumeric() is False:
        message = 'No valid number supplied.'
        await update.effective_message.reply_text(message)
        return
    jobs = context.job_queue.jobs()
    for job in jobs:
        if job.name == context.args[0]:
            job.reschedule(IntervalTrigger(seconds=int(context.args[1])))
            message = f"Successfully rescheduled *{context.args[0]}* to *{context.args[1]}s*."
            await update.effective_message.reply_text(message)
            return