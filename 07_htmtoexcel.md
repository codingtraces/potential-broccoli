Here’s a **complete documentation** for your **HTML Formula Extraction to Excel Tool**, including setup, installation instructions, and detailed steps for running the tool.

---

# **HTML Formula Extraction to Excel Tool Documentation**

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

The **HTML Formula Extraction to Excel Tool** is a Python script that extracts formulas from static `.htm` reports and writes them into an Excel file while preserving the original multi-line formatting of the formulas. The tool is particularly useful for processing business logic or rule-based reports stored in static HTML files that cannot be directly inspected.

### **Key Features:**
- Parses HTML reports to extract rule descriptions and formulas.
- Outputs the extracted data into a neatly formatted Excel file.
- Preserves the original line breaks in the formulas.
- Customizable to handle different HTML structures and formats.

---

## **2. Prerequisites**

Before setting up and running the tool, ensure that you have the following installed on your system:

- **Python 3.6 or later**: You can download Python from [python.org](https://www.python.org/downloads/).
- **Required Python Libraries**:
  - `beautifulsoup4`: For parsing HTML files.
  - `openpyxl`: For writing to Excel files.

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
pip install beautifulsoup4 openpyxl
```

This installs the necessary libraries for parsing HTML files and writing to Excel.

---

## **4. Detailed Workflow**

### **Step 1: Directory Setup**
1. **Create a folder** on your machine where you will store the script and HTML files. For example, `C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\05htmtoexcelformula`.
   
2. **Create an input folder** inside this directory where you will place the `.htm` files:
   ```
   C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\05htmtoexcelformula\input_htm
   ```

3. **Place the HTML files** (like `Batch_BrokerManagement.htm` or other reports) into the `input_htm` folder.

4. **Create an output folder** where the Excel reports will be saved:
   ```
   C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\05htmtoexcelformula\output
   ```

### **Step 2: Python Script**
In the same directory, create a Python script file called `formula_extractor.py` and paste the following code into it:

```python
import os
from bs4 import BeautifulSoup
import openpyxl
import logging
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_data_from_htm(file_path):
    extracted_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
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
- It will extract the rule descriptions and formulas, and write them into an Excel file with proper multi-line formatting.
- The Excel file will be saved in the `output` folder with the name `formula_report.xlsx`.

---

## **5. Code Explanation**

### **Key Components of the Code:**

1. **HTML Parsing (BeautifulSoup)**:
   - The script reads each `.htm` file and uses `BeautifulSoup` to find `<h3>` tags for rule descriptions and `<pre>` tags for formulas.
   
2. **Data Extraction**:
   - The `extract_data_from_htm()` function collects the extracted rule descriptions and formulas into a list.

3. **Writing to Excel (openpyxl)**:
   - The `write_to_excel()` function writes the extracted data to an Excel file and ensures that formulas are displayed with line breaks using the `wrap_text=True` property.

4. **Column Sizing**:
   - Column widths are adjusted to 50 characters to ensure that the content is readable, and formulas are not truncated.

---

## **6. Customization Options**

### **Input/Output Paths**:
- By default, the script looks for `.htm` files in the `input_htm` folder and saves the Excel file to the `output` folder.
- You can change these paths in the script by modifying the `input_directory` and `output_excel` variables.

### **HTML Structure**:
- If your HTML reports have a different structure, you can adjust the tag selectors in the `extract_data_from_htm()` function. For example, if formulas are in a different tag (not `<pre>`), you can change the line:
   ```python
   formula_tag = section.find_next('pre')  # Modify if necessary
   ```

---

## **7. Troubleshooting**

### **1. Missing Data in Excel Report**:
- Ensure the `.htm` files follow the expected structure. If formulas or rules are in different tags, modify the HTML parsing logic.

### **2. Errors While Running the Script**:
- Make sure all required libraries (`beautifulsoup4`, `openpyxl`) are installed by running:
  ```bash
  pip install beautifulsoup4 openpyxl
  ```

### **3. Encoding Issues**:
- If you encounter encoding errors, make sure the `.htm` files are encoded in UTF-8 or change the encoding in the script:
  ```python
  with open(file_path, 'r', encoding='utf-8') as file:
      # File reading logic here
  ```

---

## **8. Conclusion**

The **HTML Formula Extraction to Excel Tool** automates the process of extracting rule descriptions and formulas from static HTML reports and writing them into an Excel file while preserving the formatting. This tool is highly customizable and can be adapted to different HTML structures or report formats, making it a valuable tool for

 automating data extraction tasks.

By following the setup and instructions in this guide, you can easily run the tool to process large numbers of HTML reports and generate structured Excel files with neatly formatted formulas.

Let me know if you need further customization or adjustments!
