#! /bin/bash

echo "======================================="
echo "Welcome to Brandly Backend"
echo "This is a local setup environment"
echo "We will start the setup now"
echo "======================================="

# Apt update and install
sudo apt update
sudo apt install -y python3-venv python3-pip
sudo apt install -y sqlite3

# Create virtual environment
[ -d .venv ] && rm -rf .venv
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Deactivate virtual environment
deactivate