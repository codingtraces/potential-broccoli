import os
import re
import pandas as pd
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
    'functions': 'Function List',
    'application_report': 'Application Report'
}

RULE_IDENTIFIER = r'#Rule(\d+)'
FUNCTION_IDENTIFIER = r'#Function(\d+)'

INPUT_FOLDER = "../input"
OUTPUT_FOLDER = "../output"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "rules_report.xlsx")

# Classify based on name patterns
def classify_category(name):
    """Classify the item based on matching keywords."""
    matched_category = "Page Design"  # Default category if no keyword matches

    for category, pattern in CATEGORY_PATTERNS.items():
        if re.search(pattern, name):
            return category

    return matched_category

# Extract rules with proper categorization
def extract_rules(block):
    """Extract rules from HTML blocks."""
    rule_match = re.search(RULE_IDENTIFIER, str(block), re.IGNORECASE)
    if rule_match:
        rule_name = block.find('strong').get_text(strip=True) if block.find('strong') else "Unknown"
        formula = extract_formula(block)
        category = classify_category(rule_name)
        return [rule_match.group(1), rule_name, formula, category]
    return None

# Extract functions
def extract_functions(block):
    """Extract functions from HTML blocks."""
    function_match = re.search(FUNCTION_IDENTIFIER, str(block), re.IGNORECASE)
    if function_match:
        function_name = block.find('strong').get_text(strip=True) if block.find('strong') else "Unknown"
        formula = extract_formula(block)
        return [function_match.group(1), function_name, formula]
    return None

# Extract and preserve the formula's original structure
def extract_formula(block):
    """Extract the formula text while maintaining its formatting."""
    formula_tag = block.find('pre')
    return formula_tag.get_text() if formula_tag else "No formula found"

# Process a single HTML file
def process_html_file(html_file):
    """Extract all rules and functions from a given HTML file."""
    try:
        with open(html_file, 'r', encoding='iso-8859-1') as f:
            soup = BeautifulSoup(f, 'html.parser')

        rules, functions = [], []

        # Extract all sections
        for block in soup.find_all('div', align='left'):
            # Handle section names dynamically
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

# Write the extracted data into an Excel sheet
def write_to_excel(writer, data, sheet_name, columns):
    """Write extracted data into Excel with text wrapping."""
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(writer, sheet_name=sheet_name, index=False)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    wrap_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})
    worksheet.set_column('A:D', 30, wrap_format)

# Generate the Excel report
def generate_excel_report(rules, functions):
    """Generate an Excel report with categorized rules and functions."""
    try:
        with pd.ExcelWriter(OUTPUT_FILE, engine='xlsxwriter') as writer:
            write_to_excel(writer, rules, 'Rules', ['Rule ID', 'Rule Name', 'Formula', 'Category'])
            write_to_excel(writer, functions, 'Functions', ['Function ID', 'Function Name', 'Formula'])

        print(f"Excel report generated successfully at: {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error generating Excel report: {e}")

# Main program flow
def main():
    """Main function to process all HTML files and generate the report."""
    if not os.path.exists(INPUT_FOLDER):
        print("Input folder not found.")
        exit(1)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    all_rules, all_functions = [], []

    # Process each HTML file in the input folder
    for file_name in os.listdir(INPUT_FOLDER):
        if file_name.endswith(('.html', '.htm')):
            file_path = os.path.join(INPUT_FOLDER, file_name)
            print(f"Processing file: {file_path}")
            rules, functions = process_html_file(file_path)
            all_rules.extend(rules)
            all_functions.extend(functions)

    # Generate Excel report if data exists
    if all_rules or all_functions:
        generate_excel_report(all_rules, all_functions)
    else:
        print("No rules or functions extracted from the provided HTML files.")

# Entry point
if __name__ == "__main__":
    main()
