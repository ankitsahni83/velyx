FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY velyx ./velyx
COPY examples ./examples

# default output folder inside container
RUN mkdir -p /app/out

ENTRYPOINT ["python", "-m", "velyx.cli"]