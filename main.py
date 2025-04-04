from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
import tkinter as tk
import subprocess
import os
import sys

# Paths
GIT_UPDATER_PATH = os.path.abspath("src/git_updater.py")
SCHEDULER_PATH = os.path.abspath("src/scheduler2.py")

def run_script(path):
    if not os.path.exists(path):
        print(f"Script not found: {path}")
        return
    subprocess.Popen([sys.executable, path])

def show_gui():
    def launch_gui():
        root = tk.Tk()
        root.title("Git Updater Scheduler")
        root.geometry("300x120")
        root.resizable(False, False)

        tk.Label(root, text="Open the Scheduler", font=("Arial", 12)).pack(pady=15)
        tk.Button(root, text="Open Scheduler", width=20, command=lambda: run_script(SCHEDULER_PATH)).pack(pady=5)

        root.mainloop()

    threading.Thread(target=launch_gui).start()

def create_image():
    img = Image.new("RGB", (64, 64), color="black")
    d = ImageDraw.Draw(img)
    d.rectangle([16, 16, 48, 48], fill="white")
    return img

def quit_app(icon, item):
    icon.stop()

def setup_tray():
    # Run git_updater.py once at startup
    run_script(GIT_UPDATER_PATH)

    # Create tray menu
    menu = Menu(
        MenuItem("Scheduler", lambda icon, item: show_gui()),
        MenuItem("Quit", quit_app)
    )
    icon = Icon("GitUpdater", create_image(), menu=menu)
    icon.run()

if __name__ == "__main__":
    threading.Thread(target=setup_tray).start()
