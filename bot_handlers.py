import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from storage_manager import StorageManager
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, STORAGE_PATH

logger = logging.getLogger(__name__)

def sanitize_folder_name(folder_name: str) -> str:
    """Sanitize folder name to prevent path traversal."""
    # Remove any path separators and spaces, preserve more characters
    sanitized = "".join(c for c in folder_name if c.isalnum() or c in "-_@()")
    logger.debug(f"Sanitizing folder name: '{folder_name}' -> '{sanitized}'")
    return sanitized

# Initialize storage with the configured path
logger.info(f"Initializing StorageManager with path: {STORAGE_PATH}")
if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH, exist_ok=True)
    logger.info(f"Created storage base path: {STORAGE_PATH}")

storage = StorageManager(STORAGE_PATH)

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
    logger.info(f"Initializing predefined folders in {storage.base_path}")

    # Verify base path exists
    if not os.path.exists(storage.base_path):
        os.makedirs(storage.base_path, exist_ok=True)
        logger.info(f"Created base storage directory: {storage.base_path}")

    # Create all predefined folders
    for folder in PREDEFINED_FOLDERS:
        try:
            sanitized_folder = sanitize_folder_name(folder)
            folder_path = os.path.join(storage.base_path, sanitized_folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
                logger.info(f"Created folder: {folder_path}")
            else:
                logger.info(f"Folder already exists: {folder_path}")

            # Debug: List contents to verify
            if os.path.exists(folder_path):
                logger.debug(f"Verified folder exists at: {folder_path}")
                logger.debug(f"Folder contents: {os.listdir(folder_path)}")
        except Exception as e:
            logger.error(f"Error creating folder {folder}: {str(e)}", exc_info=True)
            raise

# Add debug logging after initialization
logger.info("Starting folder initialization...")
initialize_folders()
logger.info("Folder initialization complete")
logger.debug(f"All folders in storage: {os.listdir(STORAGE_PATH)}")

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "🤖 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗖𝗟𝗔𝗧 𝗖𝗹𝗼𝘂𝗱 𝗕𝗼𝘁!\n\n"
        "📚 𝗪𝗵𝗮𝘁 𝗧𝗵𝗶𝘀 𝗕𝗼𝘁 𝗖𝗮𝗻 𝗗𝗼:\n"
        "➜ ꜱᴛᴏʀᴇ & ᴍᴀɴᴀɢᴇ ᴘᴅꜰꜱ, ᴠɪᴅᴇᴏꜱ, ᴀɴᴅ ɪᴍᴀɢᴇꜱ\n"
        "➜ ɪɴꜱᴛᴀɴᴛ ꜱᴇᴀʀᴄʜ & ǫᴜɪᴄᴋ ꜰɪʟᴇ ʀᴇᴛʀɪᴇᴠᴀʟ\n"
        "➜ ᴏʀɢᴀɴɪᴢᴇᴅ ꜱᴜʙᴊᴇᴄᴛ-ᴡɪꜱᴇ ꜰᴏʟᴅᴇʀꜱ ꜰᴏʀ ᴇᴀꜱʏ ᴀᴄᴄᴇꜱꜱ\n"
        "➜ ꜰᴀꜱᴛ ꜱʜᴀʀɪɴɢ & ᴀɪ-ᴘᴏᴡᴇʀᴇᴅ ꜰɪʟᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ\n"
        "➜ ᴄᴏᴠᴇʀꜱ ᴄʟᴀᴛ | ᴍᴀʜᴄᴇᴛ | ᴄᴜᴇᴛ & ᴀʟʟ ʟᴀᴡ ᴇxᴀᴍꜱ\n\n"
        "💡 𝗧𝗶𝗽: 𝗛𝗼𝘄 𝘁𝗼 𝗨𝘀𝗲\n"
        "➜ 𝗨𝗦𝗘 /get <folder_number> <filename> ᴛᴏ ꜰᴇᴛᴄʜ ꜰɪʟᴇꜱ\n"
        "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /get 2 ᴄᴏɴꜱᴛɪᴛᴜᴛɪᴏɴ\n"
        "➜ 𝗘𝘅𝗽𝗹𝗼𝗿𝗲 /help ᴛᴏ ᴠɪᴇᴡ ᴀʟʟ ꜰᴏʟᴅᴇʀꜱ & ᴄᴏᴍᴍᴀɴᴅꜱ\n\n"
        "𝗙𝗼𝗿 𝗺𝗼𝗿𝗲 𝗱𝗲𝘁𝗮𝗶𝗹𝘀 ,𝗧𝘆𝗽𝗲 /help 🚀"
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
        "📂 𝗙𝗶𝗹𝗲 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁\n"
        "════════════════\n"
        "📥 𝗤𝘂𝗶𝗰𝗸 𝗙𝗲𝘁𝗰𝗵:\n"
        "➜ /get <ꜰᴏʟᴅᴇʀ_ɴᴜᴍʙᴇʀ> <ꜰɪʟᴇɴᴀᴍᴇ> – Fetch file\n"
        "➜ /get <ꜰᴏʟᴅᴇʀ_ɴᴜᴍʙᴇʀ> ᴀʟʟ – List files\n"
        "➜ /get <folder_number> <query> – Find file\n"
        "➜ /get <query> – Search across folders\n"
        "➜ /list <folder_number> – View folder files\n"
        "════════════════\n"
        "🛠 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:\n"
        "➜ /addfolder <folder_name> – Create a folder\n"
        "➜ /kickfolder <folder_number> – Delete a folder\n"
        "➜ /add <folder_number> – Add files to a folder\n"
        "➜ /kick <folder_number> <filename> – Delete a file\n"
        "➜ /share <filename> [telegram I'd] – Grant access\n"
        "➜ /lock <folder_number> – Restrict access\n"
        "════════════════\n"
        "📁 𝗩𝗶𝗲𝘄 𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗙𝗼𝗹𝗱𝗲𝗿𝘀:",
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
                # Create a numbered list of files with emoji
                files_list = "\n".join([f"{i+1}. 📄 {file}" for i, file in enumerate(files)])
                # Get folder number for the tip
                folder_num = PREDEFINED_FOLDERS.index(folder_name) + 1
                await query.message.reply_text(
                    f"📂 𝗙𝗶𝗹𝗲𝘀 𝗶𝗻 '{folder_name}':\n\n"
                    f"{files_list}\n\n"
                    f"📊 Total Files: {len(files)}\n\n"
                    f"💡 𝗧𝗶𝗽: Use /get {folder_num} <filename> to download a file\n"
                    f"════════════════"
                )
            else:
                await query.message.reply_text(
                    f"📂 𝗙𝗼𝗹𝗱𝗲𝗿 '{folder_name}' 𝗶𝘀 𝗲𝗺𝗽𝘁𝘆\n\n"
                    f"💡 𝗧𝗶𝗽: You can upload files to this folder by sending them with the folder number in caption\n"
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
            "🚫 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗶𝗹𝗲 𝗧𝘆𝗽𝗘\n"
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
        logger.debug(f"Received folder number: {folder_num + 1} (index: {folder_num})")

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
        logger.debug(f"Using folder name: {folder_name}")
        logger.debug(f"Sanitized to: {sanitized_folder}")

        # Debug: Check if folder exists and create if needed
        folder_path = os.path.join(storage.base_path, sanitized_folder)
        logger.debug(f"Full folder path: {folder_path}")
        if not os.path.exists(folder_path):
            logger.info(f"Creating missing folder: {folder_path}")
            os.makedirs(folder_path, exist_ok=True)

        # Verify folder was created
        if os.path.exists(folder_path):
            logger.debug(f"Verified folder exists at: {folder_path}")
            logger.debug(f"Folder contents: {os.listdir(folder_path)}")
        else:
            logger.error(f"Failed to create/verify folder: {folder_path}")
            raise Exception("Failed to create folder")

        # Get the file
        if update.message.document:
            file = update.message.document
            file_extension = os.path.splitext(file.file_name)[1].lower()
            logger.debug(f"Processing document with extension: {file_extension}")
        elif update.message.photo:
            file = update.message.photo[-1]  # Get the highest quality photo
            file_extension = '.jpg'
            logger.debug("Processing photo (jpg)")
        else:  # video
            file = update.message.video
            file_extension = '.mp4'
            logger.debug("Processing video (mp4)")

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
            logger.debug(f"Getting file from Telegram with ID: {file.file_id}")
            file_obj = await context.bot.get_file(file.file_id)
            if not file_obj:
                raise ValueError("Could not get file from Telegram")

            logger.debug("Downloading file content")
            downloaded_file = await file_obj.download_as_bytearray()
            if not downloaded_file:
                raise ValueError("Could not download file content")

            # Generate a unique filename using the file ID
            filename = f"{file.file_id}{file_extension}"
            logger.debug(f"Generated filename: {filename}")

            # Save file using storage manager
            logger.debug(f"Saving file to folder: {sanitized_folder}")
            storage.save_file(sanitized_folder, filename, downloaded_file)

            await update.message.reply_text(
                "✅ File saved successfully!\n"
                f"📂 Folder: {folder_name}\n"
                f"📄 Filename: {filename}\n"
                "════════════════"
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
            "📝 𝗛𝗼𝘄 𝘁𝗼 𝘂𝘀𝗲 /𝗴𝗲𝘁 𝗰𝗼𝗺𝗺𝗮𝗻𝗱:\n"
            "════════════════\n\n"
            "💡 Use: /get <folder_number> <filename/all>\n"
            "📌 Example: /get 3 document.pdf\n\n"
            "🔍 Use /help to see folder numbers\n"
            "════════════════"
        )
        return

    try:
        # Get folder number and validate
        folder_num = int(context.args[0]) - 1  # Convert to 0-based index
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
        file_name = " ".join(context.args[1:])  # Join all remaining arguments as filename

        if file_name.lower() == 'all':
            # List all files in the folder
            files = storage.list_files(sanitized_folder)
            if not files:
                await update.message.reply_text(
                    f"📂 𝗙𝗶𝗹𝗲𝘀 𝗶𝗻 '{folder_name}':\n\n"
                    "No files found.\n\n"
                    "════════════════"
                )
                return

            files_list = "\n".join([f"{i+1}. 📄 {file}" for i, file in enumerate(files)])
            await update.message.reply_text(
                f"📂 𝗙𝗶𝗹𝗲𝘀 𝗶𝗻 '{folder_name}':\n\n"
                f"{files_list}\n\n"
                f"📊 Total Files: {len(files)}\n\n"
                f"💡 𝗧𝗶𝗽: Use /get {folder_num + 1} <filename> to download a file\n"
                f"════════════════"
            )
        else:
            # Get specific file
            try:
                file_path = storage.get_file_path(sanitized_folder, file_name)
                with open(file_path, 'rb') as f:
                    await update.message.reply_document(document=f)
            except Exception as e:
                logger.error(f"Error retrieving file: {str(e)}", exc_info=True)
                await update.message.reply_text(
                    f"❌ Error retrieving file: {str(e)}\n"
                    f"🔄 Please try again or contact @CV_Owner for support\n"
                    f"════════════════"
                )

    except ValueError:
        await update.message.reply_text(
            "❌ Invalid folder number!\n"
            "💡 Please provide a valid folder number\n"
            "🔍 Use /help to see available folders\n"
            "════════════════"
        )
    except Exception as e:
        logger.error(f"Error in get_file: {str(e)}", exc_info=True)
        await update.message.reply_text(
            f"❌ Error processing request: {str(e)}\n"
            f"🔄 Please try again or contact @CV_Owner for support\n"
            f"════════════════"
        )

async def remove_folder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove a folder and its contents (kickfolder command)."""
    user = update.effective_user
    logger.debug(f"Remove folder attempt by user: {user.username}")

    if not is_developer(user.username):
        await unauthorized_message(update)
        return

    if not context.args:
        await update.message.reply_text(
            "📝 𝗛𝗼𝘄 𝘁𝗼 𝘂𝘀𝗲 /𝗸𝗶𝗰𝗸𝗳𝗼𝗹𝗱𝗲𝗿 𝗰𝗼𝗺𝗺𝗮𝗻𝗱:\n"
            "════════════════\n\n"
            "💡 Use: /kickfolder <folder_number>\n"
            "📌 Example: /kickfolder 3\n\n"
            "🔍 Use /help to see folder numbers\n"
            "════════════════"
        )
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
    """Remove a specific file from a folder (kick command)."""
    user = update.effective_user
    logger.debug(f"Remove file attempt by user: {user.username}")

    if not is_developer(user.username):
        await unauthorized_message(update)
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "📝 𝗛𝗼𝘄 𝘁𝗼 𝘂𝘀𝗲 /𝗸𝗶𝗰𝗸 𝗰𝗼𝗺𝗺𝗮𝗻𝗱:\n"
            "════════════════\n\n"
            "💡 Use: /kick <folder_number> <filename>\n"
            "📌 Example: /kick 3 document.pdf\n\n"
            "🔍 Use /help to see folder numbers\n"
            "════════════════"
        )
        return

    try:
        # Get folder number and validate
        folder_num = int(context.args[0]) - 1  # Convert to 0-based index
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
        file_name = " ".join(context.args[1:])  # Join all remaining arguments as filename

        try:
            storage.delete_file(sanitized_folder, file_name)

            # Get updated file list for summary
            files = storage.list_files(sanitized_folder)
            files_list = "\n".join([f"{i+1}. 📄 {file}" for i, file in enumerate(files)])

            await update.message.reply_text(
                f"📂 𝗙𝗶𝗹𝗲𝘀 𝗶𝗻 '{folder_name}':\n\n"
                f"{files_list}\n\n"
                f"📊 Total Files: {len(files)}\n\n"
                f"💡 𝗧𝗶𝗽: Use /get {folder_num + 1} <filename> to download a file\n"
                f"════════════════"
            )
            logger.debug(f"File '{file_name}' deleted successfully from folder '{sanitized_folder}' by user: {user.username}")

        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}", exc_info=True)
            await update.message.reply_text(
                f"❌ Error deleting file: {str(e)}\n"
                f"🔄 Please try again or contact @CV_Owner for support\n"
                f"════════════════"
            )

    except ValueError:
        await update.message.reply_text(
            "❌ Invalid folder number!\n"
            "💡 Please provide a valid folder number\n"
            "🔍 Use /help to see available folders\n"
            "════════════════"
        )
    except Exception as e:
        logger.error(f"Error in remove_file: {str(e)}", exc_info=True)
        await update.message.reply_text(
            f"❌ Error processing request: {str(e)}\n"
            f"🔄 Please try again or contact @CV_Owner for support\n"
            f"════════════════"
        )

async def handle_command_with_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /add command with file upload."""
    user = update.effective_user
    logger.debug(f"Handling /add command from user: {user.username}")

    if not is_developer(user.username):
        await unauthorized_message(update)
        return

    # Check if a reply to a file message exists
    if not update.message.reply_to_message or (
        not update.message.reply_to_message.document and
        not update.message.reply_to_message.photo and
        not update.message.reply_to_message.video
    ):
        await update.message.reply_text(
            "📤 𝗛𝗼𝘄 𝘁𝗼 𝘂𝘀𝗲 /𝗮𝗱𝗱 𝗰𝗼𝗺𝗺𝗮𝗻𝗱:\n"
            "════════════════\n\n"
            "1️⃣ 𝗥𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝗳𝗶𝗹𝗲 𝘄𝗶𝘁𝗵:\n"
            "/add <folder_number> [custom_filename]\n\n"
            "📌 𝗘𝘅𝗮𝗺𝗽𝗹𝗲𝘀:\n"
            "• /add 3 → Uses original filename\n"
            "• /add 3 my_notes.pdf → Uses custom name\n\n"
            "💡 𝗧𝗶𝗽𝘀:\n"
            "• PDF files keep original name if no custom name\n"
            "• Photos/videos need custom names\n"
            "════════════════"
        )
        return

    # Check for folder number
    if not context.args:
        await update.message.reply_text(
            "❌ 𝗠𝗶𝘀𝘀𝗶𝗻𝗴 𝗙𝗼𝗹𝗱𝗲𝗿 𝗡𝘂𝗺𝗯𝗲𝗿\n"
            "════════════════\n\n"
            "💡 Use: /add <folder_number> [custom_filename]\n"
            "🔍 Example: /add 3 my_notes.pdf\n"
            "════════════════"
        )
        return

    try:
        # Get folder number and validate
        folder_num = int(context.args[0]) - 1  # Convert to 0-based index
        logger.debug(f"Received folder number: {folder_num + 1}")

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
        logger.debug(f"Using folder: {folder_name} (sanitized: {sanitized_folder})")

        # Get the file
        file = None
        custom_filename = None
        original_filename = None
        file_extension = None

        if update.message.reply_to_message.document:
            file = update.message.reply_to_message.document
            original_filename = file.file_name
            file_extension = os.path.splitext(original_filename)[1].lower()
        elif update.message.reply_to_message.photo:
            file = update.message.reply_to_message.photo[-1]
            file_extension = '.jpg'
        else:  # video
            file = update.message.reply_to_message.video
            file_extension = '.mp4'

        # Get custom filename if provided
        if len(context.args) > 1:
            custom_filename = " ".join(context.args[1:])
            if not any(custom_filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
                custom_filename += file_extension
        elif original_filename:
            # For any file with original name, use it if no custom name provided
            custom_filename = original_filename
        else:
            # For files without original names (photos/videos), require a custom name
            await update.message.reply_text(
                "❌ 𝗠𝗶𝘀𝘀𝗶𝗻𝗴 𝗙𝗶𝗹𝗲𝗻𝗮𝗺𝗲\n"
                "════════════════\n\n"
                "💡 Files without names require a custom filename\n"
                "📄 Example: /add 3 my_image.jpg\n"
                "════════════════"
            )
            return

        # Save file and generate summary
        try:
            file_obj = await context.bot.getfile(file.file_id)
            downloaded_file = await file_obj.download_as_bytearray()
            storage.save_file(sanitized_folder, custom_filename, downloaded_file)

            # Get total files in folder for summary
            files = storage.list_files(sanitized_folder)
            files_list = "\n".join([f"{i+1}. 📄 {file}" for i, file in enumerate(files)])

            # Send summary with exact formatting
            await update.message.reply_text(
                f"📂 𝗙𝗶𝗹𝗲𝘀 𝗶𝗻 '{folder_name}':\n\n"
                f"{files_list}\n\n"
                f"📊 Total Files: {len(files)}\n\n"
                f"💡 𝗧𝗶𝗽: Use /get {folder_num + 1} <filename> to download a file\n"
                f"════════════════"
            )
            logger.debug(f"File '{custom_filename}' saved successfully to folder '{sanitized_folder}' by user: {user.username}")

        except Exception as e:
            logger.error(f"Error saving file: {str(e)}", exc_info=True)
            await update.message.reply_text(
                f"❌ Error saving file: {str(e)}\n"
                f"🔄 Please try again or contact @CV_Owner for support\n"
                f"════════════════"
            )

    except ValueError:
        await update.message.reply_text(
            "❌ Invalid folder number!\n"
            "💡 Please provide a valid folder number\n"
            "🔍 Use /help to see available folders\n"
            "════════════════"
        )
    except Exception as e:
        logger.error(f"Error in handle_command_with_file: {str(e)}", exc_info=True)
        await update.message.reply_text(
            f"❌ Error processing file: {str(e)}\n"
            f"🔄 Please try again or contact @CV_Owner for support\n"
            f"════════════════"
        )

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