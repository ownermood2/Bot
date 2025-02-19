import os
import shutil
from typing import List

class StorageManager:
    def __init__(self, base_path: str = "storage"):
        self.base_path = base_path
        self._ensure_base_path_exists()

    def _ensure_base_path_exists(self) -> None:
        """Ensure the base storage directory exists."""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def _get_folder_path(self, folder_name: str) -> str:
        """Get the full path for a folder."""
        return os.path.join(self.base_path, folder_name)

    def create_folder(self, folder_name: str) -> None:
        """Create a new folder."""
        folder_path = self._get_folder_path(folder_name)
        if os.path.exists(folder_path):
            raise Exception("Folder already exists")
        os.makedirs(folder_path)

    def save_file(self, folder_name: str, filename: str, content: bytes) -> None:
        """Save a file to a folder."""
        folder_path = self._get_folder_path(folder_name)
        if not os.path.exists(folder_path):
            raise Exception("Folder does not exist")

        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'wb') as f:
            f.write(content)

    def get_file_path(self, folder_name: str, filename: str) -> str:
        """Get the full path of a file."""
        folder_path = self._get_folder_path(folder_name)
        file_path = os.path.join(folder_path, filename)
        
        if not os.path.exists(file_path):
            raise Exception("File does not exist")
        
        return file_path

    def list_files(self, folder_name: str) -> List[str]:
        """List all files in a folder."""
        folder_path = self._get_folder_path(folder_name)
        if not os.path.exists(folder_path):
            raise Exception("Folder does not exist")
        
        return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    def delete_file(self, folder_name: str, filename: str) -> None:
        """Delete a file from a folder."""
        file_path = self.get_file_path(folder_name, filename)
        os.remove(file_path)

    def delete_folder(self, folder_name: str) -> None:
        """Delete a folder and all its contents."""
        folder_path = self._get_folder_path(folder_name)
        if not os.path.exists(folder_path):
            raise Exception("Folder does not exist")
        
        shutil.rmtree(folder_path)
