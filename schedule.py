import os
from datetime import datetime

def generate_bash_script(source_folder, destination_folder):
    script_content = f"""#!/bin/bash

SOURCE_FOLDER="{source_folder}"
DESTINATION_FOLDER="{destination_folder}"

python3 /path/to/your/script.py $SOURCE_FOLDER $DESTINATION_FOLDER
"""

    # Write the script content to a file
    script_file_path = "run_image_processing.sh"
    with open(script_file_path, "w") as script_file:
        script_file.write(script_content)

    # Make the script executable
    os.chmod(script_file_path, 0o755)

    print(f"Bash script generated: {script_file_path}")

if __name__ == "__main__":
    # Replace these paths with the actual source and destination folder paths
    source_folder = "/path/to/source/folder"
    destination_folder = "/path/to/destination/folder"

    generate_bash_script(source_folder, destination_folder)
