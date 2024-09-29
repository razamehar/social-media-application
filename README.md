# Social Media API

This project is a RESTful API built with FastAPI to serve as a backend for a social media application. It allows users to create accounts, authenticate, create posts, like posts, and interact with other users' content.

## Features
- User authentication and registration
- CRUD operations for posts
- Liking and unliking posts
- OAuth2 authentication with JWT tokens

## Installation

### Requirements
- Python 3.10+
- PostgreSQL database

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/razamehar/social-media-application

2. Navigate to the project directory:
   ```bash
   cd social-media-application

3. Set up a virtual environment:
   ```bash
   python -m venv venv

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate

    - On Unix or MacOS:
      ```bash
      source venv/bin/activate

5. Install the required packages:
   ```bash
   pip install -r requirements.txt

6. Set up environment variables by creating a .env file in the project root directory:
   ```env
    database_hostname=<YOUR_DATABASE_HOSTNAME>
    database_port=<YOUR_DATABASE_PORT>
    database_password=<YOUR_DATABASE_PASSWORD>
    database_name=<YOUR_DATABASE_NAME>
    database_username=<YOUR_DATABASE_USERNAME>
    secret_key=<YOUR_SECRET_KEY>
    algorithm=<YOUR_JWT_ALGORITHM>
    access_token_expire_minutes=<EXPIRATION_TIME_IN_MINUTES>

7. Run the application:
   ```bash
   uvicorn app.main:app --reload

## USAGE
The API contains the following endpoints:

### Authentication
- POST /login - Log in and receive a JWT token for authenticated requests.

### Users
- POST /users/ - Create a new user.
- GET /users/{id} - Retrieve a specific user's information.

### Posts
- GET /posts/ - Retrieve all posts with optional search and pagination.
- POST /posts/ - Create a new post (authenticated).
- GET /posts/{id} - Retrieve a specific post by ID.
- PUT /posts/{id} - Update an existing post (authenticated).
- DELETE /posts/{id} - Delete an existing post (authenticated).

### Likes
- POST /like/ - Like or unlike a post (authenticated).

## Project Structure
- app/main.py - Entry point for the application.
- app/routers/ - Contains API routes for users, posts, likes, and authentication.
- app/database.py - Handles database connection.
- app/schema.py - Defines request and response schemas using Pydantic.
- app/utils.py - Utility functions for password hashing and validation.
- app/config.py - Settings configuration using environment variables.

## Contact
For any questions or clarifications, please contact Raza Mehar at [raza.mehar@gmail.com]. 
