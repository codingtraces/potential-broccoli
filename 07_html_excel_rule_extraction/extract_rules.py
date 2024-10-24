import os
import re
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

def parse_rule(tag):
    """Extract rule ID, name, and formula."""
    header = tag.find('h3')
    if header and header.get_text(strip=True).startswith('R'):
        rule_id, rule_name = parse_rule_name(header.get_text(strip=True))
        formula = tag.find('div', class_='formula').get_text('\n', strip=False)
        category = categorize_rule(rule_name)
        return (rule_id, rule_name, formula, category)
    return None

def parse_rule_name(text):
    """Extract rule ID and name from the text."""
    match = re.match(r"(R\d+)\s*(.*)", text)
    if match:
        return match.group(1), match.group(2)
    return "UNKNOWN", "UNKNOWN_RULE"

def categorize_rule(rule_name):
    """Categorize rules based on keywords."""
    categories = {
        "Queue": "Queue Rule",
        "Page": "Page Rule",
        "Component": "Component Rule",
        "Document": "Document Rule",
        "Design": "Page Design"
    }
    for keyword, category in categories.items():
        if keyword in rule_name:
            return category
    return "Uncategorized"

def extract_rules(file_path):
    """Extract rules from HTML files."""
    encoding = detect_encoding(file_path)
    rules = []
    try:
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            tags = soup.find_all('div', class_='rule')
            for tag in tags:
                rule_data = parse_rule(tag)
                if rule_data:
                    rules.append(rule_data)
    except Exception as e:
        logging.error(f"Error extracting rules from {file_path}: {e}")
    return rules

def write_to_excel(data, output_file):
    """Write extracted rules to an Excel file."""
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Rules'
    sheet.append(['Rule ID', 'Rule Name', 'Formula', 'Category'])

    for row in data:
        sheet.append(row)
        sheet.cell(sheet.max_row, 3).alignment = Alignment(wrap_text=True)
        sheet.cell(sheet.max_row, 3).font = Font(name='Courier New')

    for col in range(1, 5):
        sheet.column_dimensions[get_column_letter(col)].width = 50

    workbook.save(output_file)
    logging.info(f"Saved rules report to {output_file}")

def process_rules(input_dir, output_file):
    """Process all HTML files in the input directory."""
    all_rules = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(('.html', '.htm')):
                file_path = os.path.join(root, file)
                logging.info(f"Processing {file_path}")
                rules = extract_rules(file_path)
                all_rules.extend(rules)

    if all_rules:
        write_to_excel(all_rules, output_file)
    else:
        logging.warning("No rules found.")

if __name__ == "__main__":
    input_dir = './input_htm'
    output_file = './output/rules_report.xlsx'
    process_rules(input_dir, output_file)
