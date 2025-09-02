# 1. Base Image: Use a Python image that makes it easy to install Node.js
FROM python:3.11-slim

# 2. Install System Dependencies: FFmpeg, and now Node.js and npm
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# 3. Set Environment Variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Set the working directory inside the container
WORKDIR /app

# 5. Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy files for Node.js dependencies and install them
COPY package.json package-lock.json ./
RUN npm install

# 7. Copy the rest of the project into the container
COPY . .

# 8. Build Tailwind CSS
RUN npx @tailwindcss/cli -i static/css/main.css -o static/dist/css/output.css --minify

# 9. Run Django's collectstatic with all required dummy keys
RUN DEBUG=0 SECRET_KEY=dummy ASSEMBLYAI_API_KEY=dummy COHERE_API_KEY=dummy python manage.py collectstatic --noinput

# 10. Run database migrations (for Free Tier)
RUN DEBUG=0 SECRET_KEY=dummy ASSEMBLYAI_API_KEY=dummy COHERE_API_KEY=dummy python manage.py migrate

# 11. Set the command to run the application using Gunicorn (Shell Form)
CMD gunicorn ai_blog_app.wsgi:application --bind 0.0.0.0:$PORT --timeout 1000
