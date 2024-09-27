# Define the input folder path where input.pdf and page-count.csv are located
$inputFolderPath = "C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdkt"

# Define the path to the input PDF and the CSV file
$inputPdfPath = Join-Path -Path $inputFolderPath -ChildPath "input.pdf"
$pageCountFilePath = Join-Path -Path $inputFolderPath -ChildPath "page-count.csv"

# Initialize the starting page
$startPage = 1

# Read the page counts from the CSV file
Get-Content -Path $pageCountFilePath | Select-Object -Skip 1 | ForEach-Object {
    $line = $_.Trim()
    
    # Split the line based on spaces and extract the last element as PageCount
    $parts = $line -split '\s+'
    
    if ($parts.Count -ge 2) {
        $outputFileName = $parts[0..($parts.Count - 2)] -join " "
        $outputFileName = Join-Path -Path $inputFolderPath -ChildPath (Split-Path -Leaf $outputFileName)
        $pageCount = $parts[-1]
        
        if ($pageCount -match '^\d+$') {
            # Calculate the end page for this split
            $endPage = $startPage + [int]$pageCount - 1
            
            # Run pdftk to split the PDF
            $cmd = "pdftk `"$inputPdfPath`" cat $startPage-$endPage output `"$outputFileName`""
            Invoke-Expression $cmd
            
            # Update the starting page for the next split
            $startPage = $endPage + 1
        }
        else {
            Write-Host "Error: PageCount '$pageCount' is not a valid number." -ForegroundColor Red
        }
    }
    else {
        Write-Host "Error: Line does not have enough parts to extract FileName and PageCount." -ForegroundColor Red
    }
}

Write-Host "PDF splitting completed. Files are saved in $inputFolderPath"
