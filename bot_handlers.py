import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from storage_manager import StorageManager
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE

logger = logging.getLogger(__name__)
storage = StorageManager()

def sanitize_folder_name(folder_name: str) -> str:
    """Sanitize folder name to prevent path traversal."""
    # Remove any path separators and spaces
    return "".join(c for c in folder_name if c.isalnum() or c in "-_")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"🤖 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗖𝗟𝗔𝗧 𝗖𝗹𝗼𝘂𝗱 𝗕𝗼𝘁!\n\n"
        "📚 Your Ultimate Study Storage\n"
        "➜ Store & manage PDFs, videos, images\n"
        "➜ Instant search & organized folders\n"
        "➜ Fast sharing & AI-powered management\n\n"
        "🚀 𝗪𝗵𝘆 𝗖𝗟𝗔𝗧 𝗖𝗹𝗼𝘂𝗱 𝗕𝗼𝘁?\n"
        "✅ 𝟮𝟰/𝟳 𝗔𝗰𝗰𝗲𝘀𝘀 | ✅ 𝗟𝗶𝗴𝗵𝘁𝗻𝗶𝗻𝗴-𝗙𝗮𝘀𝘁 𝗦𝗲𝗮𝗿𝗰𝗵\n"
        "✅ 𝗪𝗲𝗹𝗹-𝗢𝗿𝗴𝗮𝗻𝗶𝘇𝗲𝗱 | ✅ 𝗨𝘀𝗲𝗿-𝗙𝗿𝗶𝗲𝗻𝗱𝗹𝘆\n\n"
        "💡 𝗧𝗶𝗽: 𝗨𝘀𝗲 /[get folder name] [file name/all] to fetch related materials instantly!\n\n"
        "📌 Join All ➤ <a href='https://t.me/addlist/PyjyuGNvTnplMWZl'>𝗙𝗼𝗹𝗱𝗲𝗿 IIı 𝗖𝗩 ıII</a>\n"
        "🔹 Powered by: @CLAT_Vision | @Quiz_CV | @Conference_CV\n\n"
        "💡𝗙𝗼𝗿 𝗺𝗼𝗿𝗲 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻, 𝘁𝘆𝗽𝗲 /help"
    )

def get_folder_keyboard():
    """Create an inline keyboard with folder buttons."""
    folders = [
        "GK-CA (1-Y) STATIC",
        "GMB New (2025)",
        "@CLAT_Vision Material",
        "Case Laws & Judgments",
        "CLAT Notification & Updates",
        "English Language",
        "Extra Resources",
        "Group Study & Discussion Notes",
        "Legal Maxims & Terms",
        "Legal Reasoning",
        "Logical Reasoning",
        "Mock Tests",
        "NLU Information",
        "Notes & Summaries",
        "Quants (Maths)",
        "Syllabus & Strategy",
        "Time Management & Study Planner",
        "Video Lectures & PDFs"
    ]

    keyboard = []
    for folder in folders:
        keyboard.append([InlineKeyboardButton(f"📁 {folder}", callback_data=f"folder_{folder}")])

    return InlineKeyboardMarkup(keyboard)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "📂 𝗙𝗶𝗹𝗲 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀\n\n"
        "✅ 𝗚𝗲𝘁 𝗙𝗶𝗹𝗲𝘀\n"
        "- /get <folder_name> <filename> – Fetch a specific file\n"
        "- /get <folder_name> all – List all files in a folder\n\n"
        "🛠 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 𝗖𝗼𝗺𝗺𝗻𝗱𝘀\n"
        "- /addfolder <folder_name> – Create a folder\n"
        "- /removefolder <folder_name> – Delete a folder\n"
        "- /addpdf – Upload a PDF (Send file with folder name in caption)\n"
        "- /removepdf <filename> – Delete a PDF\n\n"
        "💡 𝗧𝗶𝗽: Always mention the folder name in commands for quick access\n\n"
        "📁 Available Folders (Click to select):",
        reply_markup=get_folder_keyboard()
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()

    if query.data.startswith("folder_"):
        folder_name = query.data[7:]  # Remove 'folder_' prefix
        try:
            files = storage.list_files(folder_name)
            if files:
                files_list = "\n".join([f"📄 {file}" for file in files])
                await query.message.reply_text(
                    f"📂 𝗙𝗶𝗹𝗲𝘀 𝗶𝗻 '{folder_name}':\n\n{files_list}\n\n"
                    f"📊 Total Files: {len(files)}\n\n"
                    f"💡 𝗧𝗶𝗽: Use /get {folder_name} <filename> to download a file"
                )
            else:
                await query.message.reply_text(
                    f"📂 𝗙𝗼𝗹𝗱𝗲𝗿 '{folder_name}' 𝗶𝘀 𝗲𝗺𝗽𝘁𝘆\n\n"
                    f"💡 𝗧𝗶𝗽: You can upload files to this folder by sending them with the folder name in caption"
                )
        except Exception as e:
            logger.error(f"Error accessing folder '{folder_name}': {str(e)}", exc_info=True)
            await query.message.reply_text(
                f"❌ 𝗘𝗿𝗿𝗼𝗿: Could not access folder '{folder_name}'\n"
                f"💡 Please try again or contact support if the issue persists."
            )

