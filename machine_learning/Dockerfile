FROM python:latest

WORKDIR /app

RUN apt update && apt upgrade -y

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY logging_framework/ logging_framework
COPY ml_adapters/ ml_adapters
COPY persistence/ persistence
COPY data/ data
COPY *.py .
COPY . .

CMD ["python3", "app.py"]