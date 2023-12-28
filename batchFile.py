import os
import subprocess

def startBatch(task_list):
    batch_content = f'start /B pythonw "autobot.py" "{task_list}"'
    batch_file = 'autobot.bat'

    user_home = os.path.expanduser("~")
    startup_folder = os.path.join(user_home, 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    os.makedirs(startup_folder, exist_ok=True)
    full_path = os.path.join(startup_folder, batch_file)

    with open(full_path, 'w') as batch_file:
        batch_file.write(batch_content)
    subprocess.run(full_path, shell=True)