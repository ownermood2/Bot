import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot_handlers import (
    start, help_command, handle_file, get_file, create_folder,
    remove_folder, remove_file, handle_unknown_command, handle_error,
    button_callback, handle_command_with_file, list_files
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Changed to DEBUG level for more detailed logs
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

    # Add command handlers first to ensure they take precedence
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("get", get_file))
    application.add_handler(CommandHandler("list", list_files))
    application.add_handler(CommandHandler("addfolder", create_folder))
    application.add_handler(CommandHandler("removefolder", remove_folder))  # Keep for backward compatibility
    application.add_handler(CommandHandler("kickfolder", remove_folder))    # New command name
    application.add_handler(CommandHandler("add", handle_command_with_file))
    application.add_handler(CommandHandler("removefile", remove_file))      # Keep for backward compatibility
    application.add_handler(CommandHandler("kick", remove_file))            # New command name

    # Add callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    # Add file handler - only for messages containing files, not commands
    file_filter = (
        (filters.ATTACHMENT | filters.Document.ALL | filters.PHOTO | filters.VIDEO) 
        & ~filters.COMMAND  # Explicitly exclude any messages starting with /
        & filters.CaptionRegex(r'^\d+$')  # Only match captions that are just numbers
    )
    application.add_handler(MessageHandler(file_filter, handle_file))

    # Handle unknown commands - this should be last in command handling
    application.add_handler(MessageHandler(filters.COMMAND, handle_unknown_command))

    # Add error handler
    application.add_error_handler(handle_error)

    # Start the bot
    application.run_polling(allowed_updates=None)

if __name__ == '__main__':
    main()