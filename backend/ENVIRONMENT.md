# Environment Configuration

The backend requires specific environment variables to function. These should be defined in a `.env` file in the `backend/` root directory.

## Required Variables

| Variable | Description | Example |
| :--- | :--- | :--- |
| `PORT` | Port number for the server to listen on | `5000` |
| `MONGODB_URI` | Connection string for MongoDB database | `mongodb://localhost:27017/careercraft` |
| `JWT_SECRET` | Secret key used to sign JSON Web Tokens | `your-super-secret-key-123` |
| `CLIENT_URL` | URL of the frontend application (for CORS) | `http://localhost:3000` |

## Cloudinary (File Storage)

Required for Resume Uploads to work.

| Variable | Description |
| :--- | :--- |
| `CLOUDINARY_CLOUD_NAME` | Your Cloudinary Cloud Name |
| `CLOUDINARY_API_KEY` | Your Cloudinary API Key |
| `CLOUDINARY_API_SECRET` | Your Cloudinary API Secret |

## OAuth (Optional)

Required only if using Social Login (Google/GitHub).

| Variable | Description |
| :--- | :--- |
| `GOOGLE_CLIENT_ID` | OAuth Client ID from Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | OAuth Client Secret from Google Cloud Console |
| `GITHUB_CLIENT_ID` | OAuth Client ID from GitHub Developer Settings |
| `GITHUB_CLIENT_SECRET` | OAuth Client Secret from GitHub Developer Settings |

## Setup

1.  Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```
2.  Fill in the values.
3.  Restart the server:
    ```bash
    npm run dev
    ```
