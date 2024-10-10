
# **HTML Formula Extraction to Excel Tool Documentation**

## **Table of Contents**
1. Introduction
2. Prerequisites
3. Installation Guide
4. Folder Structure
5. Running the Tool
6. Code Explanation
7. Customization Options
8. Troubleshooting
9. Conclusion

---

## **1. Introduction**

The **HTML Formula Extraction to Excel Tool** is a Python script that extracts rules and formulas from static `.htm` or `.html` reports and writes them into an Excel file with clean formatting. The tool also supports automatic encoding detection and handles a variety of HTML structures.

### **Key Features**:
- Automatically detects file encoding using the `chardet` library.
- Parses HTML reports to extract rule descriptions, rule IDs, and formulas.
- Outputs the extracted data into an Excel file.
- Preserves the original formatting of the formulas.
- Supports handling large files and logging errors efficiently.

---

## **2. Prerequisites**

Before running the tool, ensure that you have the following:
- **Windows Operating System**: Installation steps use Chocolatey for installing Python.
- **Python 3.6 or later**: Installed via Chocolatey (or directly).
- **Required Python Libraries**:
  - `beautifulsoup4`: For parsing HTML files.
  - `openpyxl`: For writing to Excel files.
  - `chardet`: For automatic encoding detection.

---

## **3. Installation Guide**

### **Step 1: Install Chocolatey**
Chocolatey is a Windows package manager. If you don’t have it installed, follow these steps:
1. **Open PowerShell** as Administrator (search for PowerShell, right-click, and select "Run as administrator").
2. Run the following command to install Chocolatey:

   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; `
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

3. Verify Chocolatey is installed by running:

   ```bash
   choco --version
   ```

### **Step 2: Install Python via Chocolatey**
1. Run the following command to install Python:

   ```bash
   choco install python -y
   ```

2. After installation, restart the terminal or command prompt and verify Python is installed:

   ```bash
   python --version
   ```

3. Ensure `pip` is installed:

   ```bash
   python -m ensurepip --upgrade
   ```

### **Step 3: Install Required Python Libraries**
Once Python is installed, you need to install the necessary libraries. Run the following commands in the terminal or command prompt:

```bash
pip install beautifulsoup4 openpyxl chardet
```

This installs the necessary libraries for parsing HTML files, writing to Excel, and detecting file encoding.

---

## **4. Folder Structure**

To run the tool, you need to have a specific folder structure on your machine. Here's the recommended setup:

```
Project_Folder
│   formula_extractor.py           # Main Python script
│   README.md                      # Documentation or ReadMe file (optional)
│
├───input_htm                      # Folder for HTML input files
│       report1.htm
│       report2.htm
│       report3.htm
│       ... (more .htm or .html files)
│
└───output                         # Folder for Excel output
        formula_report.xlsx         # Output Excel file (auto-generated)
```

### **Step 1: Create the Project Folder**
1. Create a folder on your system, for example:  
   `C:\Users\Company\05htmtoexcelformula`
   
2. Inside this folder, create two subfolders:
   - **input_htm**: Place your `.htm` or `.html` files in this folder.
   - **output**: The script will generate the Excel file in this folder.

---

## **5. Running the Tool**

### **Step 1: Add HTML Files**
- Place all your `.htm` or `.html` files in the `input_htm` folder you created earlier.
  - Example files: `report1.htm`, `report2.htm`, `report3.htm`, etc.

### **Step 2: Run the Script**
1. Open a terminal or command prompt.
2. Navigate to the project folder using the `cd` command:

   ```bash
   cd C:\Users\Company\05htmtoexcelformula
   ```

3. Run the script:

   ```bash
   python formula_extractor.py
   ```

### **Step 3: View the Output**
- After the script finishes processing, check the `output` folder for the generated `formula_report.xlsx` file.

---

## **6. Code Explanation**

### **Key Components**:
1. **Encoding Detection**: The `detect_encoding()` function uses the `chardet` library to detect the encoding of each HTML file before parsing it.
2. **HTML Parsing (BeautifulSoup)**: The script reads each `.htm` file and uses `BeautifulSoup` to find rule IDs, rule names, and formulas.
3. **Excel Writing (openpyxl)**: The `write_to_excel()` function writes the extracted data into an Excel file, ensuring formulas are displayed with line breaks using `wrap_text=True`.
4. **Column Sizing**: Column widths are adjusted to 50 characters for readability.

---

## **7. Customization Options**

### **Input/Output Paths**:
- By default, the script looks for `.htm` files in the `input_htm` folder and saves the Excel file in the `output` folder. You can change these paths in the script by modifying the `input_directory` and `output_excel` variables.

### **Handling Large Files**:
- The script can handle large HTML files efficiently due to memory-safe operations and by only reading the first 1MB of each file for encoding detection.

### **HTML Structure Variations**:
- The script can handle a variety of HTML formats where rule IDs and names may be in different tags like `<h3>`, `<strong>`, etc. The code is designed to flexibly detect these elements.

---

## **8. Troubleshooting**

### **Common Issues**:

1. **Encoding Errors**:
   - If the encoding of an HTML file cannot be detected, it defaults to `utf-8`. If issues persist, check if the file is corrupted or non-standard.

2. **No Data Extracted**:
   - Ensure that the `.htm` or `.html` files in the `input_htm` folder contain rule and formula structures that the script can detect. Check if tags like `<h3>` or `<pre>` are used for rule names and formulas.

3. **Excel Output Format**:
   - If the formatting in Excel does not appear correctly, ensure the `wrap_text=True` option is used in the `write_to_excel()` function.

---

## **9. Conclusion**

The **HTML Formula Extraction to Excel Tool** automates the process of extracting rule IDs, rule names, and formulas from HTML reports and exporting them to an Excel file. With features like automatic encoding detection and support for various HTML structures, this tool is highly adaptable and efficient.

By following the installation guide and using the provided script, you can easily process large numbers of HTML files and generate structured Excel reports with well-formatted formulas.
