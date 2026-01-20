# 🏥 Hospital Token Management System

A **junior → mid-level industry-style project** built using **FastAPI + React** to manage walk-in (talk-in) patients in a hospital.

This system allows staff to generate tokens for patients, doctors to manage token flow, and the public to see live token updates.

---

## 🚀 Project Purpose (Simple)

In many hospitals:

- Patients come without appointment
- Staff gives them a token
- Doctor calls patients one by one
- Everyone wants **live updates**

This project solves that problem using:

- REST APIs
- JWT authentication
- Role-based access control (RBAC)
- WebSockets for live updates
- Redis for performance

---

## 🧑‍⚕️ User Roles

| Role   | What they can do                          |
| ------ | ----------------------------------------- |
| Admin  | Create users, manage doctors/staff/nurses |
| Staff  | Register patients, generate tokens        |
| Doctor | View own tokens, update token status      |
| Public | View today’s active tokens (no login)     |

---

## 🛠 Tech Stack

### Backend

- **FastAPI** (v0.104.x)
- **PostgreSQL** (Database)
- **SQLAlchemy ORM**
- **JWT Authentication** (access + refresh)
- **Redis** (cache + token queue)
- **WebSocket** (real-time updates)

### Frontend

- **React (Vite)**
- **Axios** (API calls)
- **Context API** (Auth state)
- **Role-based routing**
- **Native WebSocket** (browser WebSocket API)

---

## 📂 Backend Folder Structure (Overview)

```
app/
├── main.py                 # App entry point
├── api/v1/
│   ├── routes/             # HTTP & WebSocket routes
│   ├── controllers/        # Business logic (patient tokens)
│   └── schemas/            # Pydantic request/response models
├── core/                   # Auth, RBAC, Redis, WebSocket manager
├── db/                     # DB session & base
├── models/                 # SQLAlchemy models
├── utils/                  # Helper utilities
└── middlewares/            # (Optional)
```

---

## 📂 Frontend Folder Structure (Overview)

```
frontend/
└── src/
    ├── api/                # Axios & API services
    ├── auth/               # Login pages
    ├── context/            # Auth context
    ├── pages/              # Dashboards
    ├── router/             # Protected routes
    ├── utils/              # Helpers
    ├── App.jsx
    └── main.jsx
```

---

## 🔐 Authentication Flow

1. User logs in
2. Backend returns:

   - Access Token
   - Refresh Token

3. Frontend stores tokens
4. Access token sent in headers
5. Backend validates user & role

---

## 🔑 Role-Based Access Control (RBAC)

Implemented using:

- JWT token
- Role checking (`require_roles`)

Example:

- Staff cannot access doctor routes
- Doctor cannot access admin routes

---

## 🎫 Token Management Flow

1. Staff registers patient
2. Staff generates token for doctor
3. Token saved in database
4. Token pushed to Redis queue
5. WebSocket broadcasts event
6. Frontend updates UI live

Token statuses:

- `waiting`
- `in_progress`
- `completed`

---

## 🔄 Real-Time Updates (WebSocket)

- Backend keeps active WebSocket connections
- Events broadcasted:

  - TOKEN_CREATED
  - TOKEN_STATUS_UPDATED

- Frontend listens and updates UI instantly

---

## ⚡ Redis Usage

Redis is used for:

- Token queues per doctor
- Caching doctors list
- Fast temporary storage

This improves performance and scalability.

---

## 🎯 Project Level

✅ Junior → Mid-level industry project

✔ Real-world problem
✔ Clean backend structure
✔ Secure authentication
✔ Live updates

---

## 🧩 Future Improvements (Planned)

- Better logging (instead of print)
- API documentation
- Testing
- LLM + RAG integration (future)

---

## ▶️ How to Run (Basic)

### Backend

1. Create virtual environment
2. Install dependencies
3. Set environment variables
4. Run:

```
uvicorn app.main:app --reload
```

### Frontend

1. Install dependencies
2. Run:

```
npm run dev
```

---

## 📌 Important Note

This README explains the project **as it exists now**.
No files were removed or changed.

Next step: **File-by-file analysis without breaking anything**.
