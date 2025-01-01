import os
import sys
import subprocess

def create_virtualenv(venv_name):
    """
    Creates a virtual environment with the given name.

    Args:
        venv_name (str): The name of the virtual environment.
    """
    if not venv_name:
        print("Error: You must provide a name for the virtual environment.")
        sys.exit(1)
    
    try:
        # Check if venv is available
        subprocess.run([sys.executable, "-m", "venv", "--help"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Error: Python 'venv' module is not available.")
        sys.exit(1)
    
    # Create the virtual environment
    print(f"Creating virtual environment: {venv_name}")
    subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
    print(f"Virtual environment '{venv_name}' created successfully.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python create_venv.py <venv_name>")
        sys.exit(1)
    
    venv_name = sys.argv[1]
    create_virtualenv(venv_name)

if __name__ == "__main__":
    main()
