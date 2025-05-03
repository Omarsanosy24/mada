# 1: Start with the official Python image
FROM python:3.12

# 2: Set environment variables to show logs immediately
ENV PYTHONUNBUFFERED=1

# 3: Update the system and install dependencies
RUN apt-get update && apt-get install -y \
    gcc \                # Compiler for building some Python packages
    libpq-dev \          # PostgreSQL development libraries
    zstd                 # Zstandard compression tool (if needed)

# 4: Create a working directory for the project
WORKDIR /app

# 5: Copy requirements.txt into the container
COPY requirements.txt /app/requirements.txt

# 6: Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# 7: Copy the rest of the project code into the container
COPY . /app/

# 8: Expose the port your app runs on (if applicable)
EXPOSE 8000

# 9: Define the command to run your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]