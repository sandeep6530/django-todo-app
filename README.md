# Todo Application (Django)

## Features
- User authentication (login/logout)
- Create, update, delete personal todos
- Status tracking (Pending / Complete)
- Secure user-based access control

## Tech Stack
- Python
- Django 5.2
- SQLite (dev)

## Project Structure
- config/ → project settings
- todo/ → todo app
- user/ → authentication logic
- templates/ → HTML templates

## Setup Instructions
1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Run migrations
5. Start server

## Security
- CSRF protection
- User ownership enforcement
- Login required for all actions

## Future Improvements
- REST API
- Pagination
- Search & filters
- Docker deployment


## API Documentation

Swagger UI:
http://localhost:8000/api/docs/

Authentication:
POST /api/v1/login/
POST /api/v1/logout/

Todos:
GET    /api/v1/todos/
POST   /api/v1/todos/
GET    /api/v1/todos/{id}/
DELETE /api/v1/todos/{id}/
