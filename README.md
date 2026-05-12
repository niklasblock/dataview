# dataview

A Python-based storage analysis and file intelligence platform.

## Installation

```bash
git clone git@github.com:niklasblock/dataview.git
cd dataview
pip install -e .
```

## Usage

```bash
dataview ~/Documents 
dataview ~/Documents --output report.md
```

## Analysis 
- Top 10 largest Files
- Top 10 largest Folders
- Duplicate Files
- File suffix counter 
- Categories Files 
- Files older than 2 years

## Development
```bash
pytest tests/