#!/bin/bash

function upgrade {
    git checkout master
    git pull
    source env/bin/activate
    pip install -r requirements.txt
    python run_device.py
}

upgrade ;
