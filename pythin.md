Here is a simple Python script that can automatically convert all `.fap` files in an input folder to `.rtf` files in an output folder using the `pypandoc` library. The script assumes that your `.fap` files contain plain text or are in a format that `pandoc` can handle for conversion.

### Prerequisites

1. **Install `pypandoc`** and **`pandoc`**:
   ```bash
   pip install pypandoc
   choco install pandoc
   ```

### Python Script

Save this script in a file named `convert_fap_to_rtf.py` inside your `code` folder.

```python
import os
import pypandoc

def convert_fap_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.fap'):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.rtf')
            try:
                pypandoc.convert_file(input_file, 'rtf', outputfile=output_file)
                print(f"Successfully converted {filename} to {output_file}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

if __name__ == "__main__":
    input_folder = os.path.join(os.path.dirname(__file__), 'input')
    output_folder = os.path.join(os.path.dirname(__file__), 'output')
    convert_fap_files(input_folder, output_folder)
```

### How to Use the Script

1. **Directory Structure**:
   - `code/` (where the script is located)
   - `input/` (where your `.fap` files are located)
   - `output/` (where the converted `.rtf` files will be saved)

2. **Running the Script**:
   - Navigate to the `code` folder in your terminal or command prompt.
   - Run the script with Python:
     ```bash
     python convert_fap_to_rtf.py
     ```

### What the Script Does:
- **Iterates over all `.fap` files** in the `input` folder.
- **Converts** each `.fap` file to `.rtf` using `pypandoc`.
- **Saves** the converted `.rtf` files in the `output` folder with the same base filename as the original `.fap` file.

This script provides a simple and efficient way to batch convert your FAP files to RTF without needing to write additional logic.
