FROM python:3.11

WORKDIR /currency_exchange

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /currency_exchange/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]