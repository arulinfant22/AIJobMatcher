from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import userlogin, Resume, CoverLetter, tb_login
from django.contrib import messages
import os
import fitz  # PyMuPDF
import requests
from django.conf import settings
from decouple import config
from django.utils.timezone import now, timedelta

# Create your views here.
def index(request):
    return render(request,'index.html')
def signup(request):
    return render(request,'signup.html')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        # Check if passwords match
        if password != confirmpassword:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Check if username already exists
        if userlogin.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        # Check if email already exists
        if userlogin.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        # Save the user with hashed password
        hashed_password = make_password(password)
        user = userlogin(username=username, email=email, password=hashed_password, confirmpassword=make_password(confirmpassword))
        user.save()

        messages.success(request, 'Registered successfully! Please log in.')
        return render(request,'login.html')  # Redirect to login page

    return render(request, 'signup.html')

def login(request):
    return render(request,'login.html')

def loginaction(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            login_user = userlogin.objects.get(email=email)
            if check_password(password, login_user.password):
                request.session['user_id'] = login_user.id  # Set session for login
                request.session['username'] = login_user.username
                messages.success(request, "Login successful!")
                return redirect('resume_upload')  # redirect to resume upload page
            else:
                messages.error(request, "Invalid email or password")
                return redirect('login')
        except userlogin.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, 'login.html')

RAPIDAPI_KEY = config("RAPIDAPI_KEY")
RAPIDAPI_HOST = config("RAPIDAPI_HOST")

# Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.lower()

# Extract simple keywords (or upgrade to NLP model)
def extract_keywords(resume_text):
    tech_keywords = [
        "python", "django", "flask", "react", "sql", "excel", "machine learning",
        "ml", "data analysis", "aws", "javascript", "html", "css", "node", "pandas", "numpy"
    ]
    return [kw for kw in tech_keywords if kw in resume_text]

# Fetch jobs from API using extracted keywords
def fetch_jobs_from_api(keywords):
    url = "https://jsearch.p.rapidapi.com/search"
    all_jobs = []
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    for kw in keywords:
        params = {
    "query": kw,
    "page": "1",
    "num_pages": "1",
    "location": "India",
    "country": "IN" , # Add this!
    "date_posted": "3days"
}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            for job in data.get("data", []):
                all_jobs.append({
                    "job_title": job.get("job_title", ""),
                    "employer_name": job.get("employer_name", ""),
                    "job_city": job.get("job_city", ""),
                    "job_country": job.get("job_country", ""),
                    "job_apply_link": job.get("job_apply_link", "#"),
                    "job_posted_at": job.get("job_posted_at_datetime_utc", "")[:10]
                })
    return all_jobs

def resume_upload(request):
    username = request.session.get('username', '')  # ✅ Get from session
    if request.method == "POST" and request.FILES.get("resume"):
        resume_file = request.FILES["resume"]

        # Save resume to temp folder
        temp_dir = os.path.join(settings.BASE_DIR, "temp")
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, resume_file.name)

        with open(file_path, "wb+") as destination:
            for chunk in resume_file.chunks():
                destination.write(chunk)

        resume_text = extract_text_from_pdf(file_path)
        keywords = extract_keywords(resume_text)
        jobs = fetch_jobs_from_api(keywords)

        return render(request, "up.html", {
            "file_name": resume_file.name,
            "matched_jobs": jobs
        })

    return render(request,'view.html',{"username": username})

def resume(request):
    return render(request,'resume.html')

