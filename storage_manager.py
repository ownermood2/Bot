import os
import shutil
import logging
from typing import List, Optional, Dict, Tuple
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self, base_path: str = "storage"):
        """Initialize storage manager with given base path."""
        self.base_path = os.path.abspath(base_path)
        self._ensure_base_path_exists()
        logger.info(f"StorageManager initialized with base path: {self.base_path}")
        self.search_history = {}  # Store recent searches for recommendations

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

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity ratio between two strings."""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    def _find_similar_files(self, query: str, files: List[str], max_results: int = 3) -> List[str]:
        """Find files similar to the query string."""
        similarities = [(f, self._calculate_similarity(query, os.path.splitext(f)[0]))
                       for f in files]
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [f for f, _ in similarities[:max_results] if _ > 0.3]  # Minimum similarity threshold

    def search_files(self, query: str, folder_name: Optional[str] = None, 
                    page: int = 1, per_page: int = 5) -> Dict[str, any]:
        """Search for files across all folders or in a specific folder."""
        logger.debug(f"Searching for '{query}' in {folder_name or 'all folders'}")
        results = []
        total_count = 0
        similar_files = []

        try:
            if folder_name:
                # Search in specific folder
                folder_path = self._get_folder_path(folder_name)
                if os.path.exists(folder_path):
                    files = [f for f in os.listdir(folder_path) 
                            if os.path.isfile(os.path.join(folder_path, f))]

                    # Find exact and partial matches
                    matches = [f for f in files if query.lower() in f.lower()]
                    total_count = len(matches)

                    # Paginate results
                    start_idx = (page - 1) * per_page
                    end_idx = start_idx + per_page
                    results = matches[start_idx:end_idx]

                    # Find similar files
                    similar_files = self._find_similar_files(query, 
                                                           [f for f in files if f not in matches])
            else:
                # Search across all folders
                all_matches = []
                for folder in os.listdir(self.base_path):
                    folder_path = os.path.join(self.base_path, folder)
                    if os.path.isdir(folder_path):
                        files = [f for f in os.listdir(folder_path) 
                                if os.path.isfile(os.path.join(folder_path, f))]
                        matches = [(folder, f) for f in files if query.lower() in f.lower()]
                        all_matches.extend(matches)

                        # Find similar files in each folder
                        similar = self._find_similar_files(query, 
                                                         [f for f in files if (folder, f) not in matches])
                        similar_files.extend([(folder, f) for f in similar])

                total_count = len(all_matches)
                # Paginate results
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page
                results = all_matches[start_idx:end_idx]

            # Update search history for recommendations
            self.search_history[query] = {
                'timestamp': os.times(),
                'results': results,
                'similar': similar_files
            }

            return {
                'results': results,
                'similar_files': similar_files,
                'total_count': total_count,
                'current_page': page,
                'total_pages': (total_count + per_page - 1) // per_page,
                'has_more': end_idx < total_count if 'end_idx' in locals() else False
            }

        except Exception as e:
            logger.error(f"Error searching files: {str(e)}", exc_info=True)
            raise

    def get_file_path(self, folder_name: str, filename: str) -> str:
        """Get the full path of a file, supporting partial matches."""
        folder_path = self._get_folder_path(folder_name)
        logger.debug(f"Searching for file '{filename}' in folder: {folder_path}")

        if not os.path.exists(folder_path):
            logger.error(f"Folder does not exist: {folder_path}")
            raise FileNotFoundError(f"Folder '{folder_name}' does not exist")

        try:
            # List all files in the folder
            files = os.listdir(folder_path)
            logger.debug(f"Found {len(files)} files in folder")

            # First try exact match (with and without extension)
            if filename in files:
                file_path = os.path.join(folder_path, filename)
                logger.debug(f"Found exact match: {file_path}")
                return file_path

            # If no exact match, try partial match (case-insensitive)
            filename_lower = filename.lower()
            matching_files = [
                f for f in files 
                if (filename_lower in os.path.splitext(f.lower())[0]) and  # Match base name
                os.path.isfile(os.path.join(folder_path, f))
            ]

            if not matching_files:
                logger.error(f"No matching files found for '{filename}' in {folder_path}")
                raise FileNotFoundError(f"No files matching '{filename}' found")

            if len(matching_files) > 1:
                logger.debug(f"Multiple matches found for '{filename}': {matching_files}")
                matches_str = "\n".join(f"- {f}" for f in matching_files)
                raise ValueError(f"Multiple matching files found:\n{matches_str}\nPlease be more specific.")

            matched_file = matching_files[0]
            file_path = os.path.join(folder_path, matched_file)
            logger.debug(f"Found matching file: {file_path}")
            return file_path

        except Exception as e:
            if isinstance(e, (FileNotFoundError, ValueError)):
                raise
            logger.error(f"Error accessing files in {folder_path}: {str(e)}", exc_info=True)
            raise Exception(f"Error accessing files: {str(e)}")

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

    def list_files(self, folder_name: str) -> List[str]:
        """List all files in a folder."""
        folder_path = self._get_folder_path(folder_name)
        if not os.path.exists(folder_path):
            logger.error(f"Folder does not exist: {folder_path}")
            raise FileNotFoundError(f"Folder '{folder_name}' does not exist")

        try:
            files = [f for f in os.listdir(folder_path) 
                    if os.path.isfile(os.path.join(folder_path, f))]
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
            raise FileNotFoundError(f"Folder '{folder_name}' does not exist")

        try:
            shutil.rmtree(folder_path)
            logger.info(f"Successfully deleted folder: {folder_path}")
        except Exception as e:
            logger.error(f"Failed to delete folder {folder_path}: {str(e)}", exc_info=True)
            raise