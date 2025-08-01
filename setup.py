import os
import sys
import subprocess
import urllib.request
import platform
import tempfile
import time
import traceback

def download_python_installer(url, save_path):
    print(f"Downloading Python installer from {url} ...")
    urllib.request.urlretrieve(url, save_path)
    print(f"Downloaded Python installer to {save_path}")

def run_installer(installer_path):
    print("Running Python installer silently...")
    args = [installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_pip=1", "/norestart"]
    result = subprocess.run(args, shell=True)
    if result.returncode == 0:
        print("Python installed successfully.")
    else:
        print(f"Python installer exited with code {result.returncode}.")
        sys.exit(1)

def run_command(command_list):
    print(f"Running command: {' '.join(command_list)}")
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, shell=True)
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Exception running command: {e}")
        return False

def install_libraries(lib_file, python_executable):
    print(f"Installing libraries from {lib_file} ...")
    max_retries = 3
    for attempt in range(max_retries):
        print(f"Attempt {attempt+1} to install libraries")
        if not run_command([python_executable, "-m", "pip", "install", "--upgrade", "pip"]):
            print("Failed to upgrade pip")
            continue
        if run_command([python_executable, "-m", "pip", "install", "-r", lib_file]):
            print("Libraries installed successfully.")
            return True
        else:
            print("Failed to install libraries, retrying...")
            time.sleep(5)
    print("Failed to install libraries after multiple attempts.")
    return False

import shutil

def create_exe(script_path, python_executable):
    print(f"Creating executable from {script_path} using PyInstaller...")
    if not run_command([python_executable, "-m", "pip", "install", "--upgrade", "pyinstaller"]):
        print("Failed to install or upgrade PyInstaller.")
        return False
    if run_command([python_executable, "-m", "PyInstaller", "--onefile", script_path]):
        print("Executable created successfully.")
        # Move all files and folders from dist to current directory
        dist_path = os.path.join(os.getcwd(), "dist")
        if os.path.exists(dist_path):
            for item in os.listdir(dist_path):
                s = os.path.join(dist_path, item)
                d = os.path.join(os.getcwd(), item)
                if os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.move(s, d)
                else:
                    if os.path.exists(d):
                        os.remove(d)
                    shutil.move(s, d)
            shutil.rmtree(dist_path)
        return True
    else:
        print("Failed to create executable.")
        return False

def main():
    try:
        print("Starting setup script...")
        if platform.system() != "Windows":
            print("This setup script currently supports only Windows.")
            raise Exception("Unsupported OS")

        python_installer_url = "https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe"
        temp_dir = tempfile.gettempdir()
        installer_path = os.path.join(temp_dir, "python-3.13.5-amd64.exe")

        python_installed = False
        python_executable = "python"
        try:
            version_output = subprocess.check_output([python_executable, "--version"], text=True).strip()
            print(f"Current Python version: {version_output}")
            if version_output.startswith("Python 3.13"):
                print("Suitable Python version already installed.")
                python_installed = True
            else:
                print("Python version is not 3.13.x, proceeding to install Python 3.13.5.")
        except Exception as e:
            print(f"Python not found or error checking version: {e}")

        if not python_installed:
            print("Downloading and installing Python...")
            download_python_installer(python_installer_url, installer_path)
            run_installer(installer_path)
            time.sleep(10)

        lib_file = "lib.txt"
        if not os.path.exists(lib_file):
            print(f"Library file {lib_file} not found.")
            raise Exception("Missing lib.txt")
        print("Installing libraries...")
        if not install_libraries(lib_file, python_executable):
            raise Exception("Failed to install libraries")

        script_path = "main.py"
        if not os.path.exists(script_path):
            print(f"Script file {script_path} not found.")
            raise Exception("Missing main.py")
        print("Creating executable from main.py...")
        if not create_exe(script_path, python_executable):
            raise Exception("Failed to create executable")
        print("Setup script completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
    input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    main()
