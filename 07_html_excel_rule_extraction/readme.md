### **Full Documentation for HTML to Excel Report Generator**

This documentation provides an overview of the code, installation instructions, folder structure, setup, and how to run your project properly.

---

## **Overview**

This Python script:
- **Parses HTML files** to extract rules and functions.
- **Classifies rules** based on specific keywords.
- **Generates an Excel report** with two sheets: "Rules" and "Functions".
- **Formats Excel sheets** to wrap text for readability.

---

## **Prerequisites**

- Python 3.x installed on your system.
- **HTML input files** for testing.
- Libraries: `pandas`, `beautifulsoup4`, `xlsxwriter`.

---

## **Installation Instructions**

Open a terminal or command prompt and run:

```bash
# Install the required libraries
pip install pandas beautifulsoup4 xlsxwriter
```

---

## **Folder Structure**

Make sure your project follows the structure below:

```
project_root/
│
├── code/                     
│   └── main_script.py        # The provided Python script goes here
├── input/                    # Folder containing the HTML files to process
│   └── sample.html           # Example HTML file (add more files here)
├── output/                   
│   └── rules_report.xlsx     # Output Excel report will be saved here
```

- **`code/`**: Contains the Python script (your main code).
- **`input/`**: Add your `.html` or `.htm` files here to be processed.
- **`output/`**: The Excel report (`rules_report.xlsx`) will be generated in this folder.

---

## **How to Run the Code**

### Step 1: Navigate to the `code` folder
Open your terminal or command prompt and move to the `code` folder:

```bash
cd path/to/project_root/code
```

### Step 2: Run the Script
Execute the script using:

```bash
python main_script.py
```

---

## **Functionality of the Script**

1. **Extract Rules and Functions from HTML**:
   - Reads HTML files from the `input` folder.
   - Extracts **rule names**, **IDs**, **formulas**, and **categories**.
   - Identifies **functions** and their formulas.

2. **Generate Excel Report**:
   - Saves two sheets in the Excel file: **Rules** and **Functions**.
   - Applies **text wrapping** for better readability.

3. **Error Handling**:
   - Checks if the `input` folder exists; if not, displays an error.
   - Automatically creates the `output` folder if it doesn't exist.

---

## **Sample Output**

### Rules Sheet Example:
| Rule ID | Rule Name    | Formula                | Category      |
|---------|--------------|------------------------|---------------|
| 1       | Queue Rule   | IF condition THEN ...  | Queue         |
| 2       | Component1   | formula() + var ...    | Component     |

### Functions Sheet Example:
| Function ID | Function Name | Function Formula |
|-------------|---------------|------------------|
| 1           | Func1         | def func1(): ... |

---

## **Script Logic Overview**

- **Libraries Used**:
  - `os`: For folder and file operations.
  - `re`: For regular expression-based extraction.
  - `pandas`: To store data in DataFrames and write to Excel.
  - `BeautifulSoup`: To parse HTML files.
  - `xlsxwriter`: To generate and format Excel reports.

- **Core Functions**:
  - **`extract_rules_and_functions(html_file)`**:  
    Extracts rules and functions from the provided HTML file.
  - **`generate_excel_report(rules, functions)`**:  
    Creates and formats the Excel report based on the extracted data.

---

## **Handling Errors**

1. **Missing Input Folder**:
   - If the `input` folder is missing, the script will display:  
     *"Input folder not found."*

2. **Missing Libraries**:
   - If `xlsxwriter` is not installed, the script will display:  
     *"Error: 'xlsxwriter' module not found. Install it using 'pip install xlsxwriter'."*

3. **HTML File Processing Errors**:
   - If any HTML file cannot be processed, the script prints:  
     *"Error processing `<file_name>`: `<error_message>`"*

---

## **Customization**

- **Modify Input/Output Folders**:  
  Change the following variables in the script if you want to use different folders:

  ```python
  INPUT_FOLDER = "../input"
  OUTPUT_FOLDER = "../output"
  ```

- **Change Rule Categories**:  
  Update the categories assigned to rules by modifying this section:

  ```python
  if "Queue" in rule_name:
      category = "Queue"
  elif "Component" in rule_name:
      category = "Component"
  elif "Page Rule" in rule_name:
      category = "Page Rule"
  ```

---

## **Expected Output Location**

After running the script, the Excel report will be saved as:

```
output/rules_report.xlsx
```

---

## **Conclusion**

This script provides a quick and structured way to extract content from HTML files and generate well-formatted reports in Excel. With the proper folder setup and required libraries installed, it ensures easy processing and report generation. 

