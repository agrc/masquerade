SET FLASK_APP=src/masquerade/main.py
SET FLASK_ENV=development
SET WEB_API_KEY=<.apikey
flask run --cert=cert.pem --key=key.pem --host=0.0.0.0
