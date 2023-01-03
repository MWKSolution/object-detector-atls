FROM python:3.8
RUN mkdir -p /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app
WORKDIR /app
RUN chown -R 1000 .
RUN chmod -R 777 .
EXPOSE 8050
USER 1000
RUN ls -l
RUN ls -l object_detector
CMD gunicorn -b 0.0.0.0:8050 detapp:server