# FastAPI User Authentication API

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)

A robust User Login and Authentication API built with **FastAPI**, **PostgreSQL**, and **Alembic** for database migrations. This project provides a complete backend solution for managing user accounts, including registration, login, OTP verification, and password management.

---

## 📖 Table of Contents
* [Features](#-features)
* [Tech Stack](#-tech-stack)
* [Getting Started](#-getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation & Setup](#installation--setup)
* [Running the Application](#-running-the-application)
* [API Endpoints](#-api-endpoints)
* [Contributing](#-contributing)
* [License](#-license)

---

## ✨ Features

This API provides the following core functionalities:

-   **User Registration:** Create a new user account.
-   **User Login:** Authenticate and receive an access token.
-   **OTP Verification:** Generate and verify OTPs for email verification.
-   **Password Management:** Securely handle forgot and reset password flows.
-   **CRUD Operations:** Perform Create, Read, Update, and Delete operations on users.

---

## 💻 Tech Stack

-   **Framework:** FastAPI
-   **Database:** PostgreSQL
-   **Database Migration:** Alembic
-   **ORM:** SQLAlchemy
-   **Schema Validation:** Pydantic
-   **Authentication:** JWT (JSON Web Tokens)

---

## 🚀 Getting Started

Follow these instructions to get a local copy of the project up and running for development and testing.

### Prerequisites

-   Python 3.9+
-   PostgreSQL installed and running.
-   A code editor like VS Code.

### Installation & Setup

1.  **Clone the Repository**
    ```sh
    git clone [https://github.com/Soul-Will/user_login_and_authentication_API.git](https://github.com/Soul-Will/user_login_and_authentication_API.git)
    cd user_login_and_authentication_API
    ```

2.  **Create a Virtual Environment**
    It's recommended to use a virtual environment to manage project dependencies.
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    Install all the required packages from the `requirements.txt` file.
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory by copying the example file.
    ```sh
    # Create a .env file and add your database credentials and other settings.
    # Example:
    DATABASE_URL="postgresql://user:password@host:port/database_name"
    SECRET_KEY="your_secret_key"
    ```
    *Update the `DATABASE_URL` with your actual PostgreSQL connection details.*

5.  **Run Database Migrations**
    Alembic will set up the necessary tables in your database based on the models defined.
    ```sh
    alembic upgrade head
    ```

---

## ⚡ Running the Application

Once the setup is complete, you can run the application using Uvicorn.

```sh
uvicorn main:app --reload
