from datetime import datetime, timedelta
import ast 
from dataview.analyzer import Analyzer
from pathlib import Path 
import pytest
import textwrap
import tempfile
import os 

def test_top_largest_files(): 
    """Files should be ordered by the size"""

    files = [
        {"path": Path("/tmp/doc.pdf"), "name": "doc.pdf", "suffix": ".pdf", 
         "size": 1000, "modified": datetime.now()},
        {"path": Path("/tmp/photo.jpg"), "name": "photo.jpg", "suffix": ".jpg", 
         "size": 2000, "modified": datetime.now()},
        {"path": Path("/tmp/script.py"), "name": "script.py", "suffix": ".py", 
         "size": 500, "modified": datetime.now()},
    ]

    analyzer = Analyzer(files)
    result = analyzer._top_largest_files()

    assert result[0]["name"] == "photo.jpg"   # größte Datei zuerst
    assert result[1]["name"] == "doc.pdf"
    assert result[2]["name"] == "script.py"   # kleinste zuletzt

def test_file_types(): 
    """File suffix counted"""

    files = [
        {"path": Path("/tmp/doc.pdf"), "name": "doc.pdf", "suffix": ".pdf", 
         "size": 1000, "modified": datetime.now()},
        {"path": Path("/tmp/photo.jpg"), "name": "photo.jpg", "suffix": ".jpg", 
         "size": 2000, "modified": datetime.now()},
        {"path": Path("/tmp/script.py"), "name": "script.py", "suffix": ".py", 
         "size": 500, "modified": datetime.now()},
    ]

    analyzer = Analyzer(files)
    result = analyzer._file_types()

    assert result[".pdf"] == 1
    assert result[".jpg"] == 1
    assert result[".py"] == 1  

def test_old_files():
    """Files older than 2 years should be returned"""
    
    old_date = datetime.now() - timedelta(days=365 * 3)
    
    files = [
        {"path": Path("/tmp/doc.pdf"), "name": "doc.pdf", "suffix": ".pdf",
         "size": 1000, "modified": datetime.now()},
        {"path": Path("/tmp/photo.jpg"), "name": "photo.jpg", "suffix": ".jpg",
         "size": 2000, "modified": old_date},
        {"path": Path("/tmp/script.py"), "name": "script.py", "suffix": ".py",
         "size": 500, "modified": datetime.now()},
    ]

    analyzer = Analyzer(files)
    result = analyzer._old_files()

    assert len(result) == 1
    assert result[0]["name"] == "photo.jpg"

def test_categorize_files():
    """Files should be correctly categorized by their suffix"""
    
    files = [
        {"path": Path("/tmp/doc.pdf"), "name": "doc.pdf", "suffix": ".pdf", 
         "size": 1000, "modified": datetime.now()},
        {"path": Path("/tmp/photo.jpg"), "name": "photo.jpg", "suffix": ".jpg", 
         "size": 2000, "modified": datetime.now()},
        {"path": Path("/tmp/script.py"), "name": "script.py", "suffix": ".py", 
         "size": 500, "modified": datetime.now()},
    ]
    
    analyzer = Analyzer(files)
    result = analyzer._categorize_files()
    
    assert result["Dokumente"]["count"] == 1
    assert result["Bilder"]["count"] == 1
    assert result["Code"]["count"] == 1

def test_find_duplicates():
    """Two files with identical content should be detected as duplicates"""
    
    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False) as f:
        f.write("identischer inhalt")
        tmp_path1 = Path(f.name)

    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False) as f:
        f.write("identischer inhalt")
        tmp_path2 = Path(f.name)

    try:
        # files Liste bauen wie der Scanner sie liefern würde
        files = [
            {"path": tmp_path1, "name": tmp_path1.name, "suffix": ".txt", 
             "size": tmp_path1.stat().st_size, "modified": datetime.now()},
            {"path": tmp_path2, "name": tmp_path2.name, "suffix": ".txt", 
             "size": tmp_path2.stat().st_size, "modified": datetime.now()},
        ]

        analyzer = Analyzer(files)
        result = analyzer._find_duplicates()

        assert len(result) == 1        # eine Gruppe von Duplikaten
        assert len(result[0]) == 2     # zwei Dateien in der Gruppe

    finally:
        tmp_path1.unlink(missing_ok=True)
        tmp_path2.unlink(missing_ok=True)

def test_top_largest_folders():
    """Folders should be ordered by total size"""
    
    files = [
        {"path": Path("/tmp/a/doc.pdf"), "name": "doc.pdf", "suffix": ".pdf",
         "size": 1000, "modified": datetime.now()},
        {"path": Path("/tmp/b/big.dmg"), "name": "big.dmg", "suffix": ".dmg",
         "size": 5000, "modified": datetime.now()},
        {"path": Path("/tmp/b/photo.jpg"), "name": "photo.jpg", "suffix": ".jpg",
         "size": 2000, "modified": datetime.now()},
    ]

    analyzer = Analyzer(files)
    result = analyzer._top_largest_folders()

    assert result[0]["path"] == Path("/tmp/b")  # größter Ordner zuerst
    assert result[0]["size"] == 7000            # 5000 + 2000
