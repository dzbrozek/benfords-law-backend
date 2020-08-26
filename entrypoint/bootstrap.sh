#!/bin/bash

set -o errexit
set -o nounset

. /app/entrypoint/wait-postgres.sh

python manage.py migrate

python manage.py loaddata ../fixtures/*.json
