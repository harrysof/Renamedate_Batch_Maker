#!/usr/bin/env python3

def generate_renamer_script():
    print("=" * 50)
    print("   Custom File Renamer Script Generator")
    print("=" * 50)
    print()
    
    # Ask for the custom name
    custom_name = input("Enter the name for your files (e.g., Reddit Posts, Memes, Photos): ").strip()
    
    # Check if input is empty
    if not custom_name:
        print("Error: Name cannot be empty!")
        input("Press Enter to exit...")
        return
    
    # Create output filename with Z prefix for visibility
    output_file = f"Z {custom_name}.cmd"
    
    # Generate the script content
    script_content = f"""@echo off
setlocal enabledelayedexpansion

:: Check if exiftool is available
set "exiftool=exiftool.exe"
where %exiftool% >nul 2>&1
if %errorlevel% neq 0 (
    echo exiftool is not installed or not in PATH. Please install it from https://exiftool.org/ 
    pause
    exit /b
)

:: Check if any files were dropped
if "%~1"=="" (
    echo Please drag and drop one or more files onto this script. 
    pause
    exit /b
)

:: Date is chosen automatically: metadata date (Date Taken) is used first.
:: If metadata is missing, falls back to file creation date silently.

:: Create a temporary file to store files with their dates
set "tempFile=%temp%\\screenshot_sort_%random%.txt"
if exist "%tempFile%" del "%tempFile%"

:: First pass: collect all files with their dates
echo.
echo Analyzing files...
for %%A in (%*) do (
    set "file=%%~fA"
    set "ext=%%~xA"
    set "metadata_date="
    set "sortable_date="

    :: Get metadata date using exiftool 
    for /f "tokens=*" %%a in ('%exiftool% -DateTimeOriginal -d "%%Y%%m%%d" "!file!" 2^>nul ^| findstr /i "Date/Time Original"') do (
        set "metadata_date=%%a"
    )

    :: Clean up metadata_date to get YYYYMMDD format
    if defined metadata_date (
        set "metadata_date=!metadata_date:~25!"
        set "metadata_date=!metadata_date: =!"
        set "metadata_date=!metadata_date::=!"
        set "sortable_date=!metadata_date!"
    )

    :: Fallback to creation date if metadata is missing
    if "!sortable_date!"=="" (
        for /f "tokens=*" %%a in ('powershell -Command "(Get-Item '!file!').CreationTime.ToString('yyyyMMdd')"') do (
            set "sortable_date=%%a"
        )
    )

    :: Write to temp file: sortable_date|full_path
    echo !sortable_date!^|!file! >> "%tempFile%"
)

:: Sort the temporary file by date
set "sortedFile=%temp%\\screenshot_sorted_%random%.txt"
if exist "%sortedFile%" del "%sortedFile%"
sort "%tempFile%" > "%sortedFile%"
del "%tempFile%"

:: Find the highest number currently used in the folder
set maxNum=0
for /f "delims=" %%F in ('dir /b "%~dp0{custom_name} (*)*" 2^>nul') do (
    for /f "tokens=2 delims=()" %%N in ("%%F") do (
        if %%N GTR !maxNum! set "maxNum=%%N"
    )
)

:: Second pass: process files in sorted order
echo.
echo Renaming files from oldest to newest...
echo.
for /f "tokens=1,2 delims=|" %%D in (%sortedFile%) do (
    set "file=%%E"
    set "ext=%%~xE"
    set /a maxNum+=1
    set "final_date="

    :: Try metadata date first (Date Taken)
    for /f "tokens=*" %%a in ('%exiftool% -DateTimeOriginal -d "%%d-%%m-%%Y" "!file!" 2^>nul ^| findstr /i "Date/Time Original"') do (
        set "final_date=%%a"
    )

    :: Clean up metadata_date 
    if defined final_date (
        set "final_date=!final_date:~25!"
        set "final_date=!final_date: =!"
        set "final_date=!final_date::=!"
    )

    :: Fallback to creation date if metadata is missing
    if "!final_date!"=="" (
        for /f "tokens=*" %%a in ('powershell -Command "(Get-Item '!file!').CreationTime.ToString('dd-MM-yyyy')"') do (
            set "final_date=%%a"
        )
    )

    :: Build new name
    set "newName={custom_name} (!maxNum!) - !final_date!!ext!"

    :: Copy and rename
    copy "!file!" "%~dp0!newName!" >nul
    if !errorlevel! equ 0 (
        echo [OK] !newName!
    ) else (
        echo [ERROR] Failed to copy: %%~nxE
    )
)

:: Clean up
del "%sortedFile%"

echo.
echo Processing complete.
exit"""
    
    # Write the script to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print()
        print(f"✓ Success! Generated script: {output_file}")
        print()
        print("Usage:")
        print("1. Drag and drop files onto the generated .cmd file")
        print("2. Files are automatically dated: metadata date (Date Taken) is used first,")
        print("   falling back to file creation date if metadata is unavailable.")
        print("3. Files will be renamed in chronological order")
        print()
        
    except Exception as e:
        print(f"Error writing file: {e}")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    generate_renamer_script()

