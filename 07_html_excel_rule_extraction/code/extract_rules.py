import re
import os
import pandas as pd
from bs4 import BeautifulSoup
import html2text
from openpyxl import load_workbook
from openpyxl.styles import Alignment

# Define category mappings for rule names
CATEGORY_MAPPING = {
    'queue': 'Queue Rule',
    'component': 'Component Rule',
    'page': 'Page Layout / Design Rule',
    'banner': 'Banner Configuration',
    'document': 'Document Management',
}

# Enhanced regex to capture everything between two rule IDs
RULE_BLOCK_PATTERN = r'(R\d+|F\d+)\s+([\w_]+)\s*([\s\S]*?)(?=(R\d+|F\d+|\Z))'

def extract_rules_from_html_file(input_file):
    """Extracts rules, their names, and formulas from a single HTML file."""
    with open(input_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Convert HTML content to plain text
    plain_text = html2text.html2text(str(soup))

    # Extract all rule blocks between rule IDs
    rule_blocks = re.findall(RULE_BLOCK_PATTERN, plain_text)

    extracted_data = []
    for block in rule_blocks:
        rule_id, rule_name, content = block[:3]  # Extract the rule and its content
        formula = extract_formula(content)  # Extract formula from content
        category = categorize_rule(rule_name)

        extracted_data.append({
            'Rule ID': rule_id,
            'Rule Name': rule_name,
            'Formula': formula,
            'Category': category
        })

    return extracted_data

def extract_formula(content):
    """Extracts the formula from the rule content."""
    match = re.search(r'Formula:\s*(.*)', content, re.DOTALL)  # Capture multiline formulas
    return match.group(1).strip() if match else 'N/A'

def categorize_rule(rule_name):
    """Categorizes rules based on their names."""
    rule_name = rule_name.lower()
    for keyword, category in CATEGORY_MAPPING.items():
        if keyword in rule_name:
            return category
    return 'General Business Rule'

def extract_rules_from_folder(input_folder, output_file):
    """Processes all HTML files in the input folder and generates an Excel report."""
    all_data = []

    # Loop through HTML files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.html'):
            input_file = os.path.join(input_folder, filename)
            print(f"Processing {input_file}...")
            data = extract_rules_from_html_file(input_file)
            all_data.extend(data)

    # Save results to an Excel file
    df = pd.DataFrame(all_data, columns=['Rule ID', 'Rule Name', 'Formula', 'Category'])
    df.to_excel(output_file, index=False)
    print(f"Rules extracted and saved to {output_file}")
    apply_wrap_text(output_file)

def apply_wrap_text(file_path):
    """Applies wrap text to the Formula column in Excel."""
    wb = load_workbook(file_path)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=3, max_col=3):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True)

    wb.save(file_path)
    print("Wrap text applied to the Formula column.")

# Define input and output paths
input_folder = '../input'  # HTML input folder
output_folder = '../output'  # Excel output folder
output_file = os.path.join(output_folder, 'extracted_rules.xlsx')

# Run the extraction
extract_rules_from_folder(input_folder, output_file)
