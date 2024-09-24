# Assignment 1: PDF Splitter Using pdftk and PowerShell

This project provides a PowerShell script to split a PDF file into multiple parts based on page counts specified in a CSV file. The script uses `pdftk` (PDF Toolkit) to perform the splitting.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Folder Structure](#folder-structure)
- [Step 1: Setting Up the Environment](#step-1-setting-up-the-environment)
- [Step 2: Preparing the CSV File](#step-2-preparing-the-csv-file)
- [Step 3: Writing the PowerShell Script](#step-3-writing-the-powershell-script)
- [Step 4: Installing PDFTK](#step-4-installing-pdftk)
- [Step 5: Running the PowerShell Script](#step-5-running-the-powershell-script)
- [Step 6: Verifying the Output](#step-6-verifying-the-output)

## Prerequisites
- Windows OS
- PowerShell
- `pdftk` (PDF Toolkit)
- Chocolatey (for easy installation of `pdftk`)

## Folder Structure

Ensure that your project folder is structured as follows:

```
J:\Denny_01_source_code\_05_split_pdf\pdftk
├── input.pdf               # Your input PDF file
├── page-count.csv          # CSV file specifying the split details
├── Split-PDF.ps1           # PowerShell script for splitting the PDF
└── output\                 # Folder where split PDF files will be saved
```

## Step 1: Setting Up the Environment

1. **Navigate to the base folder:**
   
   ```
   J:\Denny_01_source_code\_05_split_pdf\pdftk
   ```

2. **Create the necessary files and folders as described in the folder structure section.**

## Step 2: Preparing the CSV File

Create the `page-count.csv` file in the `pdftk` folder with the following content:

```plaintext
FileName,PageCount
input.pdf,2
input.pdf,3
input.pdf,4
input.pdf,4
input.pdf,2
```

This CSV file specifies how the PDF should be split. Each row represents a split, with the number of pages to include in each split.

## Step 3: Writing the PowerShell Script

Create a PowerShell script `Split-PDF.ps1` in the `pdftk` folder with the following content:

```powershell
# Define the base folder path
$baseFolderPath = "J:\\Denny_01_source_code\\_05_split_pdf\\pdftk"

# Define paths to input PDF, CSV file, and output folder
$inputPdfPath = Join-Path -Path $baseFolderPath -ChildPath "input.pdf"
$pageCountFilePath = Join-Path -Path $baseFolderPath -ChildPath "page-count.csv"
$outputFolderPath = Join-Path -Path $baseFolderPath -ChildPath "output"

# Create the output folder if it doesn't exist
if (-Not (Test-Path $outputFolderPath)) {
    New-Item -Path $outputFolderPath -ItemType Directory
}

# Read the page counts from the CSV file
$pageCounts = Import-Csv -Path $pageCountFilePath

# Initialize the starting page
$startPage = 1
$splitCounter = 1

# Loop through each entry in the page count file
foreach ($entry in $pageCounts) {
    $pageCount = [int]$entry.PageCount

    # Define the output file name
    $outputFileName = "split_part_$splitCounter.pdf"
    $outputFilePath = Join-Path -Path $outputFolderPath -ChildPath $outputFileName

    # Calculate the end page for this split
    $endPage = $startPage + $pageCount - 1

    # Run pdftk to split the PDF
    $cmd = "pdftk `"$inputPdfPath`" cat $startPage-$endPage output `"$outputFilePath`""
    Invoke-Expression $cmd

    # Update the starting page for the next split
    $startPage = $endPage + 1
    $splitCounter++
}

Write-Host "PDF splitting completed. Files are saved in $outputFolderPath"
```

This script reads the `page-count.csv` file and splits the `input.pdf` according to the specified page ranges.

## Step 4: Installing PDFTK

PDFTK is required to perform the actual PDF splitting. You can install it using Chocolatey, a package manager for Windows.

1. **Install Chocolatey** (if not already installed):
   Open PowerShell as Administrator and run:

   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Install PDFTK**:
   Once Chocolatey is installed, run the following command to install PDFTK:

   ```powershell
   choco install pdftk
   ```

This command installs PDFTK and adds it to your system PATH, making it available for use in any command prompt or PowerShell session.

## Step 5: Running the PowerShell Script

1. **Open PowerShell:**
   Navigate to the `pdkt` directory:

   ```powershell
   cd "J:\\Denny_01_source_code\\_05_split_pdf\\pdftk"
   ```

2. **Run the script:**

   ```powershell
   .\\Split-PDF.ps1
   ```

This command executes the script, which reads the `page-count.csv` file and splits the `input.pdf` file according to the specified page ranges.

## Step 6: Verifying the Output

1. **Check the `output` folder:**
   After running the script, navigate to the `output` folder:

   ```
   J:\\Denny_01_source_code\\_05_split_pdf\\pdftk\\output
   ```

2. **Verify the split PDFs:**
   You should see the split PDF files named `split_part_1.pdf`, `split_part_2.pdf`, etc., according to the page counts specified in the CSV file.

## Conclusion

This setup allows you to split a PDF file into multiple smaller PDFs based on a page count specified in a CSV file, using `pdftk` and PowerShell. The `Split-PDF.ps1` script automates the process, making it easy to handle large PDF files in a structured and repeatable manner.

### Summary:

1. **Updated the paths** in the `README.md` and the PowerShell script to match the new folder structure: `J:\\Denny_01_source_code\\_05_split_pdf\\pdftk`.
2. **Ensure the folder structure** is set up as described, with the necessary files in the correct locations.
3. **Install `pdftk` using Chocolatey** if it's not already installed.
4. **Run the PowerShell script** to split your PDF according to the specifications in the CSV file.
5. **Verify the output** in the `output` folder.

This documentation and script should help you manage and execute the PDF splitting process efficiently.
