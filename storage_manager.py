import os
import shutil
import logging
from typing import List

logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self, base_path: str = "storage"):
        """Initialize storage manager with given base path."""
        self.base_path = os.path.abspath(base_path)
        self._ensure_base_path_exists()
        logger.info(f"StorageManager initialized with base path: {self.base_path}")

    def _ensure_base_path_exists(self) -> None:
        """Ensure the base storage directory exists."""
        try:
            os.makedirs(self.base_path, exist_ok=True)
            logger.info(f"Ensured base storage directory exists: {self.base_path}")
        except Exception as e:
            logger.error(f"Failed to create base directory: {str(e)}", exc_info=True)
            raise

    def _get_folder_path(self, folder_name: str) -> str:
        """Get the full path for a folder."""
        folder_path = os.path.join(self.base_path, folder_name)
        logger.debug(f"Resolved folder path: {folder_path}")
        return folder_path

    def create_folder(self, folder_name: str) -> None:
        """Create a new folder."""
        folder_path = self._get_folder_path(folder_name)
        try:
            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"Created/verified folder: {folder_path}")
        except Exception as e:
            logger.error(f"Failed to create folder {folder_path}: {str(e)}", exc_info=True)
            raise

    def save_file(self, folder_name: str, filename: str, content: bytes) -> None:
        """Save a file to a folder."""
        folder_path = self._get_folder_path(folder_name)
        logger.debug(f"Attempting to save file {filename} to folder: {folder_path}")

        if not os.path.exists(folder_path):
            logger.error(f"Folder does not exist: {folder_path}")
            try:
                # Try to create the folder if it doesn't exist
                os.makedirs(folder_path, exist_ok=True)
                logger.info(f"Created missing folder: {folder_path}")
            except Exception as e:
                logger.error(f"Failed to create folder: {str(e)}", exc_info=True)
                raise Exception(f"Failed to create folder: {str(e)}")

        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'wb') as f:
                f.write(content)
            logger.info(f"Successfully saved file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to save file {file_path}: {str(e)}", exc_info=True)
            raise

    def get_file_path(self, folder_name: str, filename: str) -> str:
        """Get the full path of a file."""
        folder_path = self._get_folder_path(folder_name)
        file_path = os.path.join(folder_path, filename)

        if not os.path.exists(file_path):
            logger.error(f"File does not exist: {file_path}")
            raise Exception("File does not exist")

        logger.debug(f"Retrieved file path: {file_path}")
        return file_path

    def list_files(self, folder_name: str) -> List[str]:
        """List all files in a folder."""
        folder_path = self._get_folder_path(folder_name)
        if not os.path.exists(folder_path):
            logger.error(f"Folder does not exist: {folder_path}")
            raise Exception("Folder does not exist")

        try:
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            logger.debug(f"Listed {len(files)} files in folder: {folder_path}")
            return files
        except Exception as e:
            logger.error(f"Error listing files in {folder_path}: {str(e)}", exc_info=True)
            raise

    def delete_file(self, folder_name: str, filename: str) -> None:
        """Delete a file from a folder."""
        file_path = self.get_file_path(folder_name, filename)
        try:
            os.remove(file_path)
            logger.info(f"Successfully deleted file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {str(e)}", exc_info=True)
            raise

    def delete_folder(self, folder_name: str) -> None:
        """Delete a folder and all its contents."""
        folder_path = self._get_folder_path(folder_name)
        if not os.path.exists(folder_path):
            logger.error(f"Folder does not exist: {folder_path}")
            raise Exception("Folder does not exist")

        try:
            shutil.rmtree(folder_path)
            logger.info(f"Successfully deleted folder: {folder_path}")
        except Exception as e:
            logger.error(f"Failed to delete folder {folder_path}: {str(e)}", exc_info=True)
            raise