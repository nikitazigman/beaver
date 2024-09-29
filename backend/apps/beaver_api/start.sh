#!/bin/bash

# Determine the current script's directory
this_file=$(realpath $0)
this_dir=$(dirname $this_file)
# Build the path to the API Application's base directory
api_dir=$(realpath $this_dir/src/)

cd $api_dir
poetry run python manage.py migrate
poetry run python manage.py collectstatic --noinput
poetry run gunicorn --capture-output  -w 3  -b 0.0.0.0:8000 beaver_api.wsgi 
