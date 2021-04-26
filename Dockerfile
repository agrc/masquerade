FROM python:3.8.5-slim

COPY . /app

WORKDIR /app

RUN pip install .

RUN pip install gunicorn

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 masquerade.main:app
