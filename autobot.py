import os
import time
from datetime import datetime
import sys

def monitor_task(file_path):
    def parse_file_line(line):
        parts = line.strip().split("|")
        return tuple(part.strip() for part in parts) if len(parts) == 4 else None

    while True:
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            today_date = datetime.now().strftime("%Y-%m-%d")

            with open(file_path, "r") as file:
                for line in file:
                    values = parse_file_line(line)
                    scheduled_time = datetime.strptime(values[3], "%H:%M:%S")
                    if values and scheduled_time <= datetime.now():
                        destination_folder = os.path.join(values[2], f"processed_{today_date}")
                        if not os.path.exists(destination_folder) and scheduled_time > datetime.now():
                            imageProcess(values[1:])
            time.sleep(60)

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("file path missing")
        sys.exit(1)

    task_file = sys.argv[1]
    monitor_task(task_file)