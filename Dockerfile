FROM python:3.10-alpine AS builder

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]