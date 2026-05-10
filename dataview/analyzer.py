#dataview/analyzer.py 

from datetime import datetime, timedelta
from collections import defaultdict

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
            "old_files": self._old_files()
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