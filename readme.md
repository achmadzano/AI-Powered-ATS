# AI-Powered Applicant Tracking System (ATS)

An intelligent applicant tracking system that helps recruiters match candidate CVs with available job roles using AI technology.

## 📋 Overview

This system uses AI to analyze candidate resumes/CVs and automatically match them with appropriate job positions based on skills, experience, and qualifications. The application provides an intuitive interface for recruiters to manage the entire candidate matching process.

## 🏗️ Project Structure

```
📂 project-root/
│── 📂 backend/        # Backend using FastAPI
│   │── .env.example   # Environment configuration example
│   │── cv_extractor.py # Text extraction from CVs
│   │── database.py    # MongoDB connection
│   │── main.py        # Main backend endpoints
│   │── matcher.py     # AI module for CV-role matching
│   │── models.py      # Data models (Pydantic)
│   │── requirements.txt # Backend dependencies
│
│── 📂 frontend/       # Frontend using Streamlit
│   │── .env.example   # Environment configuration example
│   │── app.py         # Application UI built with Streamlit
│   │── requirements.txt # Frontend dependencies
│
│── README.md          # Project documentation
```

## 🚀 Technologies

### Backend (FastAPI)
- **FastAPI**: Web framework for building APIs quickly and efficiently
- **Pydantic**: Data validation and settings management
- **MongoDB**: Database for storing job roles and CVs
- **LangChain (SambaNova)**: AI model for CV-role matching
- **PyMuPDF (fitz)**: Text extraction from PDF files
- **python-docx**: Text extraction from Word (DOCX) files

### Frontend (Streamlit)
- **Streamlit**: Python framework for building interactive UIs
- **Requests**: HTTP library for API communication

## 🔧 Installation

### Prerequisites
- Python 3.8+
- MongoDB
- Git

### 1. Clone Repository
```bash
git clone <repo-url>
cd project-root
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Activate virtual environment
# For Linux/macOS:
source venv/bin/activate
# For Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and configure your settings:
```
SAMBANOVA_API_KEY = ""
MONGO_URI = 
```

Run the backend server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
python -m venv venv

# Activate virtual environment (as above)
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`:
```
MONGO_URI = 
PROD_BE_URL = 
DEV_BE_URL =  
```

Run the frontend application:
```bash
streamlit run app.py
```

## 🎯 Key Features

- ✅ **Job Role Management**: Add, view, and manage job positions
- ✅ **CV Processing**: Upload CVs in PDF/DOCX formats
- ✅ **AI Matching**: Automatically match CVs with suitable roles
- ✅ **Match Scoring**: View match percentage and detailed analysis
- ✅ **Candidate Dashboard**: Review and filter matched candidates
- ✅ **Export Results**: Download matching results in various formats

## 👨‍💻 Usage

1. Access the Streamlit UI at `http://localhost:8501`
2. Add job roles with detailed requirements
3. Upload candidate CVs (PDF/DOCX formats supported)
4. View AI-generated matching results
5. Filter and sort candidates by match score
6. Export candidate reports

## 📌 Important Notes

- Ensure MongoDB is running before starting the application
- The backend API must be active for the frontend to function
- For optimal matching results, use detailed job descriptions and properly formatted CVs
- Supported file formats: PDF, DOCX

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.