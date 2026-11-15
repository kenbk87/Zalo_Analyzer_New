FROM python:3.11-slim-bookworm AS builder
WORKDIR /app
#host: your PC, laptop, cloud server,...
#Copy from "host" to "container"
COPY requirements.txt requirements.txt
#Run this command in the container
RUN pip3 install -r requirements.txt
COPY . .
#Run command in container
CMD ["python3", "main.py"]