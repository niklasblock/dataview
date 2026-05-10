#dataview/analyzer.py 

from datetime import datetime, timedelta
from collections import defaultdict
import hashlib
from pathlib import Path

CATEGORIES = {
    "Dokumente": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".txt", ".md"],
    "Bilder":    [".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp", ".webp", ".ico"],
    "Videos":    [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
    "Audio":     [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Code":      [".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".sql"],
    "Archive":   [".zip", ".tar", ".gz", ".dmg", ".pkg", ".rar"],
    "Sonstiges": []
}
class Analyzer: 

    def __init__(self, files: list[dict]) -> None: #bekommt Scanner-Output
        """Initialize Analyzer with the path from the drive.
    
        Args:
            path: Path to the drive to analyze
        """
        self.files = files 

    def analyze(self) -> dict:
        """Analyse Path File 
    
        Returns:
            List: Warning str of missing docstrings
        """

        return {
            "largest_files": self._top_largest_files(),
            "largest_folders": self._top_largest_folders(),
            "file_types": self._file_types(),
            "old_files": self._old_files(),
            "duplicates": self._find_duplicates(), 
            "categories": self._categorize_files()
        }
    
    def _top_largest_files(self, n: int = 10) -> list[dict]: 
        """Return top 10 largest files"""
        # Dateien nach Größe sortieren
        sorted_files = sorted(self.files, key=lambda f: f["size"], reverse=True)

        return sorted_files[:n]

    def _top_largest_folders(self, n: int = 10) -> list[dict]: 
        """Return all folder sizes of the input drive"""
        # Ordnergrößen berechnen
        
        folder_sizes = defaultdict(int)
        for f in self.files:
            folder_sizes[f["path"].parent] += f["size"]

        # sortieren und als Liste zurückgeben
        sorted_folders = sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)
        return [{"path": k, "size": v} for k, v in sorted_folders[:n]]

    def _file_types(self) -> dict[str, int]:           # {"pdf": 42, "csv": 13}
        """Return all files types and the amout"""
        file_types = defaultdict(int)
        for file in self.files:
            file_types[file["suffix"]] += 1
        return dict(file_types)

    def _old_files(self, years: int = 2) -> list[dict]: 
        """Return all files witch are older than 2 years"""
        # Alte Dateien filtern
        cutoff = datetime.now() - timedelta(days=years * 365)
        old = [f for f in self.files if f["modified"] < cutoff]

        return old 
    
    def _find_duplicates(self) -> list[dict]: 
        """Files that are identical but have different names or locations."""

        # Erst nach Größe gruppieren — nur gleich große Dateien hashen
        size_groups = defaultdict(list)
        for f in self.files:
            size_groups[f["size"]].append(f)

        hashes = defaultdict(list)
        for size_group in size_groups.values():
            if len(size_group) > 1:  # nur hashen wenn Größe gleich
                for f in size_group:
                    h = _hash_file(f["path"])
                    hashes[h].append(f)

        return [group for group in hashes.values() if len(group) > 1]
    
    def _categorize_files(self) -> dict[str, dict]:
        """Categorize files by type"""
        categories = {cat: {"count": 0, "size": 0, "files": []} for cat in CATEGORIES}
        
        for f in self.files:
            placed = False
            for category, extensions in CATEGORIES.items():
                if f["suffix"].lower() in extensions:
                    categories[category]["files"].append(f)
                    categories[category]["count"] += 1
                    categories[category]["size"] += f["size"]
                    placed = True
                    break
            if not placed:
                categories["Sonstiges"]["files"].append(f)
                categories["Sonstiges"]["count"] += 1
                categories["Sonstiges"]["size"] += f["size"]
        
        return categories

def _hash_file(path: Path) -> str:
    """Calculate MD5 hash of a file"""
    md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()