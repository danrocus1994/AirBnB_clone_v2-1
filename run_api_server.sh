#!/usr/bin/env bash
# Start a Flask configuration given $1 = configuration filename

filename=$(echo "$1" | cut -d '/' -f 2 | cut -d '.' -f 1)
echo "deploying $filename"
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db python3 -m api."$filename"