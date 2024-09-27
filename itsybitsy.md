Certainly! Here's the complete documentation, including the installation commands for `pdftk` and the detailed instructions for setting up and running the PDF splitting process.

---

# PDF Splitting Using PowerShell and `pdftk`

This documentation provides a step-by-step guide to splitting a PDF file (`input.pdf`) into multiple smaller files based on a CSV file (`page-count.csv`). The process uses a PowerShell script and `pdftk` (PDF Toolkit).

## Table of Contents
- [Prerequisites](#prerequisites)
- [Folder Structure](#folder-structure)
- [Step 1: Installing PDFTK](#step-1-installing-pdftk)
- [Step 2: Preparing the CSV File](#step-2-preparing-the-csv-file)
- [Step 3: Writing the PowerShell Script](#step-3-writing-the-powershell-script)
- [Step 4: Running the Script](#step-4-running-the-script)
- [Step 5: Verifying the Output](#step-5-verifying-the-output)

---

## Prerequisites

- **Windows Operating System**
- **PowerShell**
- **PDFTK (PDF Toolkit)**: Ensure `pdftk` is installed and added to your system's PATH.

## Folder Structure

The files should be organized as follows:

```
C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdkt\
│
├── input.pdf          # The PDF file to be split
├── page-count.csv     # The CSV file with split instructions
└── Split-PDF.ps1      # The PowerShell script to perform the split
```

## Step 1: Installing PDFTK

To use `pdftk` for splitting PDFs, you need to install it on your system. You can do this using Chocolatey, a package manager for Windows.

1. **Install Chocolatey** (if not already installed):

   Open PowerShell as Administrator and run:

   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Install PDFTK**:

   Once Chocolatey is installed, run the following command to install `pdftk`:

   ```powershell
   choco install pdftk
   ```

This command installs `pdftk` and adds it to your system PATH, making it available for use in any command prompt or PowerShell session.

## Step 2: Preparing the CSV File

The `page-count.csv` file should be formatted as follows:

```plaintext
FileName                                                                                  PageCount
C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdkt\doc1.pdf                            1
C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdkt\doc2.pdf                            9
```

- **FileName**: The full path where each split PDF file will be saved.
- **PageCount**: The number of pages each resulting PDF should contain.

Ensure that the CSV file has a header row (`FileName` and `PageCount`), and each subsequent row specifies the output file and the number of pages for that split.

## Step 3: Writing the PowerShell Script

Create a PowerShell script named `Split-PDF.ps1` in the same folder. The script should contain the following code:

```powershell
# Define the base folder path
$baseFolderPath = "C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdkt"

# Define the path to the input PDF and the CSV file
$inputPdfPath = Join-Path -Path $baseFolderPath -ChildPath "input.pdf"
$pageCountFilePath = Join-Path -Path $baseFolderPath -ChildPath "page-count.csv"

# Initialize the starting page
$startPage = 1

# Read the page counts from the CSV file
Get-Content -Path $pageCountFilePath | Select-Object -Skip 1 | ForEach-Object {
    $line = $_.Trim()
    
    # Split the line into FileName and PageCount based on the last space
    $lastSpaceIndex = $line.LastIndexOf(' ')
    $outputFileName = $line.Substring(0, $lastSpaceIndex).Trim()
    $pageCount = [int]$line.Substring($lastSpaceIndex + 1).Trim()
    
    # Calculate the end page for this split
    $endPage = $startPage + $pageCount - 1
    
    # Run pdftk to split the PDF
    $cmd = "pdftk `"$inputPdfPath`" cat $startPage-$endPage output `"$outputFileName`""
    Invoke-Expression $cmd
    
    # Update the starting page for the next split
    $startPage = $endPage + 1
}

Write-Host "PDF splitting completed. Files are saved in $baseFolderPath"
```

## Step 4: Running the Script

1. **Navigate to the Folder**:
   - Open PowerShell and navigate to `C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdkt`.

2. **Run the Script**:
   - Execute the script by typing:
     ```powershell
     .\Split-PDF.ps1
     ```

## Step 5: Verifying the Output

After running the script:

1. **Check the `pdkt` Folder**:
   - The split PDF files should be saved in `C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdkt`, with file names and page counts matching those specified in the `page-count.csv`.

2. **Review the Output**:
   - Ensure each PDF contains the correct number of pages as indicated by the `PageCount` in the CSV file.

---

### Conclusion

This guide should help you successfully split a PDF file into multiple smaller files based on a CSV configuration using PowerShell and `pdftk`. If you encounter any issues or need further assistance, feel free to seek additional support.

