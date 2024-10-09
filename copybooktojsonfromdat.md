Here’s the complete documentation with code, copybooks, `bill.dat`, and the expected JSON output, all designed to be placed under your folder path `d:/test/code` for easy testing.

### Project Structure

Your folder structure should look like this:

```
d:/test/
│
├── code/
│   ├── generate_json.py        # Main script for generating JSON from bill.dat using copybooks
│   ├── copybooks/              # Folder for storing .cpy files
│   │   ├── bill_header.cpy
│   │   ├── bill_detail.cpy
│   │   ├── bill_payment.cpy
│   │   ├── correspondence_header.cpy
│   │   └── correspondence_message.cpy
│   ├── data/                   # Folder for input data and output files
│   │   ├── bill.dat            # Input data file
│   │   └── output/             # Folder for storing the generated bill.json
```

---

### 1. **Script: `generate_json.py`**

```python
import os
import re
import json

# Paths to folders
COPYBOOKS_FOLDER = r"d:/test/code/copybooks"
DATA_FOLDER = r"d:/test/code/data"
OUTPUT_FOLDER = os.path.join(DATA_FOLDER, "output")

# Ensure output directory exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def parse_copybook(cpy_file_path):
    """Parses a COBOL .cpy file and returns a list of field definitions."""
    field_definitions = []
    
    with open(cpy_file_path, 'r') as file:
        for line in file:
            match = re.search(r'05\s+(\w+)\s+PIC\s+([X9]+)\((\d+)\)(V(\d+))?', line)
            if match:
                field_name = match.group(1)
                field_type = match.group(2)
                field_length = int(match.group(3))
                decimal_length = int(match.group(5)) if match.group(5) else 0
                
                field_definitions.append({
                    'name': field_name,
                    'type': field_type,
                    'length': field_length,
                    'decimal_length': decimal_length
                })
    return field_definitions

def load_copybooks(copybooks_folder):
    """Loads and parses all .cpy files in the copybooks folder."""
    copybooks = {}
    for filename in os.listdir(copybooks_folder):
        if filename.endswith(".cpy"):
            template_id = filename.split('.')[0].split('_')[-1]  # Extract identifier from file name
            cpy_path = os.path.join(copybooks_folder, filename)
            copybooks[template_id] = parse_copybook(cpy_path)
    return copybooks

def parse_record(fields, record):
    """Parses a record using the provided fields definition."""
    parsed_record = {}
    current_position = 0
    
    for field in fields:
        length = field['length']
        value = record[current_position:current_position + length].strip()
        
        # For numeric fields with decimal, format accordingly
        if field['type'] == '9' and field['decimal_length'] > 0:
            integer_part = value[:length - field['decimal_length']]
            decimal_part = value[-field['decimal_length']:]
            value = f"{integer_part}.{decimal_part}"
        
        parsed_record[field['name']] = value
        current_position += length
    
    return parsed_record

def process_bill_dat(file_path, copybooks):
    """Processes the bill.dat file and generates a list of parsed records."""
    results = []
    
    with open(file_path, 'r') as f:
        for line in f:
            # Get the first 4 digits to determine the template ID
            template_id = line[:4]
            
            # Get the copybook based on template ID
            template = copybooks.get(template_id)
            
            if template:
                # Parse the record using the template
                parsed_record = parse_record(template, line)
                results.append(parsed_record)
            else:
                print(f"Unknown template ID: {template_id}")
    
    return results

# Main function to trigger the entire process
def main():
    # Load copybooks from the specified folder
    copybooks = load_copybooks(COPYBOOKS_FOLDER)
    
    # Process the bill.dat file
    bill_dat_path = os.path.join(DATA_FOLDER, "bill.dat")
    parsed_records = process_bill_dat(bill_dat_path, copybooks)
    
    # Generate a single output JSON file
    output_file = os.path.join(OUTPUT_FOLDER, "bill.json")
    
    with open(output_file, 'w') as json_file:
        json.dump(parsed_records, json_file, indent=4)
    
    print(f"Single output JSON file generated: {output_file}")

if __name__ == "__main__":
    main()
```

---

### 2. **Copybooks:**

Place these `.cpy` files in the `d:/test/code/copybooks/` folder.

#### `bill_header.cpy`

```plaintext
01  BILL-HEADER.
    05  BILL-ID         PIC 9(8).
    05  BILL-DATE       PIC 9(8).
    05  BILL-TYPE       PIC X(1).
```

#### `bill_detail.cpy`

```plaintext
01  BILL-DETAIL.
    05  BILL-AMOUNT     PIC 9(5)V99.
    05  BILL-DUE-DATE   PIC 9(8).
    05  ITEM-DESCRIPTION PIC X(20).
```

#### `bill_payment.cpy`

```plaintext
01  BILL-PAYMENT.
    05  PAYMENT-STATUS  PIC 9(1).
    05  PAYMENT-DATE    PIC 9(8).
    05  PAYMENT-METHOD  PIC X(10).
```

#### `correspondence_header.cpy`

```plaintext
01  CORRESPONDENCE-HEADER.
    05  SENDER-ID       PIC 9(10).
    05  RECEIVER-ID     PIC 9(10).
    05  DATE-SENT       PIC 9(8).
```

#### `correspondence_message.cpy`

```plaintext
01  CORRESPONDENCE-MESSAGE.
    05  SUBJECT         PIC X(30).
    05  BODY            PIC X(100).
```

---

### 3. **Input File: `bill.dat`**

Place the `bill.dat` file in the `d:/test/code/data/` folder.

```plaintext
00001234567820210901B
00019999990020211231Electric Bill
000215000020211015Card
0010123456789020210930
0011Meeting Follow-up  Details about the meeting follow-up in the body...
```

This is a sample file with different sections like Bill, Payment, and Correspondence.

---

### 4. **Expected Output: `bill.json`**

Once you run the script, a `bill.json` file will be generated in `d:/test/code/data/output/`. The expected JSON output will look like this:

```json
[
    {
        "BILL-ID": "12345678",
        "BILL-DATE": "20210901",
        "BILL-TYPE": "B"
    },
    {
        "BILL-AMOUNT": "9999.99",
        "BILL-DUE-DATE": "20211231",
        "ITEM-DESCRIPTION": "Electric Bill"
    },
    {
        "PAYMENT-STATUS": "2",
        "PAYMENT-DATE": "20211015",
        "PAYMENT-METHOD": "Card"
    },
    {
        "SENDER-ID": "1234567890",
        "RECEIVER-ID": "20210930",
        "DATE-SENT": "20210930"
    },
    {
        "SUBJECT": "Meeting Follow-up",
        "BODY": "Details about the meeting follow-up in the body..."
    }
]
```

---

### 5. **Running the Script**

To run the script and generate the output JSON, follow these steps:

1. Ensure that the folder structure and files are set up as described.
2. Open a command prompt and navigate to the `d:/test/code/` directory.
3. Run the Python script:

```bash
python generate_json.py
```

4. The `bill.json` file will be generated in the `d:/test/code/data/output/` folder.

---

### Conclusion:

This complete setup will allow you to run the script and generate the JSON output from the `bill.dat` file using the COBOL copybooks. You can test and modify the setup as needed for your specific requirements.
