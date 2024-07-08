FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    python3-dev \
    pkg-config


RUN pip install --upgrade pip


WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY ../../viktoriiarich/Desktop /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
