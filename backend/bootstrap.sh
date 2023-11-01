#!/bin/bash
export FLASK_APP=./main.py
source $(pipenv --venv)/bin/activate
flask run --port 5003