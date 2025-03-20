#!/bin/bash

if ! command -v python3 &> /dev/null
then
    echo "Python 3.x is not installed."
    exit
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit
fi

echo "Starting the Travel Application..."
python3 TravelAppGUI.py
if [ $? -ne 0 ]; then
    echo "Failed to start the application."
    exit
fi

echo "Application started successfully!"