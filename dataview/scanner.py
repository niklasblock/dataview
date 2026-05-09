from pathlib import Path
from datetime import datetime

class Scanner: 

    def __init__(self, path: Path) -> None: 
        """Initialize Scanner with the path from the drive.
    
        Args:
            path: Path to the drive to analyze
        """
        self.path = path 

    def scan(self) -> list[dict[str, any]]:
        """Scan the path and refurn for each files the data in a list"""
        # Alle Dateien rekursiv holen
        scans = []
        for file in self.path.rglob("*"):
            if file.is_file():
                file_attributes = {
                    "path": file, 
                    "name": file.name, 
                    "suffix": file.suffix,
                    "size": file.stat().st_size,
                    "modified": datetime.fromtimestamp(file.stat().st_mtime)
                }
                scans.append(file_attributes)

        return scans
