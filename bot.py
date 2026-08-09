import os
import re
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PUBLIC_URL = os.environ.get("PUBLIC_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing.")

if not PUBLIC_URL:
    raise RuntimeError("PUBLIC_URL environment variable is missing.")

PUBLIC_URL = PUBLIC_URL.rstrip("/")


def is_terabox_url(text: str) -> bool:
    patterns = [
        r"terabox\.com",
        r"teraboxapp\.com",
        r"1024terabox\.com",
        r"teraboxlink\.com",
    ]

    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Send me a TeraBox share link.\n\n"
        "Example:\n"
        "https://terabox.com/...\n\n"
        "I can process links that you are authorized to access."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Help\n\n"
        "Send an authorized TeraBox share link and the bot will process it."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if not is_terabox_url(text):
        await update.message.reply_text(
            "❌ That doesn't look like a TeraBox link.\n\n"
            "Please send a TeraBox share URL."
        )
        return

    await update.message.reply_text(
        "🔗 TeraBox link received.\n\n"
        "⏳ Processing..."
    )

    # ---------------------------------------------------------
    # TeraBox extraction goes here.
    #
    # A legitimate TeraBox/API endpoint should be connected here.
    # We deliberately don't pretend that a direct stream URL can
    # simply be calculated from a TeraBox share URL.
    # ---------------------------------------------------------

    await update.message.reply_text(
        "⚠️ The Telegram bot is working, but the TeraBox extraction "
        "service has not been connected yet.\n\n"
        "The next step is to connect an authorized TeraBox/API "
        "endpoint that can return the file URL."
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.exception(
        "Telegram update caused an error:",
        exc_info=context.error,
    )


def main():
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    application.add_error_handler(error_handler)

    port = int(os.environ.get("PORT", "8080"))

    logging.info("Starting Telegram webhook...")
    logging.info("Public URL: %s", PUBLIC_URL)
    logging.info("Port: %s", port)

    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="telegram",
        webhook_url=f"{PUBLIC_URL}/telegram",
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
