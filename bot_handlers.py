import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from storage_manager import StorageManager
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE

logger = logging.getLogger(__name__)
storage = StorageManager()

# Initialize storage and predefined folders
PREDEFINED_FOLDERS = [
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

def initialize_folders():
    """Initialize all predefined folders."""
    for folder in PREDEFINED_FOLDERS:
        try:
            sanitized_folder = sanitize_folder_name(folder)
            if not os.path.exists(os.path.join(storage.base_path, sanitized_folder)):
                storage.create_folder(sanitized_folder)
                logger.debug(f"Created folder: {sanitized_folder}")
        except Exception as e:
            logger.error(f"Error creating folder {folder}: {str(e)}")

# Initialize folders when module loads
initialize_folders()

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
        "💡 𝗧𝗶𝗽: 𝗛𝗼𝘄 𝘁𝗼 𝗨𝘀𝗲\n"
        "1. Send files with a folder number in caption (e.g., '1' for first folder)\n"
        "2. Use /help to see all folders with their numbers\n"
        "3. Quick commands: /get 1 filename to download from folder 1\n\n"
        "📌 Join All ➤ <a href='https://t.me/addlist/PyjyuGNvTnplMWZl'>𝗙𝗼𝗹𝗱𝗲𝗿 IIı 𝗖𝗩 ıII</a>\n"
        "🔹 Powered by: @CLAT_Vision | @Quiz_CV | @Conference_CV\n\n"
        "💡𝗙𝗼𝗿 𝗺𝗼𝗿𝗲 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻, 𝘁𝘆𝗽𝗲 /help"
    )

