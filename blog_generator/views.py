from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import yt_dlp
import cohere
import os
import json
import assemblyai as aai
from .models import BlogPost

# --------------------------- Home ---------------------------

@login_required
def index(request):
    return render(request, 'index.html')

# --------------------------- Blog Generation ---------------------------

@csrf_exempt
@login_required
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)

        title = yt_title(yt_link)
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': "Failed to get transcript"}, status=500)
        print(transcription)
        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error': "Failed to generate blog article"}, status=500)

        new_blog_article = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=yt_link,
            generated_content=blog_content,
        )
        print(type(blog_content))
        print(blog_content)

        return JsonResponse({'content': f"{blog_content[:500]}..."})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)



def yt_title(link):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        return info.get('title', 'No Title Found')


def download_audio(link):
    output_dir = settings.MEDIA_ROOT
    output_template = os.path.join(output_dir, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        filename = ydl.prepare_filename(info)
        mp3_filename = os.path.splitext(filename)[0] + '.mp3'
        return mp3_filename


def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = settings.ASSEMBLYAI_API_KEY

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    if os.path.exists(audio_file):
        os.remove(audio_file)
    print("You came here \n\n\n\n")
    print(transcript.text)
    return transcript.text

def get_blog_generation_prompt(transcription: str) -> str:
    """
    Takes a transcript and embeds it into a comprehensive prompt to generate a
    well-structured, Markdown-formatted blog post.
    """
    
    # Using a triple-quoted f-string for a clean, multi-line prompt.
    prompt = f"""
Act as an expert blog writer and content strategist, specializing in transforming spoken content into compelling, high-quality articles for platforms like Medium. Your task is to take the following transcript and write a complete, original, and seamless blog post formatted in clean, standard Markdown.

**CRITICAL INSTRUCTIONS:**
- The entire output MUST be a single, continuous block of Markdown-formatted text.
- The output must be a fully-formed article, ready to be published.
- Do NOT include any placeholders, bracketed instructions, or fields to be filled in (e.g., "[Conclusion]", "[Main Point 1]").
- Do NOT wrap the output in HTML tags.
- Synthesize the core ideas from the transcript into a new, well-structured written piece. Do not simply rephrase the transcript.

**CONTENT STRUCTURE REQUIREMENTS (Use Markdown):**

1.  **Title:** Start with a single, engaging H1 title (e.g., `# My Awesome Blog Title`).
2.  **Introduction:** Follow with a powerful and inspiring introduction that hooks the reader and introduces the central topic.
3.  **Body:**
    -   Structure the main content with clear paragraphs.
    -   Use H2 subheadings (e.g., `## A Key Idea`) to organize the major sections of the article for readability.
    -   Use bullet points (`*` or `-`) for lists of items.
    -   If quoting a key insight from the transcript, use Markdown blockquotes (`>`).
4.  **Key Takeaways Section (If Applicable):**
    -   Create a distinct section with an H2 subheading like `## Key Takeaways` and use a bulleted list to highlight the most important points.
5.  **Conclusion:** End with a strong concluding paragraph that summarizes the main message and offers a final, memorable thought or a clear call to action.

**Here is the transcript:**
\"\"\"
{transcription}
\"\"\"
"""
    return prompt



def generate_blog_from_transcription(transcription):
    """
    Generates a blog post from a transcription using the Cohere API.
    """
    # It's recommended to load the key securely, e.g., from environment variables or a settings file
    api_key = settings.COHERE_API_KEY 
    print("Step 1: Initializing Cohere client...\n")
    try:
        co = cohere.Client(api_key)
        prompt = get_blog_generation_prompt(transcription)
        print("Step 2: Sending request to Cohere...\n")
        
        response = co.chat(
            # CORRECTED: Use a valid model name like 'command-r'
            model="command-r", 
            message=prompt,
            preamble="You are a professional blog writer.",
            temperature=0.7,
            max_tokens=1000
        )

        print("Step 3: Got response!\n")
        return response.text.strip()

    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Blog generation failed: {e}"





# --------------------------- Blog List and Details ---------------------------

@login_required
def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    # print(blog_articles)
    return render(request, "all-blogs.html", {'blog_articles': blog_articles})

@login_required
def blog_details(request, pk):
    try:
        blog_article_detail = BlogPost.objects.filter(id=pk, user=request.user).first()
        # print("I am in blog")
        # print(type(blog_article_detail))
        # print(blog_article_detail)
        return render(request, 'blog-details.html', {'blog_article_details': blog_article_detail})
    except BlogPost.DoesNotExist:
        return redirect('/')

# --------------------------- Authentication ---------------------------

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error_message': "Invalid username or password"})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeatPassword')

        if password != repeat_password:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match'})

        try:
            user = User.objects.create_user(username, email, password)
            login(request, user)
            return redirect('/')
        except:
            return render(request, 'signup.html', {'error_message': 'Error creating account'})

    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')
