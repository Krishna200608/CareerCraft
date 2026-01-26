# Database Schema (MongoDB)

CareerCraft uses MongoDB with Mongoose ODM.

## Collections

### 1. Users (`users`)
Stores user identity and profile information.
*   `username` (String, Unique, Index): Public handle.
*   `email` (String, Unique): Login identifier.
*   `password` (String): Bcrypt hash.
*   `oauthProviders` (Object): IDs for Google/GitHub linking.
*   `address`, `city`, `country`: Profile details.
*   `github`, `leetcode`, `codeforces`: Coding platform links.
*   `createdAt`: Timestamp.

### 2. Resumes (`resumes`)
Stores metadata for uploaded resume files.
*   `userId` (ObjectId -> User): Owner of the resume.
*   `originalName` (String): Original filename.
*   `cloudinaryUrl` (String): Public URL for the file.
*   `cloudinaryPublicId` (String): ID for deletion.
*   `text` (String): Extracted full text (cached from ML service).
*   `analysis` (Object): Last analysis result (Skills, ATS Score).

### 3. CoverLetters (`coverletters`)
Stores generated cover letters.
*   `userId` (ObjectId -> User): Owner.
*   `companyName` (String): Target company.
*   `jobTitle` (String): Target role.
*   `content` (Object): Structured content (Greeting, Body, Closing).
*   `createdAt`: Timestamp.

## Relationships
*   **1-to-Many**: A `User` can have multiple `Resumes`.
*   **1-to-Many**: A `User` can have multiple `CoverLetters`.

## Indexing Strategy
*   `email` and `username` on `User` collection are indexed for fast login/lookup.