async def get_folder_keyboard():
    """Create an inline keyboard with folder buttons in a two-column grid."""
    keyboard = []
    row = []
    for i, folder in enumerate(PREDEFINED_FOLDERS):
        sanitized_name = sanitize_folder_name(folder)
        # Add number, folder emoji and arrow for better visibility
        button_text = f"{i+1}. 📁 {folder} →"
        # Use sanitized name in callback data
        row.append(InlineKeyboardButton(button_text, callback_data=f"folder_{sanitized_name}"))

        # Create rows with 2 buttons each
        if len(row) == 2 or i == len(PREDEFINED_FOLDERS) - 1:
            keyboard.append(row)
            row = []

    return InlineKeyboardMarkup(keyboard)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    keyboard = await get_folder_keyboard()
    await update.message.reply_text(
        "📂 𝗙𝗶𝗹𝗲 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀\n"
        "════════════════\n\n"
        "📤 𝗧𝗼 𝘂𝗽𝗹𝗼𝗮𝗱 𝗳𝗶𝗹𝗲𝘀:\n"
        "1. Select your file (📎)\n"
        "2. Add folder number in caption (e.g., '3')\n"
        "3. Send the message\n\n"
        "📥 𝗧𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗳𝗶𝗹𝗲𝘀:\n"
        "- /get <folder_number> <filename>\n"
        "- /get <folder_number> all – List files\n\n"
        "🛠 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:\n"
        "- /addfolder <folder_name>\n"
        "- /removefolder <folder_number>\n"
        "- /add <folder_number>\n"
        "- /removefile <folder_number> <filename>\n\n"
        "📁 𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗙𝗼𝗹𝗱𝗲𝗿𝘀 (𝗖𝗹𝗶𝗰𝗸 𝘁𝗼 𝘃𝗶𝗲𝘄 𝗳𝗶𝗹𝗲𝘀):",
        reply_markup=keyboard
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
    user = update.effective_user
    logger.debug(f"File upload attempt by user: {user.username}")

    # First check if it's a valid file message
    if not update.message.document and not update.message.photo and not update.message.video:
        await update.message.reply_text(
            "🚫 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗶𝗹𝗲 𝗧𝘆𝗽𝗲\n"
            "════════════════\n\n"
            "💡 Please send a valid file:\n"
            "📄 Documents (PDF)\n"
            "🖼️ Images (JPG, PNG)\n"
            "🎥 Videos (MP4, AVI)\n"
            "════════════════"
        )
        return

    # Check for folder number in caption
    if not update.message.caption or not update.message.caption.strip().isdigit():
        await update.message.reply_text(
            "📝 𝗠𝗶𝘀𝘀𝗶𝗻𝗴 𝗙𝗼𝗹𝗱𝗲𝗿 𝗡𝘂𝗺𝗯𝗲𝗿\n"
            "════════════════\n\n"
            "💡 Please add a folder number in caption\n"
            "Example: Send file with '1' as caption\n\n"
            "🔍 Use /help to see folder numbers\n"
            "════════════════"
        )
        return

    try:
        # Get folder number and validate
        folder_num = int(update.message.caption.strip()) - 1  # Convert to 0-based index

        if folder_num < 0 or folder_num >= len(PREDEFINED_FOLDERS):
            await update.message.reply_text(
                "❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗼𝗹𝗱𝗲𝗿 𝗡𝘂𝗺𝗯𝗲𝗿\n"
                "════════════════\n\n"
                "💡 Please use a number between 1 and 18\n"
                "🔍 Use /help to see available folders\n"
                "════════════════"
            )
            return

        # Get folder name and sanitize it
        folder_name = PREDEFINED_FOLDERS[folder_num]
        sanitized_folder = sanitize_folder_name(folder_name)
        logger.debug(f"Using sanitized folder name: {sanitized_folder}")


        # Get the file
        if update.message.document:
            file = update.message.document
            file_extension = os.path.splitext(file.file_name)[1].lower()
        elif update.message.photo:
            file = update.message.photo[-1]  # Get the highest quality photo
            file_extension = '.jpg'
        else:  # video
            file = update.message.video
            file_extension = '.mp4'

        # Validate file size
        if hasattr(file, 'file_size') and file.file_size > MAX_FILE_SIZE:
            size_mb = MAX_FILE_SIZE / (1024 * 1024)
            await update.message.reply_text(
                f"❌ File too large!\n"
                f"💡 Maximum size allowed: {size_mb:.1f}MB\n"
                f"📏 Your file: {file.file_size / (1024*1024):.1f}MB\n"
                f"════════════════"
            )
            return

        # Check file extension
        if file_extension not in ALLOWED_EXTENSIONS:
            await update.message.reply_text(
                f"❌ Unsupported file type: {file_extension}\n"
                f"💡 Allowed types:\n"
                f"📄 Documents: {', '.join(ext for ext in ALLOWED_EXTENSIONS if ext.startswith('.p'))}\n"
                f"🖼️ Images: {', '.join(ext for ext in ALLOWED_EXTENSIONS if ext.startswith('.j') or ext.startswith('.png'))}\n"
                f"🎥 Videos: {', '.join(ext for ext in ALLOWED_EXTENSIONS if ext.startswith('.m') or ext.startswith('.avi'))}\n"
                f"════════════════"
            )
            return

        # Download and save file
        try:
            file_obj = await context.bot.get_file(file.file_id)
            if not file_obj:
                raise ValueError("Could not get file from Telegram")

            downloaded_file = await file_obj.download_as_bytearray()
            if not downloaded_file:
                raise ValueError("Could not download file content")

            # Generate a unique filename using the file ID
            filename = f"{file.file_id}{file_extension}"

            # Save file using storage manager
            storage.save_file(sanitized_folder, filename, downloaded_file)

            await update.message.reply_text(
                f"✅ File saved successfully!\n"
                f"📂 Folder: {sanitized_folder}\n"
                f"📄 Filename: {filename}\n"
                f"════════════════"
            )
            logger.debug(f"File '{filename}' saved successfully to folder '{sanitized_folder}' by user: {user.username}")

        except Exception as e:
            logger.error(f"Error downloading/saving file: {str(e)}", exc_info=True)
            await update.message.reply_text(
                f"❌ Error saving file: {str(e)}\n"
                f"🔄 Please try again or contact @CV_Owner for support\n"
                f"════════════════"
            )

    except ValueError as e:
        logger.error(f"Invalid folder number: {str(e)}", exc_info=True)
        await update.message.reply_text(
            "❌ Invalid folder number!\n"
            "💡 Please provide a valid folder number in the caption\n"
            "🔍 Use /help to see the list of folders with their numbers\n"
            "════════════════"
        )
    except Exception as e:
        logger.error(f"Error handling file: {str(e)}", exc_info=True)
        await update.message.reply_text(
            f"❌ Error processing file: {str(e)}\n"
            f"🔄 Please try again or contact @CV_Owner for support\n"
            f"════════════════"
        )

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
            "❌ Please specify folder number and filename:\n"
            "💡 Example: /removefile 1 example.pdf\n"
            "🔍 Use /help to see folder numbers\n"
            "════════════════"
        )
        return

    try:
        keyboard = await get_folder_keyboard()
        folder_num = int(context.args[0]) - 1  # Convert to 0-based index
        if folder_num < 0 or folder_num >= len(keyboard.inline_keyboard):
            await update.message.reply_text(
                "❌ Invalid folder number!\n"
                "💡 Please use a number between 1 and 18\n"
                "🔍 Use /help to see all available folders\n"
                "════════════════"
            )
            return

        # Get folder name from the keyboard buttons
        folder_name = keyboard.inline_keyboard[folder_num][0].callback_data[7:]
        folder_name = sanitize_folder_name(folder_name)
        file_name = context.args[1]

        try:
            storage.delete_file(folder_name, file_name)
            logger.debug(f"File '{file_name}' deleted successfully from folder '{folder_name}' by user: {user.username}")
            await update.message.reply_text(
                f"✅ File deleted successfully!\n"
                f"📂 Folder: {folder_name}\n"
                f"📄 Filename: {file_name}\n"
                f"════════════════"
            )
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}", exc_info=True)
            await update.message.reply_text(
                f"❌ Error deleting file: {str(e)}\n"
                f"🔄 Please try again or contact support\n"
                f"════════════════"
            )

    except ValueError:
        await update.message.reply_text(
            "❌ Invalid folder number!\n"
            "💡 Please use a number between 1 and 18\n"
            "🔍 Use /help to see all available folders\n"
            "════════════════"
        )
    except Exception as e:
        logger.error(f"Error in remove_file: {str(e)}", exc_info=True)
        await update.message.reply_text(
            f"❌ Error processing request: {str(e)}\n"
            f"🔄 Please try again or contact support\n"
            f"════════════════"
        )

