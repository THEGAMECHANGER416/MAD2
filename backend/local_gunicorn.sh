#! /bin/bash
echo "======================================="
echo "Welcome to Brandly Backend"
echo "This is a local run environment"
echo "We will start the server now"
echo "======================================="

if [ -d .venv ]; 
then
    echo "Enabling virtual environment"
else
    echo "No virtual environment found"
    echo "Please run local_setup.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate
export ENV=stage
gunicorn main:app --worker-class gevent --bind 127.0.0.1:8000 --workers=4
deactivate