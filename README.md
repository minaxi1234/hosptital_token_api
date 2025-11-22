# 🏥 Hospital Token Management System

A production-ready FastAPI backend for hospital token management with real-time updates, role-based access control, and performance optimization.

## 🚀 Features

- **🔐 JWT Authentication** with role-based access control (Admin, Doctor, Nurse, Staff)
- **📱 Real-time Updates** via WebSocket for live token notifications
- **⚡ Performance Optimization** with Redis caching
- **🗄️ Database Management** with PostgreSQL and Alembic migrations
- **🛡️ Production Security** with error handling, security headers, and input validation
- **👥 Multi-role System** with granular permissions

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.12+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache & Message Broker**: Redis
- **Authentication**: JWT tokens with Argon2 hashing
- **Real-time**: WebSocket
- **Migrations**: Alembic
- **Containerization**: Docker

## 📁 Project Structure

token-api/
├── app/
│ ├── api/v1/ # API routes and controllers
│ ├── core/ # Core configurations (auth, security, Redis)
│ ├── db/ # Database session and base setup
│ ├── models/ # SQLAlchemy models (User, Doctor, Token, etc.)
│ └── utils/ # Utilities (hashing, helpers)
├── alembic/ # Database migrations
├── scripts/ # Admin creation scripts
└── tests/ # Test suite

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis

### Installation & Setup

1. **Clone and setup environment**:

````bash
git clone <your-repo-url>
cd token-api
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt



2. **Environment configuration**:
```bash
cp .env.example .env
# Edit .env with your database credentials and secrets

### Database Setup:

bash
# Run migrations
alembic upgrade head

# Create admin user
python scripts/createadmin.py

### Start the Application:

bash
# Development
uvicorn app.main:app --reload

# Production (with workers)
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000

Once running, access the interactive documentation:

Swagger UI: http://localhost:8000/docs

👥 Roles & Permissions
Role	Permissions
Admin	Full system access, manage all users
Doctor	View and update own tokens, update profile
Nurse	Update own information
Staff	Register patients, generate tokens

🔧 Key Endpoints
- `POST /auth/login` - User authentication
- `POST /patients/token` - Generate patient tokens

GET /patients/tokens - Doctor's token queue

POST /admin/doctor - Admin: Add doctors

WS /ws/tokens - WebSocket for real-time updates
````

## 🚀 Deployment on Render

1. **Push your code to GitHub**
2. **Go to [Render.com](https://render.com)**
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub repository**
5. **Use these settings:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Add environment variables in Render dashboard:**
   - `DATABASE_URL` - Your PostgreSQL connection string
   - `SECRET_KEY` - Your JWT secret key
   - `REDIS_URL` - Your Redis connection string (optional)

Your API will be live at: `https://your-app-name.onrender.com`
