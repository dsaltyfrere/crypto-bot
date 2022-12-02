import os
import traceback
import html
import logging
import json

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.error import Unauthorized, BadRequest
from telegram.helpers import escape_markdown


logger = logging.getLogger(__name__)


async def reply(update: Update, text: str) -> None:
    await update.effective_message.reply_text(
        text=text,
        parse_mode = ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:    
    developer_chat_id = os.getenv("DEVELOPER_CHAT_ID", None)
    if developer_chat_id is not None:
            
        """Log the error and send a telegram message to notify the developer."""
        # Log the error before we do anything else, so we can see it even if something breaks.
        logger.error(msg="Exception while handling an update:", exc_info=context.error)

        # traceback.format_exception returns the usual python message about an exception, but as a
        # list of strings rather than a single string, so we have to join them together.
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = ''.join(tb_list)

        # Build the message with some markup and additional information about what happened.
        # You might need to add some logic to deal with messages longer than the 4096 character limit.
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
            f'An exception was raised while handling an update\n'
            f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
            '</pre>\n\n'
            f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
            f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
            f'<pre>{html.escape(tb_string)}</pre>'
        )

        # Finally, send the message
        context.bot.send_message(chat_id=developer_chat_id, text=message, parse_mode=ParseMode.HTML)