FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY customer/requirements.txt customer/
RUN pip install --no-cache-dir -r customer/requirements.txt

COPY common/ common/
COPY customer/ customer/

CMD ["python", "-m", "customer.app"]
