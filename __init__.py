import os
import subprocess

# get the path of the current file
root = os.path.dirname(os.path.realpath(__file__))
print(root)
# get the path of the virtual environment
venv = os.path.join(root, ".venv")
# get the path of the python executable
python = os.path.join(venv, "Scripts", "python.exe")
# get the path of the script
script = os.path.join(root, "audit.py")

# run the script
subprocess.call([python, script])