FROM python:3.10-slim

WORKDIR /app

# Install deps OS untuk opencv
RUN apt-get update && apt-get install -y \
    libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "projectname.wsgi:application"]
