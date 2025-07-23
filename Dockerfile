FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Сначала копируем только requirements.txt и устанавливаем зависимости
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt

# Затем копируем остальной код
COPY . /app

CMD ["python3", "app_api.py"]