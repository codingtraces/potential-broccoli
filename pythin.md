Here’s how you should structure your folders and files to use the Python script I provided:

### Folder Structure

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

### Steps to Set Up

1. **Create the Main Project Directory**: Name it whatever you like, e.g., `fap_to_rtf_converter`.

2. **Create a `code` Folder**: Inside your project directory, create a folder named `code`. This is where your Python script will reside.

3. **Create an `input` Folder**: Inside your project directory, create a folder named `input`. This is where you will place all your `.fap` files that need to be converted.

4. **Create an `output` Folder** (Optional): You can create an `output` folder inside your project directory where the converted `.rtf` files will be saved. If you don’t create this folder, the script will create it for you.

5. **Place the Python Script in the `code` Folder**: Save the Python script (`convert_fap_to_rtf.py`) inside the `code` folder.

### Running the Script

1. **Navigate to the `code` Folder**:
   - Open a terminal or command prompt.
   - Navigate to the `code` directory inside your project:
     ```bash
     cd /path/to/your_project_directory/code
     ```

2. **Run the Script**:
   - Run the script using Python:
     ```bash
     python convert_fap_to_rtf.py
     ```

### After Running the Script

- The script will process all `.fap` files in the `input` folder and save the converted `.rtf` files in the `output` folder.
- If the `output` folder doesn’t exist, the script will create it automatically.

This folder structure keeps everything organized and makes it easy to manage the conversion process.
