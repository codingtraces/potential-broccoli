
# **HTML Formula Extraction to Excel Tool with Automatic Encoding Detection**

## **Table of Contents**
1. Introduction
2. Prerequisites
3. Installation Guide
4. Detailed Workflow
5. Code Explanation
6. Customization Options
7. Troubleshooting
8. Conclusion

---

## **1. Introduction**

The **HTML Formula Extraction to Excel Tool** is a Python script that extracts formulas from static `.htm` reports and writes them into an Excel file, while preserving the original multi-line formatting of the formulas. The tool now includes automatic detection of file encoding to handle different character sets that may cause errors in processing.

### **Key Features:**
- Automatically detects file encoding.
- Parses HTML reports to extract rule descriptions and formulas.
- Outputs the extracted data into a neatly formatted Excel file.
- Preserves the original line breaks in the formulas.

---

## **2. Prerequisites**

Before setting up and running the tool, ensure that you have the following installed on your system:

- **Python 3.6 or later**: You can download Python from [python.org](https://www.python.org/downloads/).
- **Required Python Libraries**:
  - `beautifulsoup4`: For parsing HTML files.
  - `openpyxl`: For writing to Excel files.
  - `chardet`: For automatic encoding detection.

To install these libraries, follow the steps in the installation guide.

---

## **3. Installation Guide**

### **Step 1: Install Python**
1. Go to the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Download and install the latest version of Python for your operating system.
3. Ensure Python is added to your system's **PATH** during installation (there’s a checkbox during installation for this).

### **Step 2: Install Required Libraries**
Once Python is installed, you need to install the libraries used by the script. Open a terminal or command prompt and run the following commands:

```bash
pip install beautifulsoup4 openpyxl chardet
```

This installs the necessary libraries for parsing HTML files, writing to Excel, and detecting file encoding.

---

## **4. Detailed Workflow**

### **Step 1: Directory Setup**
1. **Create a folder** on your machine where you will store the script and HTML files. For example:  
   `C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\05htmtoexcelformula`
   
2. **Create an input folder** inside this directory where you will place the `.htm` files:  
   `C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\05htmtoexcelformula\input_htm`

3. **Place the HTML files** (like `Batch_BrokerManagement.htm` or other reports) into the `input_htm` folder.

4. **Create an output folder** where the Excel reports will be saved:  
   `C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\05htmtoexcelformula\output`

### **Step 2: Python Script**
In the same directory, create a Python script file called `formula_extractor.py` and paste the following code into it:

---

### **Complete Code with Automatic Encoding Detection:**

```python
import os
from bs4 import BeautifulSoup
import openpyxl
import logging
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
import chardet

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_encoding(file_path):
    """Detect the encoding of the file."""
    with open(file_path, 'rb') as raw_file:
        raw_data = raw_file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def extract_data_from_htm(file_path):
    extracted_data = []
    try:
        # Detect the file's encoding
        encoding = detect_encoding(file_path)
        logging.info(f"Detected encoding for {file_path}: {encoding}")

        # Open the file with the detected encoding
        with open(file_path, 'r', encoding=encoding) as file:
            soup = BeautifulSoup(file, 'html.parser')

            sections = soup.find_all('h3')  # Assuming rule sections start with <h3>
            for section in sections:
                rule_title = section.get_text().strip()
                formula_tag = section.find_next('pre')  # Assuming formulas are in <pre> tags
                if formula_tag:
                    formula_text = formula_tag.get_text().strip()
                    extracted_data.append((rule_title, formula_text, file_path))
    except Exception as e:
        logging.error(f"Error parsing file {file_path}: {e}")
    return extracted_data

def write_to_excel(extracted_data, output_excel):
    try:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Extracted Formulas'

        # Write headers
        headers = ['Rule Description', 'Formula', 'Source File']
        sheet.append(headers)

        for row_index, data in enumerate(extracted_data, start=2):  # start=2 to account for headers in row 1
            sheet.append(data)
            
            # Set formula cell to wrap text and preserve line breaks
            formula_cell = sheet.cell(row=row_index, column=2)  # Column 2 is for formula
            formula_cell.alignment = Alignment(wrap_text=True)

            # Optionally, auto-size the columns
            for col in range(1, 4):
                sheet.column_dimensions[get_column_letter(col)].width = 50

        # Save the Excel file
        workbook.save(output_excel)
        logging.info(f"Excel file saved at {output_excel}")
    except Exception as e:
        logging.error(f"Error writing to Excel: {e}")

def process_htm_reports(input_directory, output_excel):
    all_extracted_data = []
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".htm"):
                file_path = os.path.join(root, file)
                extracted_data = extract_data_from_htm(file_path)
                all_extracted_data.extend(extracted_data)

    if all_extracted_data:
        write_to_excel(all_extracted_data, output_excel)
    else:
        logging.warning("No data extracted from the provided .htm files.")

# Example usage
if __name__ == "__main__":
    input_directory = './input_htm'
    output_excel = './output/formula_report.xlsx'

    process_htm_reports(input_directory, output_excel)
```

---

### **Step 3: Run the Script**

To run the script:
1. Open your terminal (or command prompt).
2. Navigate to the directory where the script is located using the `cd` command:
   ```bash
   cd C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\05htmtoexcelformula
   ```

3. Run the script by typing:
   ```bash
   python formula_extractor.py
   ```

### **Expected Output:**
- The script will process all `.htm` files inside the `input_htm` folder.
- It will automatically detect the encoding of each file.
- The extracted rule descriptions and formulas will be written into an Excel file with proper multi-line formatting.
- The Excel file will be saved in the `output` folder with the name `formula_report.xlsx`.

---

## **5. Code Explanation**

### **Key Components of the Code:**

1. **Encoding Detection**:
   - The `detect_encoding()` function uses `chardet` to analyze the file's bytes and return the detected encoding.
   
2. **HTML Parsing (BeautifulSoup)**:
   - The script reads each `.htm` file and uses `BeautifulSoup` to find `<h3>` tags for rule descriptions and `<pre>` tags for formulas.
   
3. **Data Extraction**:
   - The `extract_data_from_htm()` function collects the extracted rule descriptions and formulas into a list.

4. **Writing to Excel (openpyxl)**:
   - The `write_to_excel()` function writes the extracted data to an Excel file and ensures that formulas are displayed with line breaks using the `wrap_text=True` property.

5. **Column Sizing**:
   - Column widths are adjusted to 50 characters to ensure that the content is readable, and formulas are not truncated.

---

## **6. Customization Options**

### **Input/Output Paths**:
- By default, the script looks for `.htm` files in the `input_htm` folder and saves the Excel file to the `output` folder.
- You can change these paths in the script by modifying the `input_directory` and `output_excel` variables.

---

## **7. Troubleshooting**

### **Encoding Issues**:
- If you still encounter encoding issues, try running the `chardet` detection manually to check the detected encoding for specific files.

---

## **8. Conclusion**

The **HTML Formula Extraction to Excel Tool with Automatic Encoding Detection** automates the process of extracting rule descriptions and formulas from static HTML reports and writing them into an Excel file. The added functionality of automatic encoding detection ensures smooth handling of files with different encodings.

