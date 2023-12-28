import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def on_file_change(event):
    if not event.is_directory:
        print("Hello!")

def watch_file(file_path):
    event_handler = FileSystemEventHandler()
    event_handler.on_any_event = on_file_change

    with Observer() as observer:
        observer.schedule(event_handler, path=file_path, recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    watch_file(file_path)