#!/bin/bash

python3 web_socket_server/server.py&
sleep 60
python3 -u watch_and_index.py
