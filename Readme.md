# 🧠 AI Blog Generator - Web App

Welcome to the **AI Blog Generator**!  
This is a web-based application that allows users to **generate insightful and structured blog content from any YouTube video link** using cutting-edge AI models and natural language processing tools.

📍 **Live URL :**  [Click Here](https://ai-blog-app-qs73.onrender.com/)  

---

## 📽️ What It Does
- ✅ Accepts a **YouTube URL**
- ✅ Extracts **audio and transcribes** it using **AssemblyAI**
- ✅ Uses **Cohere** to generate a structured blog post (with title, sections, conclusion, etc.)
- ✅ Allows users to *Save it* in their account and **copy it**
- ✅ Fast, simple, and intuitive UI

---

## 🚀 Features

| Feature                     | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| 🎧 YouTube Audio Extraction | Extracts audio from a video link                                            |
| ✍️ AI Blog Generation       | Uses OpenAI to convert transcript into a blog post                          |
| 🔥 Django Backend           | High-performance backend built on Django                                    |
| 🎨 Tailwind CSS             | Minimalistic UI powered by Tailwind CSS                                     |
| 🗄️ Aiven Postgres Database  | Limited storage up 1GB with Aiven free tier                                 |
| 🌍 Render Deployment        | Deployed on [Render](https://render.com)                                    |
| 📦 Environment Management   | Uses `.env` for storing API keys and config variables                       |

---

## 🛠️ Tech Stack
- **Frontend:** HTML,Tailwind CSS, JS
- **Backend:** Python Django 
- **AI Models:** cohere (Text Summarization API)
- **Speech-to-Text:** AssemblyAI (Audio to Text generator)
- **Deployment:** Render.com
- **Language:** Python 3.10+
- **Others:** yt-dlp, requests, gunicorn, others

---

### ⚠️ Known Issue: YouTube Video Unavailability on Render

> **Problem:**  
> When deployed on platforms like **Render**, YouTube videos may return the following error during title extraction or audio download using `yt-dlp`:
> 
> 
> `ERROR: [youtube] <video_id>: Video unavailable. This content isn’t available. WARNING: The provided YouTube account cookies are no longer valid.`
> 
> **Why This Happens:**  
> YouTube enforces stricter access policies for hosted environments. This results in public videos sometimes being blocked unless browser cookies are supplied—something this app **intentionally avoids** for security and portability reasons.

* * *

### ✅ Solutions

#### 🔹 Option 1: Run Locally

To avoid this issue altogether, it’s recommended to **run the project locally**, where YouTube access is typically unrestricted.

---

1. **🚀 Clone the Repository**:
    ```bash
    git clone https://github.com/sai-krishna-kotha/ai_blog_app.git
    cd ai_blog_app
    ```
2. **🐍 Set Up Virtual Environment**:(in linux)
   ```bash
   python3 -m venv .venv
   source .myvenv/bin/activate
   ```
3. **⚙️ Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **🛢️ Aiven PostgreSQL Database Setup**:

    1. *Create a PostgreSQL Instance* on [Aiven.io](https://aiven.io).
    2. *Enable “Replication”* when creating a database user (important for Django).
    3. *Get Connection Details*: Host, Port, Database Name, Username, Password.

    4. *Access PostgreSQL via terminal* (optional but useful):
        ```bash
        psql -h <hostname> -U <username> -p <port> -d postgres
        ```
    5. *You are asked to enter your password*
    6. *Create database*
        ```bash
        CREATE DATABASE your_db_name;
        ```
3. **🌿 Export Environment Variables to Virtual Environment**: (on linux)

    ``In your terminal (while the virtual environment is activated), set the required environment variables:``
   ```bash
   export ASSEMBLYAI_API_KEY=your_assemblyai_api_key
   export COHERE_API_KEY=your_cohere_api_key
   export SECRET_KEY='your_django_secret_key'
   export DEBUG=True  # Use False in production
   export DATABASE_URL=postgres://<username>:<password>@<hostname>:<port>/<db_name>?sslmode=require
   ```
2. **🗃️ Apply Migrations (only once)**: (on linux)
   ```bash
   python3 manage.py migrate
   ```
4. **🚀 Start the Server**:
   ```bash
   python3 manage.py runserver
   ```
#### 🔹 Option 2: Use Demo Credentials (Read-Only)

You can try the live demo (hosted on Render) using the following credentials:
```bash
   Username: kothasaikrishna
   Password: 12345
     

=> ⚠️ Due to the YouTube restriction explained above, some features (like video title fetch or transcription) may not work in the demo environment.