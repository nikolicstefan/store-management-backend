FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY owner/requirements.txt owner/
RUN pip install --no-cache-dir -r owner/requirements.txt

COPY common/ common/
COPY owner/ owner/

CMD ["python", "-m", "owner.app"]
