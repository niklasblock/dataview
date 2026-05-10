#dataview/cli.py

import argparse
import sys 
from pathlib import Path

from .scanner import Scanner
from .analyzer import Analyzer

def main() -> None:
    """Entry point for the dataview CLI"""
    path = get_cli_argument() 

    path = get_cli_argument() 

    scanner = Scanner(path)
    files = scanner.scan()

    analyzer = Analyzer(files)
    result = analyzer.analyze()

    print(result)

def get_cli_argument() -> Path: 
    """Parse and validate the CLI drive argument.
    
    Returns:
        Path: validated drive path
    
    Exits:
        1: if file does not exist 
    """
    parser = argparse.ArgumentParser(description="Analysiert Drive Files and Folder")
    parser.add_argument("file", help="Das zu analysierende Laufwerk")
    args = parser.parse_args() # Argument einlesen
    path = Path(args.file) # Zugriff auf den Wert und diesen zu einenm Pfad machen 
    if not path.exists(): 
        print("Kein gültiger Pfad", file=sys.stderr)
        sys.exit(1)

    return path 

if __name__ == "__main__": 
    main()