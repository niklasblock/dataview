#dataview/cli.py

import argparse
import sys 
from pathlib import Path

from .scanner import Scanner
from .analyzer import Analyzer
from .reporter import Reporter


def main() -> None:
    """Entry point for the dataview CLI"""
    args = get_cli_argument()
    path = Path(args.file)

    scanner = Scanner(path)
    files = scanner.scan()

    analyzer = Analyzer(files)
    result = analyzer.analyze()

    reporter = Reporter(result)
    markdown_output = reporter.generate()
    
    if args.output: 
        Path(args.output).write_text(markdown_output)
        print(f"Report gespeichert: {args.output}")
    else: 
        print(markdown_output)

def get_cli_argument() -> argparse.Namespace:
    """Parse and validate the CLI drive argument."""
    parser = argparse.ArgumentParser(description="Analysiert Drive Files and Folder")
    parser.add_argument("file", help="Das zu analysierende Laufwerk")
    parser.add_argument("--output", help="Speicherpfad für den Report", default=None)
    args = parser.parse_args()
    
    path = Path(args.file)
    if not path.exists(): 
        print("Kein gültiger Pfad", file=sys.stderr)
        sys.exit(1)

    return args


if __name__ == "__main__": 
    main()