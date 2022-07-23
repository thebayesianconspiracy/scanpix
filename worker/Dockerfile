# Running worker to watch /data

FROM python:3.8-slim
WORKDIR worker-app/

# Copying directories and installing dependencies
COPY worker/ .
COPY ../utils utils/
RUN  pip3 install watchdog requests singleton-decorator

EXPOSE 5000

# start monitoring
RUN chmod +x start_worker.sh
CMD ["./start_worker.sh"]
