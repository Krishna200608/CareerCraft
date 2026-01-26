# CareerCraft Architecture

## System Overview

CareerCraft uses a **Service-Oriented Architecture** (SOA) with a unified frontend orchestrating interactions between a persistent Backend API and a stateless ML Service. This hybrid approach enables high-performance AI inference without overloading the main application server.

### Key Components

1.  **Frontend (Next.js)** (Port 3000)
    *   **Role**: Main user interface and orchestrator.
    *   **Tech Stack**: Next.js 16, React 19, Tailwind CSS 4, Lucide React.
    *   **Responsibilities**:
        *   Rendering UI (Server & Client Components).
        *   Managing Authentication state (Context/Cookies).
        *   Communicating with Backend for user data.
        *   Communicating directly with ML Service for real-time analysis.
    
2.  **Backend (Node.js/Express)** (Port 5000)
    *   **Role**: Persistent data manager and authentication provider.
    *   **Tech Stack**: Express.js, Mongoose, JWT, Bcrypt.
    *   **Database**: MongoDB (User data, Profiles, Saved Cover Letters).
    *   **Storage**: Cloudinary (Resume file storage).
    *   **Responsibilities**:
        *   User Authentication (Signup/Signin).
        *   Profile Management.
        *   storing and retrieving saved resources (Resumes, Cover Letters).

3.  **ML Service (FastAPI)** (Port 8001)
    *   **Role**: Stateless intelligence engine.
    *   **Tech Stack**: Python, FastAPI, Spacy, Scikit-Learn, Sentence-Transformers.
    *   **Responsibilities**:
        *   Resume Parsing (Text Extraction from PDF/DOCX).
        *   Resume Analysis (Keyword scoring, feedback).
        *   Job Matching (Cosine similarity).
        *   Cover Letter Generation (Template/GenAI logic).

---

## High-Level Architecture Diagram

```ascii
+----------------------+       +----------------------+
|   User Client        |-------|   Third-Party Services|
|  (Browser/Next.js)   |       | (Cloudinary/MongoDB) |
+----------------------+       +----------------------+
       |          |
       | (Auth /  | (Analysis /
       | Persistence) Inference)
       v          v
+------------+  +-------------+
|  Backend   |  | ML Service  |
| (Express)  |  |  (FastAPI)  |
+------------+  +-------------+
       |
+------------+
|  Database  |
| (MongoDB)  |
+------------+
```

## Data Flows

### 1. Resume Analysis
*   **User Action**: Uploads a resume file on "Resume Analysis" page.
*   **Flow**: Frontend -> **ML Service** (`POST /resume/extract-text` & `/resume/analyze`).
*   **Result**: Instant feedback displayed to user. No persistent storage in DB until explicitly saved.
*   **Rationale**: Reduces load on Backend; keeps analysis fleeting and fast.

### 2. Resume Upload (Profile)
*   **User Action**: Uploads a resume on "Upload Resume" page.
*   **Flow**: Frontend -> **Backend** (`POST /api/resumes/upload`).
*   **Result**: File stored in **Cloudinary**, link saved in **MongoDB** User Profile.

### 3. Cover Letter Generation
*   **User Action**: Enters job details and analyzes resume.
*   **Flow**: Frontend -> **ML Service** (`POST /cover-letter/generate-cover-letter`).
*   **Result**: Generated text returned to Frontend.
*   **Save Action**: User clicks "Save" -> Frontend -> **Backend** (`POST /api/cover-letters`).

## Security & Authentication

*   **JWT Strategies**: Backend issues JWTs upon login. Frontend includes Bearer tokens in requests to Backend.
*   **ML Service Security**: Currently open (CORS allowing all for development) or protected via internal tokens (Future improvement).
*   **Environmental Variables**: All sensitive keys (DB URI, Cloudinary Secrets) are stored in `.env` files and never exposed to the client.

## Scalability Considerations

*   **Stateless ML**: The ML Service is stateless, making it easy to scale horizontally on GPU/CPU-optimized instances.
*   **CDN**: frontend assets served via Next.js optimization.
*   **Database**: MongoDB handles flexible schema for evolving user profiles.
