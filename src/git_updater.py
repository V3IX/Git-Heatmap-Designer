import json
import datetime
import socket
import os
import random
import string
import subprocess
import time

def is_today_in_json(file_path):
    try:
        with open(file_path, 'r') as file:
            dates = json.load(file)
        today = datetime.date.today().isoformat()
        return today in dates
    except (FileNotFoundError, json.JSONDecodeError):
        return False

def is_internet_available():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def random_commit():
    random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    with open("dummy.txt", "a") as file:
        file.write(random_text + "\n")
    
    os.system("git add dummy.txt")
    
    # Use subprocess to safely pass the commit message
    subprocess.run(["git", "commit", "-m", f"Update: {random_text}"], check=True)

print("Current Working Directory:", os.getcwd())  # Debugging line

# Get the absolute path of the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Correctly join the git_tests directory relative to the script
GIT_REPO_PATH = os.path.join(SCRIPT_DIR, "..", "git_tests")

def update_repo():
    os.chdir(GIT_REPO_PATH)  # Ensure we're inside the repo

    for _ in range(40):
        random_commit()

    # Check if the branch has an upstream
    try:
        subprocess.run(["git", "push"], check=True)
    except subprocess.CalledProcessError:
        print("Setting upstream branch...")
        subprocess.run(["git", "push", "--set-upstream", "origin", "master"], check=True)

def wait_for_internet():
    print("Waiting for internet connection...")
    while not is_internet_available():
        time.sleep(5)  # Wait for 5 seconds before checking again
    print("Internet connection established.")

def main():
    print("Executing main function...")
    update_repo()

if __name__ == "__main__":
    if is_today_in_json("dates.json"):
        if is_internet_available():
            main()
        else:
            wait_for_internet()
            main()
    else:
        print("Today's date is not in dates.json.")
