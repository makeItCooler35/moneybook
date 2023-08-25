FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/backend
COPY requirements.txt /usr/src/backend
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .