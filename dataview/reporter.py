
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
            self._old_files_section()
        )

    def _files_section(self) -> str:
        """"""
        lines = ["## 📁 Top 10 größte Dateien\n"]
        lines.append("| Datei | Größe |")
        lines.append("|-------|-------|")
        for f in self.result["largest_files"]:
            lines.append(f"| {f['name']} | {format_size(f['size'])} |")
        return "\n".join(lines)


    def _folders_section(self) -> str: 
        """"""
        lines = ["## 📂 Top 10 größte Ordner\n"]
        lines.append("| Ordner | Größe |")
        lines.append("|-------|-------|")
        for f in self.result["largest_folders"]:
            lines.append(f"| {f['path']} | {format_size(f['size'])} |")
        return "\n".join(lines)

    def _types_section(self) -> str: 
        """"""
        lines = ["## 📋 Dateitypen\n"]
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
        lines.append("| Datei | Größe |")
        lines.append("|-------|-------|")
        for f in self.result["old_files"]:
            lines.append(f"| {f['name']} | {format_size(f['size'])} |")
        return "\n".join(lines)

def format_size(bytes: int) -> str:
        """Convert bytes to human readable format"""
        for unit in ["B", "KB", "MB", "GB"]:
            if bytes < 1024:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024
        return f"{bytes:.1f} TB"