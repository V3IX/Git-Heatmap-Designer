import os
import sys
import winreg as reg

def add_to_startup():
    """Add the script to Windows startup."""
    script_path = os.path.join(os.path.dirname(sys.argv[0]), "src", "git_updater.py")
    
    # Ensure the script exists before adding it to startup
    if not os.path.exists(script_path):
        print(f"Error: {script_path} does not exist.")
        return
    
    # Use Python executable to run the script
    python_exe = sys.executable
    command = f'"{python_exe}" "{script_path}"'
    
    # Registry path for startup entries
    registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        # Open the registry and add the entry
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, registry_key, 0, reg.KEY_WRITE)
        reg.SetValueEx(reg_key, "GitUpdater", 0, reg.REG_SZ, command)
        reg.CloseKey(reg_key)
        print("GitUpdater added to startup successfully!")
    except Exception as e:
        print(f"Error adding to startup: {e}")

def is_first_run():
    """Check if this is the first time the program is running."""
    first_run_file = os.path.join(os.getenv('APPDATA'), 'git_updater_first_run.txt')
    
    if not os.path.exists(first_run_file):
        with open(first_run_file, 'w') as f:
            f.write('This is the first run.')
        print("First run detected!")
        return True
    else:
        print("This is not the first run.")
        return False

def main():
    """Main function to check and handle first run logic."""
    if is_first_run():
        add_to_startup()
    else:
        print("GitUpdater has already been set to start on boot.")

if __name__ == "__main__":
    main()
