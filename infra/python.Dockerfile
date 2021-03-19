FROM python:3.9-slim

ARG DIR_SOURCE

COPY "${DIR_SOURCE}requirements.txt" /requirements.txt

RUN pip install --upgrade pip && pip install -r /requirements.txt

WORKDIR /app

CMD [ "python", "main.py" ]
