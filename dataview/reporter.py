
def format_size(bytes: int) -> str:
        """Convert bytes to human readable format"""
        for unit in ["B", "KB", "MB", "GB"]:
            if bytes < 1024:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024
        return f"{bytes:.1f} TB"

class Reporter: 

    def __init__(self, result: dict) -> None:
        """Initialize Scanner with the result from the drive.
    
        Args:
            result: dict with analyzer results 
        """
        self.result = result 

    def generate(self) -> str: #gibt kompletten Markdown String zurück 
        """"""
        header = "# 📊 DataView Report\n\n"
        return (
            header + 
            self._files_section() + "\n\n" +
            self._folders_section() + "\n\n" +
            self._types_section() + "\n\n" +
            self._old_files_section() + "\n\n" +
            self._duplicates_section() + "\n\n" +
            self._categories_section() + "\n\n" +
            self._empty_files_section()
        )

    def _files_section(self) -> str:
        """"""
        lines = ["## 📁 Top 10 größte Dateien\n"]

        if not self.result["largest_files"]: 
            lines.append("Keine großen Dateien gefunden.")
            return "\n".join(lines)

        lines.append("| Datei | Größe |")
        lines.append("|-------|-------|")
        for f in self.result["largest_files"]:
            lines.append(f"| {f['name']} | {format_size(f['size'])} |")
        return "\n".join(lines)


    def _folders_section(self) -> str: 
        """"""
        lines = ["## 📂 Top 10 größte Ordner\n"]

        if not self.result["largest_folders"]: 
            lines.append("Keine großen Ordner gefunden.")
            return "\n".join(lines)

        lines.append("| Ordner | Größe |")
        lines.append("|-------|-------|")
        for f in self.result["largest_folders"]:
            lines.append(f"| {f['path']} | {format_size(f['size'])} |")
        return "\n".join(lines)

    def _types_section(self) -> str: 
        """"""
        lines = ["## 📋 Dateitypen\n"]

        if not self.result["file_types"]: 
            lines.append("Keine Dateiendungen gefunden.")
            return "\n".join(lines)

        lines.append("| Typ | Anzahl |")
        lines.append("|-------|-------|")
        for suffix, count in self.result["file_types"].items():
            if suffix == "": 
                lines.append(f"| {suffix or 'ohne Endung'} | {count} |")
            else: 
                lines.append(f"| {suffix} | {count} |")
        return "\n".join(lines)

    def  _old_files_section(self) -> str: 
        """"""
        lines = ["## ⚠️ Alte Dateien (> 2 Jahre)\n"]

        if not self.result["old_files"]:
            lines.append("Keine alten Dateien gefunden.")
            return "\n".join(lines)

        lines.append("| Datei | Größe |")
        lines.append("|-------|-------|")
        for f in self.result["old_files"]:
            lines.append(f"| {f['name']} | {format_size(f['size'])} |")
        return "\n".join(lines)
    
    def _duplicates_section(self) -> str:
        """Return markdown section for duplicate files"""
        lines = ["## 🔁 Doppelte Dateien\n"]
        
        if not self.result["duplicates"]:
            lines.append("Keine doppelten Dateien gefunden.")
            return "\n".join(lines)
        
        lines.append("| Datei | Pfad | Größe |")
        lines.append("|-------|------|-------|")
        
        for group in self.result["duplicates"]:
            for f in group:
                lines.append(f"| {f['name']} | {f['path'].parent} | {format_size(f['size'])} |")
            lines.append("|-------|------|-------|")  # Trennlinie zwischen Gruppen
        
        return "\n".join(lines)
    
    def _categories_section(self) -> str:
        """Return markdown section for file categories"""
        lines = ["## 📂 Kategorien\n"]

        if not self.result["categories"]:
            lines.append("Keine Kategorien gefunden.")
            return "\n".join(lines)

        lines.append("| Kategorie | Anzahl | Größe |")
        lines.append("|-----------|--------|-------|")
        
        for category, data in self.result["categories"].items():
            if data["count"] > 0:  # nur Kategorien mit Dateien anzeigen
                lines.append(f"| {category} | {data['count']} | {format_size(data['size'])} |")
        
        return "\n".join(lines)

    def _empty_files_section(self) -> str: 
        """Return markdown section for empty files"""

        lines = ["## 📂 Leere Dateien\n"]

        if not self.result["empty_files"]:
            lines.append("Keine leeren Dateien gefunden.")
            return "\n".join(lines)
        
        lines.append("| Datei | Pfad |")
        lines.append("|-------|------|")

        for f in self.result["empty_files"]:
            lines.append(f"| {f['name']} | {f['path'].parent} |")
            lines.append("|-------|------|")  # Trennlinie zwischen Gruppen
        
        return "\n".join(lines)