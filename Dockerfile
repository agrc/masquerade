FROM python:3.10 AS base


FROM base AS dev_container

RUN apt install -y git

COPY . .

RUN pip install -e ".[tests]"


FROM base AS prod

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

COPY . /app

WORKDIR /app

RUN pip install .

RUN pip install gunicorn

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 masquerade.main:app
