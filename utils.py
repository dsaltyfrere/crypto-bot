from telegram import Update
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown

async def reply(update: Update, text: str) -> None:
    await update.effective_message.reply_text(
        text=text,
        parse_mode = ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True
    )
