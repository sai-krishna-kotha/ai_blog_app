# 1. Base Image: Use a newer Python version
FROM python:3.11-slim

# 2. Install System Dependencies: FFmpeg is required for youtube-dlp
RUN apt-get update && apt-get install -y ffmpeg

# 3. Set Environment Variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Set the working directory inside the container
WORKDIR /app

# 5. Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the entire project into the container
COPY . .

# 7. Run Django's collectstatic with all required dummy keys
RUN DEBUG=0 SECRET_KEY=dummy ASSEMBLYAI_API_KEY=dummy COHERE_API_KEY=dummy python manage.py collectstatic --noinput

# 8. Set the command to run the application using Gunicorn
CMD ["gunicorn", "ai_blog_app.wsgi:application", "--bind", "0.0.0.0:$PORT"]
