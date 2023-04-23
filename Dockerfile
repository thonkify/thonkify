FROM python:3.10-alpine AS builder

WORKDIR /app
COPY . /app
RUN pip3 install --no-cache-dir .
CMD ["thonkify-server"]
