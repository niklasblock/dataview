#dataview/analyzer.py 

from pathlib import Path

class Analyzer: 

    def __init__(self, path: Path) -> None: 
        """Initialize Analyzer with the path from the drive.
    
        Args:
            path: Path to the drive to analyze
        """
        self.path = path 

    def analyze(self) -> list[str]:
        """Analyse Path File 
    
        Returns:
            List: Warning str of missing docstrings
        """

        result = []

        #später dann alle warnung wie auch type hints 
        return result

    def _check_size_folder(self, tree): 
        pass

    def _check_size_files(self): 
        pass 

    def _check_double_data(self):
        """folder, files the heaving the same name"""
        pass 

    def _check_data_older_than_x_years(self): 
        pass 

    #! ich möchte dann auch so gruppen habe, 
    # pdf, docx, excel ... -> informationen 
    # png, icon, ... -> video, bild 
    # ... irgendwie so 