async def handle_command_with_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show instructions for uploading files."""
    logger.debug(f"Handling /add command from user: {update.effective_user.username}")
    await update.message.reply_text(
        "📤 𝗛𝗼𝘄 𝘁𝗼 𝘂𝗽𝗹𝗼𝗮𝗱 𝗮 𝗳𝗶𝗹𝗲:\n"
        "════════════════\n\n"
        "1️⃣ 𝗦𝗲𝗹𝗲𝗰𝘁 𝘆𝗼𝘂𝗿 𝗳𝗶𝗹𝗲:\n"
        "   • Click 📎 (attachment)\n"
        "   • Choose your PDF/photo/video\n\n"
        "2️⃣ 𝗔𝗱𝗱 𝗳𝗼𝗹𝗱𝗲𝗿 𝗻𝘂𝗺𝗯𝗲𝗿:\n"
        "   • Type ONLY the number (e.g., '3')\n"
        "   • Add it in the caption field\n\n"
        "3️⃣ 𝗦𝗲𝗻𝗱 𝘁𝗵𝗲 𝗺𝗲𝘀𝘀𝗮𝗴𝗲\n\n"
        "💡 𝗘𝘅𝗮𝗺𝗽𝗹𝗲:\n"
        "• Select your file\n"
        "• Type '3' in caption to save in folder 3\n"
        "• Send\n\n"
        "🔍 Use /help to see all folder numbers\n"
        "════════════════"
    )
    logger.debug("Upload instructions sent successfully")


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