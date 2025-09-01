# 1. Base Image: Use the same Python version as your project
FROM python:3.9-slim

# 2. Install System Dependencies: FFmpeg is required for youtube-dlp
RUN apt-get update && apt-get install -y ffmpeg

# 3. Set Environment Variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Set the working directory inside the container
WORKDIR /app

# 5. Copy and install Python requirements
# This is done in a separate step to leverage Docker's build cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the entire project into the container
COPY . .

# 7. Run Django's collectstatic
# This gathers all static files (CSS, JS) into a single folder for WhiteNoise to serve
RUN python manage.py collectstatic --noinput

# 8. Set the command to run the application using Gunicorn
# Render provides the $PORT environment variable, which we bind to.
CMD ["gunicorn", "blog_app.wsgi:application", "--bind", "0.0.0.0:$PORT"]
