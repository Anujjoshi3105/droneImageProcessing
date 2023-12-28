import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

def watch_and_execute(file_path):
    def execute_scripts(file_list_path, startup_files):
        with open(file_list_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split(" | ")
            if len(parts) == 4:
                file_name = parts[0]
                if file_name.lower() not in startup_files:
                    pass

        for startup_file in startup_files:
            if startup_file.lower() not in {line.strip().split(" | ")[0].lower() for line in lines}:
                file_to_delete = os.path.join(startup_folder, startup_file)
                os.remove(file_to_delete)
   
    def on_modified(event):
        if event.src_path.endswith(file_path):
            print(f"{file_path} updated. Checking for new files and executing scripts...")
            execute_scripts(file_path, startup_files)

    try:
        user_home = os.path.expanduser("~")
        startup_folder = os.path.join(user_home, 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        startup_files = {os.path.splitext(file)[0].lower() for file in os.listdir(startup_folder) if file.lower().endswith('.bat')}

        event_handler = FileSystemEventHandler()
        event_handler.on_modified = on_modified
        observer = Observer()
        observer.schedule(event_handler, path=".", recursive=False)
        observer.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    watch_and_execute("file_list.txt")