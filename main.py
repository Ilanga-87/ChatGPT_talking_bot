import os
from dotenv import load_dotenv
import logging

from telegram import __version__ as TG_VER
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import openai

from static_text import welcome_text, help_text, undefined_command_text

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

load_dotenv()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPEN_AI_API_KEY")


async def start(update, context):
    text = welcome_text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def handle_message(update, context):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=update.message.text,
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response["choices"][0]["text"])


async def helper(update, context):
    text = help_text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def undefined_commands(update, context):
    text = undefined_command_text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

start_handler = CommandHandler("start", start)
main_handler = MessageHandler(filters.TEXT, handle_message)
help_handler = CommandHandler("help", helper)
unknown_handler = MessageHandler(filters.COMMAND, undefined_commands)

app.add_handler(start_handler)
app.add_handler(main_handler)
app.add_handler(help_handler)
app.add_handler(unknown_handler)

app.run_polling()
