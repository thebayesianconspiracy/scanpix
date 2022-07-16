#!/bin/bash

python3 web_socket_server/server.py&
python3 -u watch_and_index.py
