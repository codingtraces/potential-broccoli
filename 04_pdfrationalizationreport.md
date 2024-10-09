### Complete Documentation for PDF Template Reusability Analyzer

---

This Python project analyzes multiple PDFs to identify reusable sections (such as headers, footers, tables, paragraphs, images) and generates a single consolidated HTML report. The report highlights common elements across the PDFs that can be reused for templates, making it easier to rationalize document structure for template creation.

---

### Features
- **PDF Structure Analysis**: Extracts headers, footers, text blocks, images, and tables from each PDF.
- **Element Comparison**: Compares elements across PDFs to find common sections that can be reused.
- **Template Reusability Report**: Generates a consolidated HTML report that identifies which sections are repeated across PDFs and lists the PDFs where those sections appear.

---

### Prerequisites

Ensure that you have the following installed before running the script:

1. **Python 3.x**: Install Python from [here](https://www.python.org/downloads/).
2. **pip**: Python's package manager, which is usually installed along with Python.

---

### Installation

#### Step 1: Install Required Libraries
You will need the following Python library:
- **PyMuPDF** (also known as `fitz`): This library is used to extract the structure from PDFs.

To install PyMuPDF, open your terminal or command prompt and run:

```bash
pip install pymupdf
```

#### Step 2: Download or Clone the Project
You can download the Python script from the repository or create a new file with the provided code in the documentation.

#### Step 3: Place Your PDFs in a Folder
Organize the PDFs you want to analyze in a folder. In this documentation, we assume the PDFs are located in:

```
C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdfratioanlization\input
```

Make sure the folder contains all the PDFs you want to analyze.

---

### How to Run the Script

#### Step 1: Modify the Input and Output Paths
In the script, set the paths for your input and output folders. For example:

```python
folder_path = r"C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdfratioanlization\input"  # Input PDF folder path
output_folder = r"C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdfratioanlization\report"  # Output folder path for reports
```

#### Step 2: Run the Script
Navigate to the folder where the Python script is saved and run it using the following command:

```bash
python pdf_template_analyzer.py
```

#### Step 3: Check the Output
The script will generate a consolidated HTML report in the output folder. The report will be saved as `template_reusability_report.html`. You can open this file in any web browser to view the results.

---

### Project Structure

```
📁 <project-directory>
├── pdf_template_analyzer.py  # Main Python script
├── input/  # Folder where PDFs are stored for analysis
└── report/  # Folder where the HTML report will be generated
```

---

### How the Script Works

1. **PDF Structure Analysis**:
   - The script uses **PyMuPDF** to extract structural elements from each PDF, such as headers, footers, text blocks, tables, and images.
   - It normalizes the text to compare similar content between different PDFs.

2. **Element Comparison**:
   - The script compares the extracted elements across all PDFs.
   - It identifies elements that are **common** across multiple PDFs and groups them for easier identification of reusable sections.

3. **HTML Report Generation**:
   - The script generates a detailed HTML report listing the common elements (e.g., headers, footers, paragraphs) found in the PDFs and where those elements occur.
   - For each common element, the report specifies which PDFs contain that element, making it easy to identify which sections can be reused for templates.

---

### Example Output

The generated HTML report (`template_reusability_report.html`) will look something like this:

```html
<html>
<head>
    <title>Template Reusability Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        h2, h3 { color: #555; }
        p { margin-bottom: 10px; }
        .section { margin-bottom: 40px; }
    </style>
</head>
<body>
    <h1>Template Reusability Report</h1>
    <p>Generated on 2024-10-08 14:35:45</p>

    <h2>Common Headers Across PDFs</h2>
    <p><strong>invoice header</strong> - Found in: invoice1.pdf, invoice2.pdf</p>
    <p><strong>company logo header</strong> - Found in: invoice1.pdf, contract.pdf</p>

    <h2>Common Footers Across PDFs</h2>
    <p><strong>footer text</strong> - Found in: invoice1.pdf, report.pdf</p>

    <h2>Common Paragraphs/Text Blocks Across PDFs</h2>
    <p><strong>Terms and Conditions apply</strong> - Found in: contract.pdf, terms.pdf</p>

    <h2>Common Tables Across PDFs</h2>
    <p><strong>Product and pricing table</strong> - Found in: invoice1.pdf, invoice2.pdf</p>

    <h2>Common Images Across PDFs</h2>
    <p><strong>company logo</strong> - Found in: invoice1.pdf, contract.pdf</p>
</body>
</html>
```

This example shows common headers, footers, paragraphs, tables, and images that were found across multiple PDFs and lists which PDFs contained them.

---

### Full Python Code

Here is the full Python code for generating the template reusability report:

```python
import os
import fitz  # PyMuPDF for analyzing structure and layout
from datetime import datetime
from collections import defaultdict

# Helper function to normalize text (for comparison purposes)
def normalize_text(text):
    return text.lower().strip()

# Step 1: Analyze the structure of a PDF and extract relevant elements
def analyze_pdf_structure(file_path):
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"Error opening file {file_path}: {e}")
        return None  # Skip this file if it can't be opened

    structure_report = {
        "headers": set(),
        "footers": set(),
        "images": set(),
        "tables": set(),
        "text_blocks": set()
    }
    
    for page_number in range(len(doc)):
        try:
            page = doc.load_page(page_number)  # Try loading the page
        except Exception as e:
            print(f"Error reading page {page_number+1} of {file_path}: {e}")
            continue  # Skip this page if there is an error
        
        blocks = page.get_text("dict")["blocks"]  # Get layout blocks
        
        for block in blocks:
            # Identify image blocks
            if "image" in block:
                structure_report["images"].add(f"Image at position {block['bbox']}")
            
            # Identify text blocks and categorize them
            if "lines" in block:
                block_text = "\n".join([span["text"] for line in block["lines"] for span in line["spans"]]).strip()
                
                # Normalize text for comparison
                normalized_text = normalize_text(block_text)
                
                # Simple logic for identifying headers and footers based on position and size
                if block['bbox'][1] < 100:  # Upper part of the page
                    structure_report["headers"].add(normalized_text)
                elif block['bbox'][1] > page.rect.height - 100:  # Lower part of the page
                    structure_report["footers"].add(normalized_text)
                else:
                    structure_report["text_blocks"].add(normalized_text)
        
        # Assuming tables are blocks with more uniform text structures, can improve this detection
        for block in structure_report["text_blocks"]:
            if "table" in block or block.count("\n") > 5:
                structure_report["tables"].add(block)
    
    return structure_report

# Step 2: Compare and identify common elements across PDFs
def compare_pdf_structures(pdf_reports):
    common_elements = {
        "headers": defaultdict(set),
        "footers": defaultdict(set),
        "text_blocks": defaultdict(set),
        "tables": defaultdict(set),
        "images": defaultdict(set)
    }
    
    # Compare headers, footers, text_blocks, tables, and images across PDFs
    for pdf_name, report in pdf_reports.items():
        for element_type in common_elements.keys():
            for element in report[element_type]:
                common_elements[element_type][element].add(pdf_name)
    
    return common_elements

# Step 3: Generate a detailed comparison report
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
        <h1>Template

 Reusability Report</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """

    # Show common headers across PDFs
    html_content += "<h2>Common Headers Across PDFs</h2>"
    if common_elements["headers"]:
        for header, pdfs in common_elements["headers"].items():
            if len(pdfs) > 1:  # Only show headers that are common in more than one PDF
                html_content += f"<p><strong>{header}</strong> - Found in: {', '.join(pdfs)}</p>"
    else:
        html_content += "<p>No common headers found.</p>"

    # Show common footers across PDFs
    html_content += "<h2>Common Footers Across PDFs</h2>"
    if common_elements["footers"]:
        for footer, pdfs in common_elements["footers"].items():
            if len(pdfs) > 1:  # Only show footers that are common in more than one PDF
                html_content += f"<p><strong>{footer}</strong> - Found in: {', '.join(pdfs)}</p>"
    else:
        html_content += "<p>No common footers found.</p>"

    # Show common text blocks across PDFs
    html_content += "<h2>Common Paragraphs/Text Blocks Across PDFs</h2>"
    if common_elements["text_blocks"]:
        for block, pdfs in common_elements["text_blocks"].items():
            if len(pdfs) > 1:  # Only show text blocks common across PDFs
                html_content += f"<p><strong>{block}</strong> - Found in: {', '.join(pdfs)}</p>"
    else:
        html_content += "<p>No common text blocks found.</p>"

    # Show common tables across PDFs
    html_content += "<h2>Common Tables Across PDFs</h2>"
    if common_elements["tables"]:
        for table, pdfs in common_elements["tables"].items():
            if len(pdfs) > 1:  # Only show tables common across PDFs
                html_content += f"<p><strong>{table}</strong> - Found in: {', '.join(pdfs)}</p>"
    else:
        html_content += "<p>No common tables found.</p>"

    # Show common images across PDFs
    html_content += "<h2>Common Images Across PDFs</h2>"
    if common_elements["images"]:
        for image, pdfs in common_elements["images"].items():
            if len(pdfs) > 1:  # Only show images common across PDFs
                html_content += f"<p><strong>{image}</strong> - Found in: {', '.join(pdfs)}</p>"
    else:
        html_content += "<p>No common images found.</p>"

    html_content += """
    </body>
    </html>
    """

    # Save the HTML file with UTF-8 encoding
    html_filename = os.path.join(output_folder, "template_reusability_report.html")
    with open(html_filename, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)
    
    print(f"Template reusability report generated: {html_filename}")

# Step 4: Analyze all PDFs and generate the reusability report
def analyze_pdfs_and_generate_report(folder_path, output_folder):
    pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the folder.")
        return
    else:
        print(f"Found {len(pdf_files)} PDF files to analyze.")

    os.makedirs(output_folder, exist_ok=True)

    # Dictionary to store report for each PDF
    pdf_reports = {}
    
    for pdf in pdf_files:
        pdf_name = os.path.basename(pdf)
        print(f"Analyzing PDF structure for: {pdf_name}")
        
        # Analyze PDF structure
        structure_report = analyze_pdf_structure(pdf)
        
        if structure_report:
            pdf_reports[pdf_name] = structure_report
    
    # Compare and find common elements
    common_elements = compare_pdf_structures(pdf_reports)
    
    # Generate a detailed comparison report
    generate_comparison_html_report(common_elements, output_folder)

# Update paths based on your requirement
if __name__ == "__main__":
    folder_path = r"C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdfratioanlization\input"  # Input PDF folder path
    output_folder = r"C:\Users\denny\Dev\zCompany\Jackson\05SourceCode\pdfratioanlization\report"  # Output folder path for reports

    print(f"Looking for PDFs in folder: {folder_path}")
    analyze_pdfs_and_generate_report(folder_path, output_folder)
```

---

### Known Limitations
- **Table Detection**: The script assumes tables are text blocks with many line breaks. This could be improved for more accurate table detection.
- **Image Comparison**: Image matching is based on their positions. Further enhancement could involve detecting similar images by content.
  
---

### Conclusion

This tool provides a robust method for analyzing and comparing the structure of PDFs to identify reusable elements, allowing for better document rationalization and template creation. It generates a detailed, easy-to-read HTML report that outlines what can be reused across multiple PDFs.
