FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install --upgrade pip && pip install -r requirements.txt