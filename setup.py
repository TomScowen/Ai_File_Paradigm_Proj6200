#  ___________________________________________________________________
# |=-=-=-=-=-=-=-=-=-=-=-=-=-| SETUP SCRIPT |=-=-=-=-=-=-=-=-=-=-=-=-=|
# | Run this script once to install all dependencies and launch the   |
# | AI-Driven File Paradigm Application.                              |
# | type python setup.py in terminal                                  |
#  \_________________________________________________________________/

import subprocess #lets python run terminal commands (pip install etc)
import sys # access to python interpreter
import os # access to operating system
import pathlib

#resuable function to run a terminal command (so we dont have to keep doing subprocesses throughout.)
def run(cmd, description=""):
    if description:
        print(f"\n{description}")
    subprocess.run(cmd, check=True) #runs termninal command


print("   AI-Driven File Paradigm - Setup Script")

# STEP 1
# Checks if the virtual environment exists, if it doesn't we create the environment
if not os.path.exists("venv"):
    run([sys.executable, "-m", "venv", "venv"],
        "1/4 creating virtual environment.....")
else:
    print("\n[1/4 virtual environment already exists (skipping).....")

# Checks whether windows or mac (or linux) and determines venv path
if sys.platform == "win32":
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    venv_pip = os.path.join("venv", "Scripts", "pip.exe")
else:
    venv_python = os.path.join("venv", "bin", "python")
    venv_pip = os.path.join("venv", "bin", "pip")

# STEP 2
#Install requirements.txt (now different as mac required specific additions that would crash win)
if not os.path.exists("venv"):
    if sys.platform == "win32": #Windows req
        run([venv_pip, "install", "-r", "requirements-win.txt", "--ignore-requires-python"], 
        "2/4 Installing requirements (Windows)...")
    else: #Mac req
        run([venv_pip, "install", "-r", "requirements-mac.txt"], "2/4 installing requirements-mac.py (Mac)...")
else: 
    print("\n2/4 requirements already installed (skipping)...")

# Step 3 - Downloading the Mistral7B model
#sets the path for model cache
if sys.platform == "win32": 
    model_cache = pathlib.Path.home() / "AppData" / "Local" / "huggingface" / "hub" / "models--mistralai--Mistral-7B-Instruct-v0.3"
else: #downloads to mac path 
    model_cache = pathlib.Path.home() / ".cache" / "huggingface" / "hub" / "models--mistralai--Mistral-7B-Instruct-v0.3"
#checks if mistral exists.
if not model_cache.exists():
    print("\n3/4 Downloading Mistral7B (This could take up to 20minutes for first time users)")
    run([venv_python, "-c",
        "from transformers import AutoModelForCausalLM, AutoTokenizer; import torch; "
        "print('Downloading tokeniser...'); "
        "AutoTokenizer.from_pretrained('mistralai/Mistral-7B-Instruct-v0.3'); "
        "print('Downloading model weights...'); "
        "AutoModelForCausalLM.from_pretrained('mistralai/Mistral-7B-Instruct-v0.3', dtype=torch.float16); "
        "print('Model downloaded successfully!')"])
else:
    print("\n3/4 Mistral7B already exists (skipping)....")

#LAUNCHING THE APP (STEP 4)
print("\n[4/4] Setup complete! Launching application...")
print("\nNote: To run the app again in future use:")
print("  streamlit run fileParadigmApp.py")
print("  (after activating venv with: source venv/bin/activate)\n")

#this runs the app in the browser
run([venv_python, "-m", "streamlit", "run", "fileParadigmApp.py"])