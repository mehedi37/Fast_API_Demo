#!/bin/bash

# Create and activate virtual environment
python -m venv env
source env/Scripts/activate

# Install requirements
pip install -r requirements.txt

# Load .env file and get PORT value
# export $(grep -v '^#' .env | xargs)

# Run FastAPI server
# uvicorn main:app --host $HOST --port $PORT --reload

# run main.py
python main.py