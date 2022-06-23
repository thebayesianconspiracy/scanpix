# Running worker to watch /data

FROM python:3.8-slim
WORKDIR worker-app/

# Copying directories and installing dependencies
COPY . .
COPY ../data .
RUN  pip3 install watchdog

# start monitoring
CMD ["python3","watch_and_index.py"]
