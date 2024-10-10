import os
from bs4 import BeautifulSoup
import openpyxl
import logging
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
import chardet
import re

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_encoding(file_path):
    """Detect the encoding of the file using chardet."""
    try:
        with open(file_path, 'rb') as raw_file:
            raw_data = raw_file.read(1024 * 1024)  # Read the first 1MB to detect encoding
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            logging.info(f"Detected encoding for {file_path}: {encoding}")
            return encoding
    except Exception as e:
        logging.error(f"Error detecting encoding for {file_path}: {e}")
        return 'utf-8'  # Default to utf-8 if detection fails

def extract_formula_patterns(soup):
    """Extract rule-formula pairs from the parsed HTML (BeautifulSoup)."""
    extracted_data = []

    # Find all <pre> tags as they typically contain formulas
    formula_tags = soup.find_all('pre')

    for formula_tag in formula_tags:
        formula_text = formula_tag.get_text(strip=True)
        parent = formula_tag.find_previous(['h3', 'strong'])

        if parent:
            # Check if parent has a rule ID and name
            rule_text = parent.get_text(strip=True)
            match = re.match(r"(R\d+)\s*(.*)", rule_text)
            if match:
                rule_id = match.group(1)
                rule_name = match.group(2)
            else:
                rule_id = "UNKNOWN"
                rule_name = "UNKNOWN_RULE"
        else:
            rule_id = "UNKNOWN"
            rule_name = "UNKNOWN_RULE"

        # Clean formula text and append to extracted data
        formula_text = clean_formula_block(formula_text)
        extracted_data.append((rule_id, rule_name, formula_text))

    return extracted_data

def clean_formula_block(formula_text):
    """Clean extra spaces and newlines in formula text."""
    return ' '.join(formula_text.split()).replace(' ENDIF', '\nENDIF')

def extract_data_from_htm(file_path):
    """Extract rule ID, rule name, and formulas from an HTML file by searching for patterns."""
    extracted_data = []
    try:
        # Detect the file's encoding
        encoding = detect_encoding(file_path)
        logging.info(f"Processing {file_path}")

        # Open the file with the detected encoding
        with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
            soup = BeautifulSoup(file, 'html.parser')

            # Extract rule-formula pairs
            patterns_found = extract_formula_patterns(soup)

            if patterns_found:
                logging.info(f"Found {len(patterns_found)} rule-formula pairs in {file_path}")
                for rule_id, rule_name, formula in patterns_found:
                    extracted_data.append((rule_id, rule_name, formula, file_path))
                    logging.info(f"Extracted formula: {rule_id} {rule_name} = {formula} from {file_path}")
            else:
                logging.warning(f"No formulas found in {file_path}")

    except Exception as e:
        logging.error(f"Error parsing file {file_path}: {e}")
    return extracted_data

def write_to_excel(extracted_data, output_excel):
    """Write the extracted data into an Excel file."""
    try:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Extracted Formulas'

        # Write headers
        headers = ['Rule ID', 'Rule Name', 'Formula', 'Source File']
        sheet.append(headers)

        for row_index, data in enumerate(extracted_data, start=2):  # start=2 to account for headers in row 1
            sheet.append([data[0], data[1], data[2], data[3]])  # rule ID, rule name, formula, source file

            # Set formula cell to wrap text and preserve line breaks
            formula_cell = sheet.cell(row=row_index, column=3)  # Column 3 is for formula
            formula_cell.alignment = Alignment(wrap_text=True)

            # Auto-size the columns for readability
            for col in range(1, 5):
                sheet.column_dimensions[get_column_letter(col)].width = 50

        # Save the Excel file
        workbook.save(output_excel)
        logging.info(f"Excel file saved at {output_excel}")
    except Exception as e:
        logging.error(f"Error writing to Excel: {e}")

def process_htm_reports(input_directory, output_excel):
    """Process all HTML reports in the input directory."""
    all_extracted_data = []
    total_files = sum([len(files) for r, d, files in os.walk(input_directory)])
    file_count = 0

    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".htm") or file.endswith(".html"):  # Handling both .htm and .html files
                file_path = os.path.join(root, file)
                file_count += 1
                logging.info(f"Processing file {file_count}/{total_files}: {file_path}")
                try:
                    extracted_data = extract_data_from_htm(file_path)
                    all_extracted_data.extend(extracted_data)  # Append data from each file to the master list
                except Exception as e:
                    logging.error(f"Failed to process file {file_path}: {e}")

    if all_extracted_data:
        write_to_excel(all_extracted_data, output_excel)
    else:
        logging.warning("No data extracted from the provided .htm files.")

# Example usage
if __name__ == "__main__":
    input_directory = './input_htm'
    output_excel = './output/formula_report.xlsx'

    # Process reports and generate Excel
    try:
        process_htm_reports(input_directory, output_excel)
    except Exception as e:
        logging.error(f"Critical error in processing: {e}")
