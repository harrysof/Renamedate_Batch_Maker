# Renamer CMD Maker

A Python script that generates custom Windows batch files for renaming multiple files in chronological order.

## What It Does

This tool creates personalized `.cmd` scripts that you can use to batch rename files with sequential numbering and dates. It's particularly useful for organizing photos, screenshots, or any collection of files you want to keep in order.

## Requirements

- Windows operating system
- Python 3.x
- [ExifTool](https://exiftool.org/) installed and available in your system PATH

## Installation

1. Download `Renamer_CMD_Maker.py`
2. Install ExifTool from https://exiftool.org/
3. Make sure ExifTool is added to your system PATH

## Usage

### Step 1: Generate Your Custom Renamer

Run the Python script:

```
python Renamer_CMD_Maker.py
```

When prompted, enter a name for your file collection (e.g., "Family Photos", "Work Documents", "Screenshots").

The script will create a `.cmd` file with your chosen name, prefixed with "Z" to keep it at the bottom of your file list.

### Step 2: Use the Generated Script

1. Locate the newly created `.cmd` file (e.g., `Z Family Photos.cmd`)
2. Drag and drop the files you want to rename onto this `.cmd` file
3. Choose your preferred date source:
   - Option 1: Metadata date (Date Taken from photo EXIF data)
   - Option 2: File creation date
4. The script will process and rename your files

## Output Format

Files are renamed with the following pattern:

```
[Custom Name] (Number) - DD-MM-YYYY[Extension]
```

For example:
```
Family Photos (1) - 23-12-2023.jpg
Family Photos (2) - 24-12-2023.jpg
Family Photos (3) - 25-12-2023.jpg
```

## Features

- **Chronological sorting** - Files are automatically sorted from oldest to newest before renaming
- **Smart numbering** - If files with the same naming pattern already exist in the folder, numbering continues from the highest existing number
- **Date flexibility** - Choose between metadata dates (for photos) or file creation dates
- **Safe operation** - Creates copies of files rather than modifying originals
- **Batch processing** - Handle multiple files at once

## How It Works

The generated batch script performs these steps:

1. Checks for ExifTool installation
2. Collects all dropped files and extracts their dates
3. Sorts files chronologically based on your chosen date source
4. Finds the highest existing number in the target folder
5. Renames files sequentially with dates in DD-MM-YYYY format
6. Copies renamed files to the same directory as the script

## Notes

- The script uses ExifTool to read photo metadata. If metadata is unavailable, it falls back to the file's creation date
- Files are copied, not moved, so your originals remain unchanged
- The generated `.cmd` files must be in the same directory where you want the renamed files to appear

## Troubleshooting

**ExifTool not found error**
- Make sure ExifTool is installed and added to your system PATH
- Restart your command prompt or system after installing ExifTool

**No files processed**
- Ensure you're dragging files directly onto the `.cmd` file
- Check that the files aren't read-only or locked by another program

**Dates showing as creation date when you expected metadata date**
- Some files don't contain EXIF metadata (non-photo files, edited images, etc.)
- The script automatically falls back to creation date when metadata is unavailable

## License

Free to use and modify as needed.
