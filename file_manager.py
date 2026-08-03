#!/usr/bin/python

# programer: CG July 2026

import shutil
import os

from datetime import datetime
from pathlib import Path
from typing import Optional

# A helper class to safely and easily manage common file operations.
class FileManager:
    def __init__(self, base_directory: Optional[str] = None):
        # Initializes the helper with an optional base directory.
        self.base_dir = Path(base_directory) if base_directory else Path.cwd()

    def _resolve_path(self, filename: str) -> Path:
        # Helper method to construct and ensure absolute paths.
        return (self.base_dir / filename).resolve()

    def read_text(self, filename: str) -> str:
        """Reads and returns the complete text content of a file."""
        file_path = self._resolve_path(filename)
        try:
            return file_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{filename}' was not found at {file_path}")

    def write_list(self, sep: str, file_name: str, list):
        # Creates or overwrites a file with the provided list
        file_path = self._resolve_path(file_name)
        file_path.parent.mkdir(parents = True, exist_ok = True)

        txt_file = None
        with open(file_name, "w") as txt_file:
            for row in list:
                # Convert each element to string, join with tabs, and add a newline
                line = sep.join(str(item) for item in row)
                txt_file.write(line + '\n')

        return txt_file
    
    def append_line(self, file_name: str, line: str) -> None:
        # Appends a single line of text with a newline character to a file.
        file_path = self._resolve_path(file_name)
        file_path.parent.mkdir(parents = True, exist_ok = True)
        with open(file_path, mode = "a", encoding = "utf-8") as file:
            file.write(f"{line}\n")

    def delete_file(self, file_name: str) -> bool:
        # Removes a file safely if it exists. Returns True if deleted.
        result = False
        file_path = self._resolve_path(file_name)
        if file_path.is_file():
            file_path.unlink()
            result = True
        return result
    
    def is_dir_empty(self, path):
        result = False
        if (os.path.exists(path) and os.path.isdir(path)):
            if (len(os.listdir(path)) == 0):
                result = True
        return result

    # Creates a backup copy with today's date/time
    # Parameter:
    #   source_path -      A character string containing the file path for backup creation.
    #   backup_directory - A character string containing the path where the backup file will be saved.
    # Return:
    #   result-            A character string containing the backup path

    # How to used it:
    # backup_directory = "/phodnet/drifter/gonzalez/programs/python/migration_for2py/save"
    # timestamped_backup = file_manager.create_timestamped_backup(file_name, backup_directory)
    # if (timestamped_backup):
    #     print("backup created:", timestamped_backup)
    # else:
    #     print(f"Error: {file_name} not found.")
    def create_timestamped_backup(self, source_path: str, backup_directory: Optional[str] = '') -> str:
        result = ''

        if (os.path.exists(source_path)):
            full_path = Path(source_path)
            parent = str(full_path.parent)
            if(self.is_dir_empty(parent)):
                parent = "" # = current directory

            if (not backup_directory):
                backup_directory = parent # = source directory
            # Check if the last character is not a slash
            if ((backup_directory) and (not backup_directory.endswith('/'))):
                backup_directory += "/"

            dir_path = Path(backup_directory)
            # Creates the backup_directory safely.
            # parent = true: Creates any missing parent directories in the path automatically.
            # exist_ok=True: Prevents from throwing a FileExistsError if the directory already exists.
            dir_path.mkdir(parents = True, exist_ok = True)

            if (os.path.exists(backup_directory) and os.path.isdir(backup_directory)):
                # Generate timestamp (Format: YYYYMMDD_HHMMSS)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            
                # Create unique backup name
                backup_path = f"{backup_directory}{full_path.stem}_{timestamp}{full_path.suffix}"
            
                # Copies and renames the file simultaneously
                shutil.copy(source_path, backup_path)
                result = backup_path

        return result


