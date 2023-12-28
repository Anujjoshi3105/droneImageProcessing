import os
from datetime import datetime
from pyodm import Node

def image_process(source, destination):
    n = Node('spark1.webodm.net', 443, '79c1998e-eee0-4287-afda-4b6175e236e0')

    images = []

    # Iterate over files in the source directory
    for file in os.scandir(source):
        if file.is_file() and file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff')):
            images.append(file.path)

    if not images:
        print("No image found !!!")
        return

    task = n.create_task(images, {'dsm': True})
    task.wait_for_completion()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    destination_path = os.path.join(destination, f"processed_{timestamp}")
    os.makedirs(destination_path, exist_ok=True)
    task.download_assets(destination_path)

if __name__ == "__main__":
    pass