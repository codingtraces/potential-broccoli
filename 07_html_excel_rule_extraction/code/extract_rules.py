import os
import re
import pandas as pd
from html import unescape
from bs4 import BeautifulSoup

# Configuration: Keywords, Identifiers, and Section Headers
CATEGORY_PATTERNS = {
    'Queue': r'(?i)queue',
    'Component': r'(?i)component',
    'Page Rule': r'(?i)page',
    'Banner': r'(?i)banner',
    'Batch': r'(?i)batch',
    'Document Rule': r'(?i)document'
}

SECTION_HEADERS = {
    'rules': 'Rules List',
    'functions': 'Function List'
}

RULE_IDENTIFIER = r'R(\d+)'  # Updated to capture all patterns like R1, R12, R1234
FUNCTION_IDENTIFIER = r'F(\d+)'

INPUT_FOLDER = "../input"
OUTPUT_FOLDER = "../output"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "rules_report.xlsx")

def classify_category(name):
    """Classify the item based on matching keywords."""
    matched_category = "General Rule"  # Default category
    for category, pattern in CATEGORY_PATTERNS.items():
        if re.search(pattern, name):
            matched_category = category
            break  # Stop once a match is found to prioritize the first match
    return matched_category

import html2text

def extract_formula(block):
    """Extract formula using html2text to preserve original formatting, handling lengthy blocks."""
    formula_tag = block.find('pre')
    if formula_tag:
        # Initialize the HTML2Text converter to retain alignment and disable word wrapping.
        converter = html2text.HTML2Text()
        converter.body_width = 0  # Ensure no word wrapping occurs.

        # Preserve long formulas with exact formatting
        formula = converter.handle(str(formula_tag))

        # Clean up and ensure no extra leading/trailing newlines or spaces
        return formula.rstrip('\n')  # Use rstrip to remove only trailing newlines
    return "No formula found"


def extract_rules(block):
    """Extract rules from an HTML block."""
    strong_tag = block.find('strong')
    if strong_tag:
        rule_name = strong_tag.get_text(strip=True)
        rule_match = re.search(RULE_IDENTIFIER, rule_name)
        if rule_match:
            rule_id = rule_match.group(1)
            formula = extract_formula(block)
            category = classify_category(rule_name)
            return [rule_id, rule_name, formula, category]
    return None

def extract_functions(block):
    """Extract functions from an HTML block."""
    strong_tag = block.find('strong')
    if strong_tag:
        function_name = strong_tag.get_text(strip=True)
        function_match = re.search(FUNCTION_IDENTIFIER, function_name)
        if function_match:
            function_id = function_match.group(1)
            formula = extract_formula(block)
            return [function_id, function_name, formula]
    return None

def process_html_file(html_file):
    """Extract rules and functions from a given HTML file."""
    try:
        with open(html_file, 'r', encoding='iso-8859-1') as f:
            soup = BeautifulSoup(f, 'html.parser')

        rules, functions = [], []

        # Iterate over all 'div' blocks
        for block in soup.find_all('div', align='left'):
            section_name = block.find_previous('p').get_text(strip=True).lower() if block.find_previous('p') else ""

            if SECTION_HEADERS['rules'].lower() in section_name:
                rule = extract_rules(block)
                if rule:
                    rules.append(rule)

            elif SECTION_HEADERS['functions'].lower() in section_name:
                function = extract_functions(block)
                if function:
                    functions.append(function)

        return rules, functions

    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return [], []

def write_to_excel(writer, data, sheet_name, columns):
    """Write data to an Excel sheet with proper formatting."""
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(writer, sheet_name=sheet_name, index=False)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    wrap_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})
    worksheet.set_column('A:D', 30, wrap_format)

def generate_excel_report(rules, functions):
    """Generate an Excel report with categorized rules and functions."""
    try:
        with pd.ExcelWriter(OUTPUT_FILE, engine='xlsxwriter') as writer:
            write_to_excel(writer, rules, 'Rules', ['Rule ID', 'Rule Name', 'Formula', 'Category'])
            write_to_excel(writer, functions, 'Functions', ['Function ID', 'Function Name', 'Formula'])

        print(f"Excel report generated successfully at: {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error generating Excel report: {e}")

def main():
    """Main function to process all HTML files and generate the report."""
    if not os.path.exists(INPUT_FOLDER):
        print("Input folder not found.")
        exit(1)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    all_rules, all_functions = [], []

    for file_name in os.listdir(INPUT_FOLDER):
        if file_name.endswith(('.html', '.htm')):
            file_path = os.path.join(INPUT_FOLDER, file_name)
            print(f"Processing file: {file_path}")
            rules, functions = process_html_file(file_path)
            all_rules.extend(rules)
            all_functions.extend(functions)

    if all_rules or all_functions:
        generate_excel_report(all_rules, all_functions)
    else:
        print("No rules or functions extracted from the provided HTML files.")

if __name__ == "__main__":
    main()
