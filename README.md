# CareerCraft — Resume Evaluator & Job Match Assistant

CareerCraft is an **AI-powered career enhancement platform** designed to help job seekers optimize their resumes, evaluate job-fit, and generate tailored cover letters.  
It uses modern **AI, NLP, and web technologies** to simulate real-world Applicant Tracking Systems (ATS) and hiring workflows.

The platform provides actionable insights that improve resume quality, skill alignment, and overall job readiness.

---

## 🚀 Key Features

### 📝 Resume Analyzer (ATS Optimization)
- Upload **PDF / DOCX** resumes
- ATS-style scoring based on:
  - Keyword alignment
  - Resume structure & formatting
  - Readability
  - Section completeness
- Detailed improvement suggestions

---

### 🎯 Skill Match & Job Fit Scoring
- Paste or select a **target job description**
- Get:
  - Job match percentage
  - Identified missing skills
  - Role-specific improvement tips
- Personalized upskilling recommendations with learning resources

---

### ✍️ AI Cover Letter Generator
- Generates **professionally tailored cover letters**
- Uses:
  - Resume content
  - Job description insights
- Supports tone customization:
  - Formal
  - Confident
  - Friendly
- One-click **PDF export**

---

### 📊 User Dashboard & History Tracking
- Secure user authentication
- Store:
  - Resumes
  - Generated cover letters
  - Job match results
- Track progress across multiple applications
- Manage multiple resume versions

---

## 🧠 System Architecture

CareerCraft follows a **microservice-based architecture**:

CareerCraft/
├── frontend/ # User Interface (Next.js)  
├── backend/ # API & Authentication (Node.js / Express)  
└── ml-service/ # AI & NLP Engine (FastAPI)  

### Architecture Flow

Frontend → Backend → ML Service → Backend → Frontend


---

## 🛠️ Tech Stack

### Frontend
- Next.js 
- Tailwind CSS
- Axios

### Backend
- Node.js
- Express.js
- MongoDB
- JWT Authentication

### ML Service
- Python
- FastAPI
- NLP-based keyword & role matching
- Rule-based + AI-expandable models

---

## ⚙️ Setup & Installation

### 🐳 Docker Setup (Recommended)

#### Prerequisites
- Docker and Docker Compose installed on your system
- Git

#### Quick Start with Docker

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/CareerCraft.git
cd CareerCraft
```

2. **Configure Environment Variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your configuration
# Required: Cloudinary credentials, JWT secret
# Optional: Google/GitHub OAuth credentials
```

3. **Start All Services**
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

4. **Access the Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- ML Service: http://localhost:8001
- MongoDB: localhost:27017

5. **Stop Services**
```bash
docker-compose down
```

#### Docker Commands

```bash
# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f ml-service

# Rebuild a specific service
docker-compose up --build backend

# Stop and remove all containers
docker-compose down -v
```

### 🛠️ Manual Setup (Without Docker)

#### Prerequisites
- Node.js (v18+)
- Python (v3.11+)
- MongoDB
- Git

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/CareerCraft.git
cd CareerCraft
```

#### 2️⃣ Start ML Service
```bash
cd ml-service
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

#### 3️⃣ Start Backend
```bash
cd backend
npm install
cp .env.production .env  # Configure with your credentials
npm run dev
```

#### 4️⃣ Start Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🔧 Environment Variables

### Required Variables
- `MONGODB_URI`: MongoDB connection string
- `CLOUDINARY_CLOUD_NAME`: Cloudinary cloud name
- `CLOUDINARY_API_KEY`: Cloudinary API key
- `CLOUDINARY_API_SECRET`: Cloudinary API secret
- `JWT_SECRET`: Secret for JWT token signing

### Optional Variables
- `GOOGLE_CLIENT_ID` & `GOOGLE_CLIENT_SECRET`: Google OAuth
- `GITHUB_CLIENT_ID` & `GITHUB_CLIENT_SECRET`: GitHub OAuth
- `OLLAMA_BASE_URL`: Ollama service URL (default: http://localhost:11434)

### Service URLs
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- ML Service: http://localhost:8001
- MongoDB: localhost:27017

---

## 📝 Docker Development Notes

### Service Architecture
- **frontend**: Next.js application (Port 3000)
- **backend**: Node.js/Express API (Port 5000)
- **ml-service**: Python/FastAPI ML service (Port 8001)
- **mongodb**: MongoDB database (Port 27017)

### Volume Mounts
- Source code is mounted for live development
- Node modules are isolated to prevent conflicts
- MongoDB data persists in Docker volume

### Health Checks
All services include health checks for monitoring:
- Backend: HTTP check on `/api/health`
- ML Service: HTTP check on `/`
- Frontend: Process monitoring

### Production Deployment
For production deployment:
1. Update environment variables with production values
2. Remove volume mounts for source code
3. Use proper secrets management
4. Configure reverse proxy (nginx/traefik)
5. Set up SSL certificates

---

## 👨‍💻 Contributors

See CONTRIBUTORS for the full list of contributors.

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ Acknowledgements

Inspired by real-world ATS systems and modern hiring workflows.  
Built for learning, experimentation, and real-world impact.
