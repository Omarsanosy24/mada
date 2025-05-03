# 1: Start from official Python 3.12 image
FROM python:3.12-slim

# 2: Show logs immediately
ENV PYTHONUNBUFFERED=1

# 3: Install required system packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    zstd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4: Set working directory
WORKDIR /app

# 5: Copy requirements file first (for layer caching)
COPY requirements.txt .

# 6: Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# 7: Copy the rest of the project
COPY . .

# 8: Set default command (اختياري)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
