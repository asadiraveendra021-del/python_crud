the file name shouls be always in lowercase and no capital letter in between the file name . use _ for seprating.

Create Project Folder
Ex:
mkdir fastapi-project
cd fastapi-project

Create main.py File like bellow
======================
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI project is running!"}
==========================


1)Run bellow two command to setup environment to run the python projec
  => python -m venv venv
  => .\venv\Scripts\activate

2)Install fast API and Unicorn which are required to excute teh project because we are doing developemnet in fast API and unicors is to run the python project
  => pip install fastapi uvicorn

3)Run the bellow command to start the pythion fast API application
  => uvicorn main:app --reload

by default Swagger documentation we can access at http://127.0.0.1:8000/docs#/


# FastAPI User Management Project

## Project Overview

This project is a REST API built with FastAPI and SQLAlchemy. It provides user management, user profiles, and posts with proper authentication and logging.

## Code Flow Explanation

### 1. Application Start

* The entry point is `main.py`.
* FastAPI app is created.
* All database tables are created automatically using SQLAlchemy `Base.metadata.create_all()`.
* Routers (`users`, `profiles`, `posts`) are included.

### 2. User Registration and Login

* **Register**: User sends POST request to `/users/register` with username, email, and password.

  * System checks if username already exists.
  * Password is hashed and user is saved to the database.
  * Logs are generated for successful registration or warnings if username is taken.
* **Login**: User sends POST request to `/users/login`.

  * System verifies username and password.
  * On success, JWT token is created and returned.
  * Logs are generated for login attempts and success/failure.

### 3. User Profiles (One-to-One Relationship)

* **Create Profile**: POST `/profiles/{user_id}` with JWT token.

  * System checks if the user exists and if a profile already exists.
  * If valid, a new profile is created and linked to the user.
  * Logs indicate creation success or any warnings.
* **Get Profile**: GET `/profiles/{user_id}`.

  * Returns the profile details for a user.
  * Logs track retrieval and warnings if profile is not found.

### 4. Posts (One-to-Many Relationship)

* **Create Post**: POST `/posts/user/{user_id}`.

  * Creates a post linked to the user.
  * Logs track the creation event.
* **Read Posts**: GET `/posts/` or `/posts/{post_id}`.

  * Returns all posts or a specific post.
  * Logs indicate retrieval actions.
* **Update Post**: PUT `/posts/{post_id}`.

  * Updates title/content of a post.
  * Logs track the update operation.
* **Delete Post**: DELETE `/posts/{post_id}`.

  * Deletes a specific post.
  * Logs track the deletion.

### 5. Authentication

* JWT tokens are used to secure profile and post endpoints.
* `get_current_user` dependency ensures only authenticated users can access protected routes.
* Tokens are verified in each request automatically using FastAPI dependencies.

### 6. Logging

* Centralized logging using `logger.py`.
* Logs include info and warning levels.
* Tracks all CRUD operations, authentication events, and errors.
* Logs can be written to console or file for auditing and debugging.

### 7. Database Relationships

* **User ↔ UserProfile**: One-to-One mapping; a user can have only one profile.
* **User ↔ Post**: One-to-Many mapping; a user can have multiple posts.
* SQLAlchemy handles relationships and cascading actions automatically.

### 8. Modular Structure

* **Models**: Define database tables and relationships.
* **Schemas**: Pydantic models for request/response validation.
* **Services**: Handling APi endpoint core logic/Bussiness logic.
* **Routers**: Define endpoints for users, profiles, and posts.
* **Auth**: Handles password hashing and JWT token generation.
* **Logger**: Centralized logging.
* **Database**: Session and engine management.

This structure ensures a clean, modular, and scalable FastAPI application that is easy to maintain and extend.


### 9. Email Sending and Scheduling 
* I have implemented Email Sending and Scheduler to send emails as well. when ever a post is saved created then i am creating a row in email_Queue table with to email address , email body and the status so that for every one min a scheduler will trigger and fetch teh ppending Emails from Email Queue table and send he mail as soon as email sent successfully then he status marked as Sent 

### 10. External API Implementation

* I have implemented External API to retrive teh hotel Data and save that data in our DB by creating Data base tables . while writing code also i have added comments and loggers for easy undertsnading 