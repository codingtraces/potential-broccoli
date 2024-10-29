import os
import re
import pandas as pd
from bs4 import BeautifulSoup

# Ensure xlsxwriter is installed
try:
    import xlsxwriter
except ImportError:
    print("Error: 'xlsxwriter' module not found. Install it using 'pip install xlsxwriter'.")
    exit(1)

# Define input and output directories
INPUT_FOLDER = "../input"
OUTPUT_FOLDER = "../output"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "rules_report.xlsx")

def extract_rules_and_functions(html_file):
    try:
        with open(html_file, 'r', encoding='iso-8859-1') as f:
            soup = BeautifulSoup(f, 'html.parser')

        rules = []
        functions = []

        # Extract rules
        rule_blocks = soup.find_all('div', align='left')
        for block in rule_blocks:
            rule_id = re.search(r'#Rule(\d+)', str(block))
            if rule_id:
                rule_name_tag = block.find('strong')
                rule_name = rule_name_tag.get_text(strip=True) if rule_name_tag else "Unknown"
                formula = block.find('pre').get_text() if block.find('pre') else "No formula found"
                
                # Determine category based on rule name or keywords
                category = "Page Design"  # Default category
                if "Queue" in rule_name:
                    category = "Queue"
                elif "Component" in rule_name:
                    category = "Component"
                elif "Page Rule" in rule_name:
                    category = "Page Rule"
                elif "Document Rule" in rule_name:
                    category = "Document Rule"
                elif "Search Online" in rule_name:
                    category = "Search Online"
                
                rules.append([rule_id.group(1), rule_name, formula, category])

            # Extract functions
            function_id = re.search(r'#Function(\d+)', str(block))
            if function_id:
                function_name_tag = block.find('strong')
                function_name = function_name_tag.get_text(strip=True) if function_name_tag else "Unknown"
                function_formula = block.find('pre').get_text() if block.find('pre') else "No formula found"
                functions.append([function_id.group(1), function_name, function_formula])

        return rules, functions

    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return [], []

def generate_excel_report(rules, functions):
    try:
        with pd.ExcelWriter(OUTPUT_FILE, engine='xlsxwriter') as writer:
            # Create a DataFrame for rules and write to Excel
            df_rules = pd.DataFrame(rules, columns=['Rule ID', 'Rule Name', 'Formula', 'Category'])
            df_rules.to_excel(writer, sheet_name='Rules', index=False)

            # Create a DataFrame for functions and write to Excel
            df_functions = pd.DataFrame(functions, columns=['Function ID', 'Function Name', 'Function Formula'])
            df_functions.to_excel(writer, sheet_name='Functions', index=False)

            # Apply formatting to wrap text in the Excel sheet
            workbook = writer.book
            for sheet_name in ['Rules', 'Functions']:
                worksheet = writer.sheets[sheet_name]
                wrap_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})
                worksheet.set_column('A:D', 30, wrap_format)

        print(f"Excel report generated successfully at: {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error generating Excel report: {e}")

if __name__ == "__main__":
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
            rules, functions = extract_rules_and_functions(file_path)
            all_rules.extend(rules)
            all_functions.extend(functions)

    if not all_rules and not all_functions:
        print("No rules or functions extracted from the provided HTML files.")
    else:
        generate_excel_report(all_rules, all_functions)
