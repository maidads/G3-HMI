import os
import glob
import subprocess
import sys

def convert_ui_to_py():
    ui_files = glob.glob("*.ui")
    success_count = 0
    failed_files = []
    
    for ui_file in ui_files:
        base_name = os.path.splitext(ui_file)[0]
        py_file = "ui_" + base_name + ".py"
        
        try:
            # Add the --debug flag to get detailed error information
            result = subprocess.run(
                ["pyuic6", "--debug", "-x", ui_file, "-o", py_file],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✓ Successfully converted {ui_file} to {py_file}")
            success_count += 1
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Error converting {ui_file}:")
            print(f"Exit code: {e.returncode}")
            print(f"Standard output: {e.stdout}")
            print(f"Error output: {e.stderr}")
            failed_files.append(ui_file)
            
            # Still try to check if the output file was created
            if os.path.exists(py_file):
                print(f"  Note: Output file {py_file} was created despite errors")

    # Report summary
    print("\nConversion Summary:")
    print(f"Total files: {len(ui_files)}")
    print(f"Successfully converted: {success_count}")
    print(f"Failed: {len(failed_files)}")
    
    if failed_files:
        print("\nFiles with errors:")
        for failed_file in failed_files:
            print(f"- {failed_file}")
        
        print("\nAlternatives:")
        print("1. Try using a different version of PyQt6 or install PySide6")
        print("2. Check your UI files for any syntax errors or unsupported elements")
        print("3. Consider using the Qt Designer's 'Preview' functionality to validate your UI files")

if __name__ == "__main__":
    convert_ui_to_py()