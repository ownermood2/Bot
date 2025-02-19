import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from storage_manager import StorageManager
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE

logger = logging.getLogger(__name__)
storage = StorageManager()

# Developer usernames both with and without @ symbol
DEVELOPER_USERNAMES = ['CV_Owner', '@CV_Owner', 'Ace_Clat', '@Ace_Clat']

def is_developer(username: str) -> bool:
    """Check if the user is a developer."""
    if not username:
        logger.debug("No username provided for developer check")
        return False
    # Remove @ symbol if present for comparison
    clean_username = username.lstrip('@')
    is_dev = clean_username in [name.lstrip('@') for name in DEVELOPER_USERNAMES]
    logger.debug(f"Developer check for username '{username}' (cleaned: '{clean_username}'): {is_dev}")
    return is_dev

async def unauthorized_message(update: Update) -> None:
    """Send unauthorized access message."""
    logger.debug(f"Unauthorized access attempt by user: {update.effective_user.username}")
    await update.message.reply_text(
        "🔒 𝗗𝗘𝗩𝗘𝗟𝗢𝗣𝗘𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗢𝗡𝗟𝗬\n"
        "════════════════\n"
        "🚀 𝗥𝗲𝘀𝘁𝗿𝗶𝗰𝘁𝗲𝗱 𝗔𝗰𝗰𝗲𝘀𝘀\n"
        "🔹 This command is exclusively available to the Developer & His Wife to maintain quiz integrity & security.\n\n"
        "📌 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 & ଇ𝗻𝗾𝘂𝗶𝗿𝗶𝗲𝘀\n"
        "📩 DM: @CV_Owner & Admins ❤️\n"
        "💰 Paid Promotions: Up to 1K GC\n"
        "📝 Contribute: Share your quiz ideas\n"
        "⚠️ Report: Issues & bugs\n"
        "💡 Suggest: Improvements & enhancements\n\n"
        "✅ Thank you for your cooperation!\n"
        "════════════════"
    )

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
    row = []
    for i, folder in enumerate(folders):
        # Add number, folder emoji and arrow for better visibility
        button_text = f"{i+1}. 📁 {folder} →"
        row.append(InlineKeyboardButton(button_text, callback_data=f"folder_{folder}"))

        # Create rows with 2 buttons each for better layout
        if len(row) == 2 or i == len(folders) - 1:
            keyboard.append(row)
            row = []

    return InlineKeyboardMarkup(keyboard)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "📂 𝗙𝗶𝗹𝗲 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀\n\n"
        "✅ 𝗚𝗲𝘁 𝗙𝗶𝗹𝗲𝘀\n"
        "- /get <folder_number> <filename> – Fetch a specific file\n"
        "- /get <folder_number> all – List all files in a folder\n\n"
        "🛠 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 𝗖𝗼𝗺𝗺𝗻𝗱𝘀\n"
        "- /addfolder <folder_name> – Create a folder\n"
        "- /removefolder <folder_number> – Delete a folder\n"
        "- /addpdf <folder_number> – Upload a PDF (Send file with command)\n"
        "- /removepdf <folder_number> <filename> – Delete a PDF\n\n"
        "💡 𝗧𝗶𝗽: Use folder numbers for quick access (e.g., /addpdf 1 for first folder)\n\n"
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
                # Create a paginated list of files with numbers
                files_list = "\n".join([f"{i+1}. 📄 {file}" for i, file in enumerate(files)])
                await query.message.reply_text(
                    f"📂 𝗙𝗶𝗹𝗲𝘀 𝗶𝗻 '{folder_name}':\n\n{files_list}\n\n"
                    f"📊 Total Files: {len(files)}\n\n"
                    f"💡 𝗧𝗶𝗽: Use /get {folder_name} <filename> to download a file\n"
                    f"════════════════"
                )
            else:
                await query.message.reply_text(
                    f"📂 𝗙𝗼𝗹𝗱𝗲𝗿 '{folder_name}' 𝗶𝘀 𝗲𝗺𝗽𝘁𝘆\n\n"
                    f"💡 𝗧𝗶𝗽: You can upload files to this folder by sending them with the folder name in caption\n"
                    f"════════════════"
                )
        except Exception as e:
            logger.error(f"Error accessing folder '{folder_name}': {str(e)}", exc_info=True)
            await query.message.reply_text(
                f"❌ 𝗘𝗿𝗿𝗼𝗿: Could not access folder '{folder_name}'\n"
                f"💡 Please try again or contact support if the issue persists.\n"
                f"════════════════"
            )

async def create_folder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create a new folder."""
    user = update.effective_user
    logger.debug(f"Create folder attempt by user: {user.username}")

    if not is_developer(user.username):
        await unauthorized_message(update)
        return

    if not context.args:
        await update.message.reply_text("Please specify a folder name: /addfolder <folder_name>")
        return

    folder_name = sanitize_folder_name(context.args[0])
    if not folder_name:
        await update.message.reply_text("Invalid folder name. Use only letters, numbers, hyphens and underscores.")
        return

    try:
        storage.create_folder(folder_name)
        logger.debug(f"Folder '{folder_name}' created successfully by user: {user.username}")
        await update.message.reply_text(f"Folder '{folder_name}' created successfully!")
    except Exception as e:
        logger.error(f"Error creating folder: {str(e)}", exc_info=True)
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
    user = update.effective_user
    logger.debug(f"Remove folder attempt by user: {user.username}")

    if not is_developer(user.username):
        await unauthorized_message(update)
        return

    if not context.args:
        await update.message.reply_text("Please specify a folder name: /removefolder <folder_name>")
        return

    folder_name = sanitize_folder_name(context.args[0])
    if not folder_name:
        await update.message.reply_text("Invalid folder name. Use only letters, numbers, hyphens and underscores.")
        return

    try:
        storage.delete_folder(folder_name)
        logger.debug(f"Folder '{folder_name}' deleted successfully by user: {user.username}")
        await update.message.reply_text(f"Folder '{folder_name}' and its contents deleted successfully!")
    except Exception as e:
        logger.error(f"Error deleting folder: {str(e)}", exc_info=True)
        await update.message.reply_text(f"Error deleting folder: {str(e)}")

async def remove_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove a specific file from a folder."""
    user = update.effective_user
    logger.debug(f"Remove file attempt by user: {user.username}")

    if not is_developer(user.username):
        await unauthorized_message(update)
        return

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
        logger.debug(f"File '{file_name}' deleted successfully from folder '{folder_name}' by user: {user.username}")
        await update.message.reply_text(f"File '{file_name}' deleted successfully from folder '{folder_name}'!")
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}", exc_info=True)
        await update.message.reply_text(f"Error deleting file: {str(e)}")


async def handle_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    await update.message.reply_text(
        "Sorry, I don't understand that command. Use /help to see available commands."
    )

async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}", exc_info=True)

    error_message = "Sorry, something went wrong. Please try again later."

    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(error_message)
        elif update and update.callback_query:
            await update.callback_query.message.reply_text(error_message)
    except Exception as e:
        logger.error(f"Failed to send error message: {e}", exc_info=True)