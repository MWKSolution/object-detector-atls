FROM python:3.8
WORKDIR .
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn -b 0.0.0.0:8050 detapp:server