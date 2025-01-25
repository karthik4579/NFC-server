#!/bin/bash
cd /home/karthik/NFCserver
source env/bin/activate
gunicorn --bind 0.0.0.0:7656 --log-file=/home/karthik/NFCserver/flask.log wsgi:app &
