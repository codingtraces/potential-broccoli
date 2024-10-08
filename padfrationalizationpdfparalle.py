import os
import fitz  # PyMuPDF for analyzing structure and layout
from datetime import datetime
from collections import defaultdict
import pandas as pd
import concurrent.futures
import traceback

# Helper function to normalize text for comparison
def normalize_text(text):
    return text.lower().strip()

# Function to analyze a single PDF structure (text, headers, footers, etc.)
def analyze_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        if doc.is_encrypted:
            print(f"PDF {file_path} is encrypted. Skipping...")
            return None

        structure_report = {
            "headers": set(),
            "footers": set(),
            "images": set(),
            "tables": set(),
            "text_blocks": set()
        }

        for page_number in range(len(doc)):
            try:
                page = doc.load_page(page_number)
            except Exception as e:
                print(f"Error reading page {page_number + 1} of {file_path}: {e}")
                continue

            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if "image" in block:
                    structure_report["images"].add(f"Image at position {block['bbox']}")
                if "lines" in block:
                    block_text = "\n".join([span["text"] for line in block["lines"] for span in line["spans"]]).strip()
                    normalized_text = normalize_text(block_text)

                    # Filter out small blocks of text less than 100 characters
                    if len(block_text) < 100:
                        continue

                    # Simple logic to categorize headers, footers, and text blocks
                    if block['bbox'][1] < 100:
                        structure_report["headers"].add(normalized_text)
                    elif block['bbox'][1] > page.rect.height - 100:
                        structure_report["footers"].add(normalized_text)
                    else:
                        structure_report["text_blocks"].add(normalized_text)

            # Add logic to detect tables (many line breaks, uniform text)
            for block in structure_report["text_blocks"]:
                if "table" in block or block.count("\n") > 5:
                    structure_report["tables"].add(block)

        return structure_report

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        traceback.print_exc()
        return None

# Function to compare PDFs and find common elements
def compare_pdf_structures(pdf_reports):
    common_elements = {
        "headers": defaultdict(set),
        "footers": defaultdict(set),
        "text_blocks": defaultdict(set),
        "tables": defaultdict(set),
        "images": defaultdict(set)
    }

    for pdf_name, report in pdf_reports.items():
        for element_type in common_elements.keys():
            for element in report[element_type]:
                common_elements[element_type][element].add(pdf_name)

    return common_elements

# Function to generate HTML report for common elements
def generate_comparison_html_report(common_elements, output_folder):
    html_content = f"""
    <html>
    <head>
        <title>Template Reusability Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            h2, h3 {{ color: #555; }}
            p {{ margin-bottom: 10px; }}
            .section {{ margin-bottom: 40px; }}
        </style>
    </head>
    <body>
        <h1>Template Reusability Report</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """

    def add_section(title, elements):
        html = f"<h2>{title}</h2>"
        if elements:
            for item, pdfs in elements.items():
                if len(pdfs) > 1:
                    html += f"<p><strong>{item[:200]}...</strong> - Found in: {', '.join(pdfs)}</p>"
        else:
            html += f"<p>No common {title.lower()} found.</p>"
        return html

    html_content += add_section("Common Headers Across PDFs", common_elements["headers"])
    html_content += add_section("Common Footers Across PDFs", common_elements["footers"])
    html_content += add_section("Common Paragraphs/Text Blocks Across PDFs", common_elements["text_blocks"])
    html_content += add_section("Common Tables Across PDFs", common_elements["tables"])
    html_content += add_section("Common Images Across PDFs", common_elements["images"])

    html_content += "</body></html>"

    html_filename = os.path.join(output_folder, "template_reusability_report.html")
    with open(html_filename, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print(f"Template reusability report generated: {html_filename}")

# Function to generate Excel report
def generate_comparison_excel_report(common_elements, output_folder):
    rows = []

    for element_type, elements in common_elements.items():
        for item, pdfs in elements.items():
            if len(pdfs) > 1:
                rows.append([element_type, item[:200], ', '.join(pdfs)])

    df = pd.DataFrame(rows, columns=["Type", "Content (first 200 characters)", "Found in PDFs"])
    
    excel_filename = os.path.join(output_folder, "template_reusability_report.xlsx")
    df.to_excel(excel_filename, index=False)
    
    print(f"Excel report generated: {excel_filename}")

# Function to handle the main comparison between single PDF and multiple PDFs with parallel processing
def analyze_single_vs_all(single_pdf_folder, all_pdf_folder, output_folder):
    single_pdf = os.path.join(single_pdf_folder, os.listdir(single_pdf_folder)[0])
    all_pdf_files = [os.path.join(all_pdf_folder, f) for f in os.listdir(all_pdf_folder) if f.lower().endswith('.pdf')]

    if not all_pdf_files:
        print("No PDF files found in the allpdf folder.")
        return

    print(f"Analyzing single PDF: {single_pdf}")
    single_pdf_report = analyze_pdf(single_pdf)
    
    if single_pdf_report is None:
        print("Failed to process the single PDF.")
        return

    pdf_reports = {}

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(analyze_pdf, pdf): pdf for pdf in all_pdf_files}
        for future in concurrent.futures.as_completed(futures):
            pdf = futures[future]
            try:
                report = future.result()
                if report:
                    pdf_name = os.path.basename(pdf)
                    pdf_reports[pdf_name] = report
            except Exception as exc:
                print(f"{pdf} generated an exception: {exc}")
                with open(os.path.join(output_folder, "processing_log.txt"), "a") as log_file:
                    log_file.write(f"{pdf} failed with error: {exc}\n")
    
    # Compare and generate reports
    common_elements = compare_pdf_structures(pdf_reports)
    generate_comparison_html_report(common_elements, output_folder)
    generate_comparison_excel_report(common_elements, output_folder)

# Main execution
if __name__ == "__main__":
    import sys
    single_pdf_folder = r"C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdfratioanlization\v2\singlepdf"
    all_pdf_folder = r"C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdfratioanlization\v2\allpdf"
    output_folder = r"C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdfratioanlization\v2\result"

    os.makedirs(output_folder, exist_ok=True)
    
    print(f"Starting analysis...")
    analyze_single_vs_all(single_pdf_folder, all_pdf_folder, output_folder)
    print("Analysis complete.")
