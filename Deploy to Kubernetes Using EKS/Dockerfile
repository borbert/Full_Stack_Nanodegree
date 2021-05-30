# Base image starting point
FROM python:stretch

# Set up an app directory for the code in the container.
COPY . /app
WORKDIR /app

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", ":8080", "main:APP"]