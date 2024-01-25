FROM docker.io/python:3.12-alpine

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY app.py app.py

ENTRYPOINT ["python3", "app.py"]