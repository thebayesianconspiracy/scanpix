# Running worker to watch /data

FROM python:3.8-slim
WORKDIR worker-app/

# Copying directories and installing dependencies
COPY worker/ .
RUN  pip3 install watchdog requests

EXPOSE 5000

# start monitoring
CMD ["python3","watch_and_index.py"]
