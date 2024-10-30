import re
import os
import pandas as pd
from bs4 import BeautifulSoup
import html2text
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from multiprocessing import Pool, cpu_count

# Category mappings for rule names
CATEGORY_MAPPING = {
    'queue': 'Queue Rule',
    'component': 'Component Rule',
    'page': 'Page Layout / Design Rule',
    'banner': 'Banner Configuration',
    'document': 'Document Management',
}

# Regex pattern to match rules and content blocks between them
RULE_BLOCK_PATTERN = r'(R\d+|F\d+)\s+([\w_]+)\s*([\s\S]*?)(?=R\d+|F\d+|\Z)'

def extract_rules_from_html_file(input_file):
    """Extract rules, names, and formulas from a single HTML file."""
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as file:
            soup = BeautifulSoup(file, 'lxml')  # Using lxml for faster parsing
            plain_text = html2text.html2text(str(soup))

        # Extract all rule blocks between IDs
        rule_blocks = re.findall(RULE_BLOCK_PATTERN, plain_text)

        extracted_data = []
        for block in rule_blocks:
            rule_id, rule_name, content = block
            formula = extract_formula(content)
            category = categorize_rule(rule_name)

            extracted_data.append({
                'Rule ID': rule_id,
                'Rule Name': rule_name,
                'Formula': formula,
                'Category': category
            })

        return extracted_data
    except Exception as e:
        print(f"Error processing {input_file}: {e}")
        return []

def extract_formula(content):
    """Extracts the formula from the content."""
    match = re.search(r'Formula:\s*(.*)', content, re.DOTALL)
    return match.group(1).strip() if match else 'N/A'

def categorize_rule(rule_name):
    """Categorizes rules based on keywords."""
    rule_name = rule_name.lower()
    for keyword, category in CATEGORY_MAPPING.items():
        if keyword in rule_name:
            return category
    return 'General Business Rule'

def extract_rules_from_folder(input_folder, output_file):
    """Processes all HTML files and generates an Excel report."""
    files = [
        os.path.join(input_folder, filename)
        for filename in os.listdir(input_folder) if filename.endswith('.html')
    ]

    # Use multiprocessing to process multiple files in parallel
    with Pool(cpu_count()) as pool:
        all_data = pool.map(extract_rules_from_html_file, files)

    # Flatten the results and save to Excel
    flattened_data = [item for sublist in all_data for item in sublist]
    df = pd.DataFrame(flattened_data, columns=['Rule ID', 'Rule Name', 'Formula', 'Category'])
    df.to_excel(output_file, index=False)
    print(f"Rules extracted and saved to {output_file}")

    # Apply wrap text to the formula column
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

# Define paths based on server environment
input_folder = '../input'
output_folder = '../output'
output_file = os.path.join(output_folder, 'extracted_rules.xlsx')

if __name__ == '__main__':
    # Run the extraction process
    extract_rules_from_folder(input_folder, output_file)