async def create_folder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create a new folder."""
    if not context.args:
        await update.message.reply_text("Please specify a folder name: /addfolder <folder_name>")
        return

    folder_name = sanitize_folder_name(context.args[0])
    if not folder_name:
        await update.message.reply_text("Invalid folder name. Use only letters, numbers, hyphens and underscores.")
        return

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

    folder_name = sanitize_folder_name(update.message.caption.strip())
    if not folder_name:
        await update.message.reply_text("Invalid folder name. Use only letters, numbers, hyphens and underscores.")
        return

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

        # Check file size
        if hasattr(file, 'file_size') and file.file_size > MAX_FILE_SIZE:
            await update.message.reply_text(
                f"File too large! Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB"
            )
            return

        # Check file extension
        file_extension = ''
        if hasattr(file, 'file_name'):
            file_extension = os.path.splitext(file.file_name)[1].lower()
        elif update.message.photo:
            file_extension = '.jpg'
        elif update.message.video:
            file_extension = '.mp4'

        if file_extension not in ALLOWED_EXTENSIONS:
            await update.message.reply_text(
                f"Unsupported file type! Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
            return

        # Download and save the file
        file_obj = await context.bot.get_file(file.file_id)
        downloaded_file = await file_obj.download_as_bytearray()

        # Save the file using storage manager
        filename = f"{file.file_id}{file_extension}"
        storage.save_file(folder_name, filename, downloaded_file)

        await update.message.reply_text(
            f"File saved successfully in folder '{folder_name}' as '{filename}'"
        )
    except Exception as e:
        logger.error(f"Error handling file: {str(e)}", exc_info=True)
        await update.message.reply_text(f"Error saving file: {str(e)}")

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get a file or list files in a folder."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Please specify folder and filename: /get <folder_name> <filename/all>"
        )
        return

    folder_name = sanitize_folder_name(context.args[0])
    if not folder_name:
        await update.message.reply_text("Invalid folder name. Use only letters, numbers, hyphens and underscores.")
        return

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
        logger.error(f"Error retrieving file: {str(e)}", exc_info=True)
        await update.message.reply_text(f"Error retrieving file: {str(e)}")

async def remove_folder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove a folder and its contents."""
    if not context.args:
        await update.message.reply_text("Please specify a folder name: /removefolder <folder_name>")
        return

    folder_name = sanitize_folder_name(context.args[0])
    if not folder_name:
        await update.message.reply_text("Invalid folder name. Use only letters, numbers, hyphens and underscores.")
        return

    try:
        storage.delete_folder(folder_name)
        await update.message.reply_text(f"Folder '{folder_name}' and its contents deleted successfully!")
    except Exception as e:
        await update.message.reply_text(f"Error deleting folder: {str(e)}")

async def remove_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove a specific file from a folder."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Please specify folder and filename: /removepdf <folder_name> <filename>"
        )
        return

    folder_name = sanitize_folder_name(context.args[0])
    if not folder_name:
        await update.message.reply_text("Invalid folder name. Use only letters, numbers, hyphens and underscores.")
        return

    file_name = context.args[1]
    try:
        storage.delete_file(folder_name, file_name)
        await update.message.reply_text(f"File '{file_name}' deleted successfully from folder '{folder_name}'!")
    except Exception as e:
        await update.message.reply_text(f"Error deleting file: {str(e)}")


async def handle_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    await update.message.reply_text(
        "Sorry, I don't understand that command. Use /help to see available commands."
    )

async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}", exc_info=True)
    await update.message.reply_text(
        "Sorry, something went wrong. Please try again later."
    )