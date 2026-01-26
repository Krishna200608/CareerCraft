# Authentication & Security

CareerCraft uses **JWT (JSON Web Tokens)** for stateless authentication.

## Logic Flow

1.  **Login/Signup**:
    *   User submits credentials to `/api/auth/signin`.
    *   Backend verifies credentials (using `bcrypt` to compare password hashes).
    *   Backend generates a JWT signed with `JWT_SECRET`.
    *   Token contains: `_id`, `email`, `username`.
    *   Token is sent back in **Response Body** AND set as an **HTTP-Only Cookie** (`jwtToken`).

2.  **Protected Requests**:
    *   Frontend sends request to protected API (e.g., `/api/resumes`).
    *   **Middleware (`auth.middleware.js`)** intercepts request.
    *   Checks for token in `req.cookies.jwtToken` OR `Authorization: Bearer <token>` header.
    *   Verifies token signature.
    *   Fatches User from DB (`User.findById`).
    *   Attaches `req.user` to the request object.
    *   Passes control to the Controller.

## Security Measures
*   **Hashing**: Passwords are never stored in plain text. We use `bcrypt` with salt rounds (10).
*   **HTTP-Only Cookies**: Prevents XSS attacks from accessing the token via JavaScript.
*   **Validation**: Inputs are checked for presence and type before processing.

## OAuth
*   Supported Providers: **Google**, **GitHub**.
*   Flow:
    1.  Frontend redirects to `/api/auth/oauth/:provider`.
    2.  User consents on Provider page.
    3.  Provider redirects back to `/api/auth/oauth/:provider/callback`.
    4.  Backend issues JWT and redirects to Frontend with token.
