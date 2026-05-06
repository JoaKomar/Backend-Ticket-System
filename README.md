# Ticket System API

Backend REST API built with FastAPI for managing support tickets, authentication, comments, and admin assignment.

## Features

- User registration and login
- JWT authentication
- Role-based authorization (user/admin)
- Ticket creation and management
- Automatic admin assignment
- Ticket comments
- Soft delete
- PostgreSQL integration
- Pytest testing

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT
- Bcrypt
- Pytest

## Installation

```bash
git clone <repo>
cd Ticket-System
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt