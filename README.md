FastAPI User Authentication API
A robust User Login and Authentication API built with FastAPI, PostgreSQL, and Alembic for database migrations. This project provides a complete backend solution for managing user accounts, including registration, login, OTP verification, and password management.

📖 Table of Contents
Features

Tech Stack

Getting Started

Prerequisites

Installation & Setup

Running the Application

API Endpoints

Contributing

License

✨ Features
This API provides the following core functionalities:

User Registration: Create a new user account.

User Login: Authenticate and receive an access token.

OTP Verification: Generate and verify OTPs for email verification.
--   Password Management: Securely handle forgot and reset password flows.

CRUD Operations: Perform Create, Read, Update, and Delete operations on users.

💻 Tech Stack
Framework: FastAPI

Database: PostgreSQL

Database Migration: Alembic

ORM: SQLAlchemy

Schema Validation: Pydantic

Authentication: JWT (JSON Web Tokens)

🚀 Getting Started
Follow these instructions to get a local copy of the project up and running for development and testing.

Prerequisites
Python 3.9+

PostgreSQL installed and running.

A code editor like VS Code.

Installation & Setup
Clone the Repository

Bash

git clone https://github.com/Soul-Will/user_login_and_authentication_API.git
cd user_login_and_authentication_API
Create a Virtual Environment
It's recommended to use a virtual environment to manage project dependencies.

Bash

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install Dependencies
Install all the required packages from the requirements.txt file.

Bash

pip install -r requirements.txt
Configure Environment Variables
Create a .env file in the root directory by copying the example file.

Bash

# Create a .env file and add your database credentials and other settings.
# Example:
DATABASE_URL="postgresql://user:password@host:port/database_name"
SECRET_KEY="your_secret_key"
Update the DATABASE_URL with your actual PostgreSQL connection details.

Run Database Migrations
Alembic will set up the necessary tables in your database based on the models defined.

Bash

alembic upgrade head
⚡ Running the Application
Once the setup is complete, you can run the application using Uvicorn.

Bash

uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000. You can access the interactive API documentation at http://127.0.0.1:8000/docs.

📡 API Endpoints
The API provides the following endpoints:

HTTP Method	Endpoint	Description
POST	/users/register	Register a new user
POST	/users/login	Authenticate a user and get a token
GET	/users/	Get a list of all users
GET	/users/{user_id}	Search for a specific user by ID
PUT	/users/{user_id}	Update user details
DELETE	/users/{user_id}	Delete a user
POST	/otp/generate	Generate OTP for email verification
POST	/otp/verify	Verify OTP for email verification
POST	/password/forgot	Request a password reset
POST	/password/reset	Reset the user's password

Export to Sheets
🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Fork the Project.

Create your Feature Branch (git checkout -b feature/AmazingFeature).

Commit your Changes (git commit -m 'Add some AmazingFeature').

Push to the Branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📄 License
This project is distributed under the MIT License. See the LICENSE file for more information.
