# Project Blood Legion

A website for World of Warcraft Classic guilds

## Setup

    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    git submodule update --init --recursive
    python -m project_blood_legion --css
    python manage.py migrate
    python manage.py loaddata initial_data
    python manage.py runserver
