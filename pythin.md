Here’s a complete documentation guide for your project, covering everything from checking the Python version to setting up the folder structure, running the script, and checking the results.

---

## Project Documentation: FAP to RTF Conversion using Python

### 1. Prerequisites

Before you start, ensure you have the following installed on your system:

- **Python 3.x**: You can check if Python is installed by running the following command in your terminal or command prompt:

  ```bash
  python --version
  ```

  If Python is not installed, download and install it from the [official Python website](https://www.python.org/downloads/).

- **pip**: Python’s package installer. It usually comes with Python, but you can check if it’s installed by running:

  ```bash
  pip --version
  ```

  If `pip` is not installed, you can follow the instructions on the [official pip installation page](https://pip.pypa.io/en/stable/installation/).

### 2. Folder Structure

Create the following folder structure for your project:

```plaintext
your_project_directory/
│
├── code/
│   └── convert_fap_to_rtf.py  # The Python script
│
├── input/
│   ├── file1.fap              # Your .fap files go here
│   ├── file2.fap
│   └── ...                    # Add more .fap files as needed
│
└── output/
    └── (this folder will be created automatically by the script if it doesn't exist)
```

- **`code/`**: Contains the Python script.
- **`input/`**: Place your `.fap` files here.
- **`output/`**: This is where the converted `.rtf` files will be saved. The script will create this folder if it doesn't exist.

### 3. Python Script

Save the following Python script as `convert_fap_to_rtf.py` inside the `code` folder:

```python
import os
import pypandoc

def convert_fap_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Check if Pandoc is installed; if not, download it
    try:
        pypandoc.get_pandoc_path()
    except OSError:
        print("Pandoc not found. Downloading and installing Pandoc...")
        pypandoc.download_pandoc()

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
    input_folder = os.path.join(os.path.dirname(__file__), '../input')
    output_folder = os.path.join(os.path.dirname(__file__), '../output')
    convert_fap_files(input_folder, output_folder)
```

### 4. Installing Dependencies

1. **Install `pypandoc`**:

   Run the following command in your terminal or command prompt:

   ```bash
   pip install pypandoc
   ```

### 5. Running the Script

1. **Navigate to the `code` folder**:

   Open a terminal or command prompt and navigate to the `code` directory:

   ```bash
   cd /path/to/your_project_directory/code
   ```

2. **Run the Script**:

   Run the Python script using the following command:

   ```bash
   python convert_fap_to_rtf.py
   ```

   The script will automatically:
   - Check if Pandoc is installed, and download it if necessary.
   - Convert all `.fap` files in the `input` folder to `.rtf` files.
   - Save the converted `.rtf` files in the `output` folder.

### 6. Checking the Results

After the script finishes running:

1. **Check the `output` Folder**:

   Navigate to the `output` folder inside your project directory. You should see `.rtf` files corresponding to each `.fap` file that was in the `input` folder.

2. **Verify the Conversion**:

   Open the `.rtf` files to ensure that the content has been converted correctly from the `.fap` format.

### 7. Additional Information

- **Checking Pandoc Version**:

  If you want to check the version of Pandoc that was downloaded or is installed on your system, run:

  ```bash
  pandoc --version
  ```

- **Script Behavior**:
  - If Pandoc is not found, the script will automatically download it using `pypandoc`.
  - If the `output` folder does not exist, the script will create it.

### 8. Troubleshooting

- **Error: "Pandoc not found"**: If Pandoc is not detected, the script will attempt to download it. Ensure that you have a stable internet connection.
- **Conversion Errors**: If a `.fap` file fails to convert, the script will print an error message. Check the input file’s format to ensure it is compatible with Pandoc.

### 9. Conclusion

This documentation provides all the necessary steps to set up, run, and verify the conversion of `.fap` files to `.rtf` files using a Python script. This process minimizes manual dependencies and provides a straightforward approach to handle the conversion efficiently.

---

This guide should help you set up and run your project without issues, ensuring that your FAP files are successfully converted to RTF format.
