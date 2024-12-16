FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    wget \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6

COPY . /app/
RUN mkdir -p /app/models && mkdir -p /app/dataset
EXPOSE 5000
CMD ["python", "app.py"]