def resumemaker(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        details = request.POST.get('details')
        user = Resume(user=user, details=details)
        user.save()
        context = {
            # Personal Info
            'name': request.POST.get('name', ''),
            'email': request.POST.get('email', ''),
            'phone': request.POST.get('phone', ''),
            'linkedin': request.POST.get('linkedin', ''),
            'github': request.POST.get('github', ''),
            'summary': request.POST.get('summary', ''),

            # Technical Skills
            'languages': request.POST.get('languages', ''),
            'frameworks': request.POST.get('frameworks', ''),
            'tools': request.POST.get('tools', ''),
            'database': request.POST.get('database', ''),

            # Projects
            'project1_title': request.POST.get('project1_title', ''),
            'project1_duration': request.POST.get('project1_duration', ''),
            'project1_stack': request.POST.get('project1_stack', ''),
            'project1_point1': request.POST.get('project1_point1', ''),
            'project1_point2': request.POST.get('project1_point2', ''),
            'project1_point3': request.POST.get('project1_point3', ''),

            'project2_title': request.POST.get('project2_title', ''),
            'project2_duration': request.POST.get('project2_duration', ''),
            'project2_stack': request.POST.get('project2_stack', ''),
            'project2_point1': request.POST.get('project2_point1', ''),
            'project2_point2': request.POST.get('project2_point2', ''),
            'project2_point3': request.POST.get('project2_point3', ''),

            # Experience
            'exp_company': request.POST.get('exp_company', ''),
            'exp_position': request.POST.get('exp_position', ''),
            'exp_duration': request.POST.get('exp_duration', ''),
            'exp_location': request.POST.get('exp_location', ''),
            'exp_point1': request.POST.get('exp_point1', ''),
            'exp_point2': request.POST.get('exp_point2', ''),
            'exp_point3': request.POST.get('exp_point3', ''),

            # Education
            'edu1_institute': request.POST.get('edu1_college', ''),
            'edu1_degree': request.POST.get('edu1_degree', ''),
            'edu1_duration': request.POST.get('edu1_year', ''),

            'edu2_institute': request.POST.get('edu2_college', ''),
            'edu2_degree': request.POST.get('edu2_degree', ''),
            'edu2_duration': request.POST.get('edu2_year', ''),

            # Certifications
            'cert1': request.POST.get('cert1', ''),
            'cert2': request.POST.get('cert2', ''),
        }

        return render(request, 'resumemaker.html', context)

    return render(request, 'resume.html')

def cover(request):
    return render(request,'cover.html')

def coverletter_form(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        details = request.POST.get('details')
        user = CoverLetter(user=user, details=details)
        user.save()
        context = {
            'full_name': request.POST.get('user'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'company': request.POST.get('company'),
            'position': request.POST.get('position'),
            'intro': request.POST.get('intro'),
            'body': request.POST.get('details'),
            'closing': request.POST.get('closing'),
        }
        return render(request, 'coverletter.html', context)
    return render(request, 'cover.html')

def dashboard(request):
    total_users = userlogin.objects.count()
    total_resumes = Resume.objects.count()
    total_cover_letters = CoverLetter.objects.count()
    recent_users = userlogin.objects.order_by('created_at')[:7]
    past_days = [now() - timedelta(days=i) for i in range(6, -9, -1)]
    chart_labels = [day.strftime('%b %d') for day in past_days]
    resume_data = [Resume.objects.filter(created_at__date=day.date()).count() for day in past_days]
    user_data = [userlogin.objects.filter(created_at__date=day.date()).count() for day in past_days]
    coverletter_data = [CoverLetter.objects.filter(ccreated_at__date=day.date()).count() for day in past_days]
    return render(request,'dashboard.html',{'total_users': total_users,'total_resumes': total_resumes,
                                            'total_cover_letters': total_cover_letters,
                                            'recent_users': recent_users,'chart_labels': chart_labels,
                                            'resume_data': resume_data,'user_data': user_data,
                                            'coverletter_data': coverletter_data,})
    
def adminlogin(request):
    return render(request,'adminlogin.html')

def dashlogin(request):
    if request.method == "POST":
        
        try:
            login=tb_login.objects.get(username=request.POST['username'],password=request.POST['password'])
            
            return redirect('dash')  # Redirect to the desired page
        except tb_login.DoesNotExist :
            messages.error(request, "Invalid username or password")
            return redirect('adminlogin')  # Redirect back to login page

def logout(request):
    request.session.flush()  # Clear all session data
    messages.success(request, "Logged out successfully!")
    return redirect('index')
