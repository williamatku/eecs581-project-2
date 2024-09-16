# Project 2 Setup Guide
- Install python 3.12 https://www.python.org/downloads/
- Open project root directory in terminal
- Install project environment

      python3.12 -m venv .
      source bin/activate
    - NOTE: to deactivate project environment

          deactivate
    - NOTE: to reset project environment (macos, linux, powershell?)

          rm -rf bin include lib pyvenv.cfg
- Install project in development mode and dependencies with PIP 

      pip install -e .
- Run on local machine
      
      python ./src/main.py
