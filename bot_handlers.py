import logging
from telegram import Update
from telegram.ext import ContextTypes
from storage_manager import StorageManager
import os

logger = logging.getLogger(__name__)
storage = StorageManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\n"
        "Welcome to the File Storage Bot. Here are the available commands:\n"
        "/help - Show available commands\n"
        "/mkdir <folder_name> - Create a new folder\n"
        "/get <folder_name> <filename> - Get a specific file\n"
        "/get <folder_name> all - List all files in a folder\n"
        "\nTo upload a file, simply send it to me along with the folder name in the caption!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Available commands:\n"
        "/mkdir <folder_name> - Create a new folder\n"
        "/get <folder_name> <filename> - Get a specific file\n"
        "/get <folder_name> all - List all files in a folder\n"
        "\nTo upload a file, send it with the folder name in the caption."
    )

async def create_folder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create a new folder."""
    if not context.args:
        await update.message.reply_text("Please specify a folder name: /mkdir <folder_name>")
        return

    folder_name = context.args[0]
    try:
        storage.create_folder(folder_name)
        await update.message.reply_text(f"Folder '{folder_name}' created successfully!")
    except Exception as e:
        await update.message.reply_text(f"Error creating folder: {str(e)}")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming files."""
    if not update.message.caption:
        await update.message.reply_text(
            "Please provide a folder name in the caption when sending files."
        )
        return

    folder_name = update.message.caption.strip()
    
    try:
        # Get the file from the message
        if update.message.document:
            file = update.message.document
        elif update.message.photo:
            file = update.message.photo[-1]  # Get the highest quality photo
        elif update.message.video:
            file = update.message.video
        else:
            await update.message.reply_text("Unsupported file type!")
            return

        # Download and save the file
        file_obj = await context.bot.get_file(file.file_id)
        file_extension = os.path.splitext(file.file_name)[1] if hasattr(file, 'file_name') else ''
        
        if not file_extension and update.message.photo:
            file_extension = '.jpg'
        elif not file_extension and update.message.video:
            file_extension = '.mp4'

        downloaded_file = await file_obj.download_as_bytearray()
        
        # Save the file using storage manager
        filename = f"{file.file_id}{file_extension}"
        storage.save_file(folder_name, filename, downloaded_file)
        
        await update.message.reply_text(
            f"File saved successfully in folder '{folder_name}' as '{filename}'"
        )
    except Exception as e:
        await update.message.reply_text(f"Error saving file: {str(e)}")

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get a file or list files in a folder."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Please specify folder and filename: /get <folder_name> <filename/all>"
        )
        return

    folder_name = context.args[0]
    file_name = context.args[1]

    try:
        if file_name.lower() == 'all':
            # List all files in the folder
            files = storage.list_files(folder_name)
            if not files:
                await update.message.reply_text(f"No files found in folder '{folder_name}'")
                return
            
            files_list = "\n".join(files)
            await update.message.reply_text(
                f"Files in folder '{folder_name}':\n{files_list}"
            )
        else:
            # Get specific file
            file_path = storage.get_file_path(folder_name, file_name)
            with open(file_path, 'rb') as f:
                await update.message.reply_document(document=f)
    except Exception as e:
        await update.message.reply_text(f"Error retrieving file: {str(e)}")

async def handle_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    await update.message.reply_text(
        "Sorry, I don't understand that command. Use /help to see available commands."
    )

async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    await update.message.reply_text(
        "Sorry, something went wrong. Please try again later."
    )
