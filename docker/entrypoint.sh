#!/bin/sh

set -x
DE_PATH="/var/www/html/DE_project"

"$DE_PATH"/manage.py makemigrations
"$DE_PATH"/manage.py migrate

exec "$@"
