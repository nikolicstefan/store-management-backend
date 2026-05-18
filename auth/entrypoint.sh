#!/bin/sh
set -e

flask --app app.py db upgrade

exec python app.py
