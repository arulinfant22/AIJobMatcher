# AI Job Matcher

An intelligent job matching platform that analyzes resumes and suggests relevant job opportunities using AI-powered keyword extraction and external job APIs.

## Features

- **User Authentication**: Registration and login system
- **Resume Upload**: PDF resume parsing and text extraction
- **AI-Powered Matching**: Keyword extraction for skill matching
- **Job Search Integration**: Real-time job fetching from external APIs
- **Resume Builder**: Interactive resume creation tool
- **Cover Letter Generator**: Professional cover letter creation
- **Admin Dashboard**: Analytics and user management

## Tech Stack

- **Backend**: Django 5.0.6
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **PDF Processing**: PyMuPDF (fitz)
- **External APIs**: 
  - Google Custom Search API
  - RapidAPI JSearch API
- **Environment Management**: python-decouple

## Prerequisites

- Python 3.8+
- MySQL Server
- pip package manager

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AIJobMatcher
```

### 2. Create Virtual Environment
```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE AIJob;

# Update database credentials in .env file
```

### 5. Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
GOOGLE_API_KEY=your-google-api-key
GOOGLE_CSE_ID=your-google-cse-id
RAPIDAPI_KEY=your-rapidapi-key
RAPIDAPI_HOST=jsearch.p.rapidapi.com
```

### 6. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

## API Keys Setup

### Google Custom Search API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Custom Search API
3. Create credentials and get API key
4. Set up Custom Search Engine ID

### RapidAPI JSearch API
1. Sign up at [RapidAPI](https://rapidapi.com/)
2. Subscribe to JSearch API
3. Get your API key and host

## Project Structure

```
AIJobMatcher/
├── AIJobMatcher/          # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI configuration
├── JobMatcher/           # Main application
│   ├── models.py         # Database models
│   ├── views.py          # Business logic
│   ├── urls.py           # App URL routing
│   └── migrations/       # Database migrations
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── temp/                # Temporary file storage
└── .env                 # Environment variables
```

## Database Models

### User Authentication
- **userlogin**: User registration and login data
- **tb_login**: Admin authentication

### Content Management
- **Resume**: User resume details
- **CoverLetter**: Cover letter information

## Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/signup` | GET/POST | User registration |
| `/login` | GET/POST | User login |
| `/resume_upload` | GET/POST | Resume upload and analysis |
| `/resumemaker` | GET/POST | Resume builder |
| `/coverletter` | GET/POST | Cover letter generator |
| `/dash` | GET | Admin dashboard |
| `/adminlogin` | GET/POST | Admin login |

## Usage

### 1. User Registration
- Visit `/signup`
- Fill in username, email, and password
- Confirm password and submit

### 2. Login
- Use `/login` with registered credentials
- Session-based authentication

### 3. Resume Analysis
- Upload PDF resume via `/resume_upload`
- System extracts keywords and matches jobs
- View matched job opportunities

### 4. Resume Building
- Use `/resumemaker` for interactive resume creation
- Fill in personal details, skills, experience
- Generate formatted resume

### 5. Cover Letter Creation
- Access via `/coverletter`
- Input company and position details
- Generate professional cover letter

## Security Considerations

⚠️ **Important Security Notes**:

1. **Password Storage**: Currently stores passwords in plain text (requires immediate fix)
2. **API Keys**: Ensure `.env` is in `.gitignore`
3. **Debug Mode**: Disable `DEBUG=True` in production
4. **File Uploads**: Implement file validation and size limits

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Admin
Access admin panel at `/admin` with superuser credentials.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Known Issues

- Passwords stored without hashing (Critical security issue)
- Missing input validation on forms
- No rate limiting on API calls
- File upload security vulnerabilities
- Session management issues in logout

## Future Enhancements

- Implement password hashing with Django's auth system
- Add email verification for registration
- Implement job application tracking
- Add machine learning for better job matching
- Create user profiles and preferences
- Add notification system for new jobs

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository or contact the development team.

---

**⚠️ Security Warning**: This project contains security vulnerabilities that should be addressed before production deployment. See the "Security Considerations" section for details.
