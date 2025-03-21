FROM python:3.12-slim

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONPATH=src

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src src

EXPOSE 8000

CMD ["gunicorn", "src.main:create_app()", "--bind", "0.0.0.0:8000"]
