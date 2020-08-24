FROM python:3.8.5-slim

COPY . /app

WORKDIR /app

RUN pip install .

RUN pip install gunicorn

EXPOSE 8000

CMD ["gunicorn", "masquerade.main:app", "-b", ":8000"]
