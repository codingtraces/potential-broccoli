import os
import logging
import chardet
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_encoding(file_path):
    """Detect encoding using chardet."""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(1024 * 1024)  # Read 1MB for encoding detection
            result = chardet.detect(raw_data)
            return result.get('encoding', 'utf-8')
    except Exception as e:
        logging.error(f"Error detecting encoding: {e}")
        return 'utf-8'

def extract_function(tag):
    """Extract function name and formula."""
    header = tag.find('h3')
    if header and header.get_text(strip=True).startswith('F'):
        func_name = header.get_text(strip=True)
        formula = tag.find('div', class_='formula').get_text('\n', strip=False)
        return (func_name, formula)
    return None

def extract_functions(file_path):
    """Extract functions from HTML."""
    encoding = detect_encoding(file_path)
    functions = []
    try:
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            tags = soup.find_all('div', class_='rule')
            for tag in tags:
                func_data = extract_function(tag)
                if func_data:
                    functions.append(func_data)
    except Exception as e:
        logging.error(f"Error extracting functions from {file_path}: {e}")
    return functions

def write_to_excel(data, output_file):
    """Write extracted functions to an Excel file."""
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Functions'
    sheet.append(['Function Name', 'Formula'])

    for row in data:
        sheet.append(row)
        sheet.cell(sheet.max_row, 2).alignment = Alignment(wrap_text=True)
        sheet.cell(sheet.max_row, 2).font = Font(name='Courier New')

    for col in range(1, 3):
        sheet.column_dimensions[get_column_letter(col)].width = 50

    workbook.save(output_file)
    logging.info(f"Saved functions report to {output_file}")

def process_functions(input_dir, output_file):
    """Process all HTML files in the input directory."""
    all_functions = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(('.html', '.htm')):
                file_path = os.path.join(root, file)
                logging.info(f"Processing {file_path}")
                functions = extract_functions(file_path)
                all_functions.extend(functions)

    if all_functions:
        write_to_excel(all_functions, output_file)
    else:
        logging.warning("No functions found.")

if __name__ == "__main__":
    input_dir = './input_htm'
    output_file = './output/functions_report.xlsx'
    process_functions(input_dir, output_file)
