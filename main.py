import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot_handlers import (
    start, help_command, handle_file, get_file, create_folder,
    handle_unknown_command, handle_error
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Get the token from environment variable
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("No token provided!")
        return

    # Create the Application and pass it your bot's token
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("get", get_file))
    application.add_handler(CommandHandler("mkdir", create_folder))
    
    # Add file handler
    application.add_handler(MessageHandler(
        filters.ATTACHMENT | filters.Document.ALL | filters.PHOTO | filters.VIDEO,
        handle_file
    ))

    # Handle unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, handle_unknown_command))

    # Add error handler
    application.add_error_handler(handle_error)

    # Start the bot
    application.run_polling(allowed_updates=Application.ALL_UPDATES)

if __name__ == '__main__':
    main()
