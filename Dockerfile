# Running Python Flask Server

FROM python:3.8-slim
WORKDIR /scanpix

# install python dependencies and expose port
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5001

# copy directories
COPY ml/ ml/
COPY data/ data/

# start server
CMD ["python3", "ml/server.py", "--index-loc", "data"]