import re
import os
import pandas as pd
from bs4 import BeautifulSoup
import html2text
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from multiprocessing import Pool, cpu_count

# Category mappings to classify rule names
CATEGORY_MAPPING = {
    'queue': 'Queue Rule',
    'component': 'Component Rule',
    'page': 'Page Layout / Design Rule',
    'banner': 'Banner Configuration',
    'document': 'Document Management',
}

def extract_rules_from_html_file(input_file):
    """Extracts rules and their formulas from nested HTML structures."""
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as file:
            soup = BeautifulSoup(file, 'lxml')

        extracted_data = []

        # Extract content from all <pre> and <div> tags where rules may reside
        content_blocks = soup.find_all(['pre', 'div'])

        for block in content_blocks:
            # Convert to plain text
            plain_text = html2text.html2text(block.get_text())

            # Find all rules and formulas within the block
            rule_blocks = re.findall(
                r'(R\d+|F\d+)\s+([\w_]+)\s*([\s\S]*?)(?=R\d+|F\d+|\Z)', 
                plain_text, 
                re.DOTALL
            )

            for rule_id, rule_name, content in rule_blocks:
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
    """Extracts the formula from the content block."""
    match = re.search(r'Formula:\s*(.*)', content, re.DOTALL)
    return match.group(1).strip() if match else 'N/A'

def categorize_rule(rule_name):
    """Classifies the rule name into categories."""
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

    # Use multiprocessing to handle large files faster
    with Pool(cpu_count()) as pool:
        all_data = pool.map(extract_rules_from_html_file, files)

    # Flatten the list of results
    flattened_data = [item for sublist in all_data for item in sublist]
    df = pd.DataFrame(flattened_data, columns=['Rule ID', 'Rule Name', 'Formula', 'Category'])

    # Save to Excel
    df.to_excel(output_file, index=False)
    print(f"Rules extracted and saved to {output_file}")

    # Apply wrap text to the formula column
    apply_wrap_text(output_file)

def apply_wrap_text(file_path):
    """Applies wrap text formatting to the Formula column in Excel."""
    wb = load_workbook(file_path)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=3, max_col=3):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True)

    wb.save(file_path)
    print("Wrap text applied to the Formula column.")

# Define paths
input_folder = '../input'
output_folder = '../output'
output_file = os.path.join(output_folder, 'extracted_rules.xlsx')

if __name__ == '__main__':
    # Run the extraction
    extract_rules_from_folder(input_folder, output_file)
