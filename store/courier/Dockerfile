FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY courier/requirements.txt courier/
RUN pip install --no-cache-dir -r courier/requirements.txt

COPY common/ common/
COPY courier/ courier/

CMD ["python", "-m", "courier.app"]
