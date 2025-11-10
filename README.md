# Vehicle Parking App

A full-stack vehicle parking management system with Vue.js frontend and Flask backend.

## Project Structure

```
VPApp-main/
├── backend/          # Flask backend application
│   ├── controllers/  # Route handlers
│   ├── templates/    # HTML templates (legacy)
│   ├── models.py     # Database models
│   ├── app.py        # Flask application entry point
│   └── requirements.txt
│
└── frontend/         # Vue.js frontend application
    ├── src/
    │   ├── components/  # Vue components
    │   ├── views/       # Page views
    │   ├── stores/      # Pinia stores
    │   ├── services/    # API services
    │   └── router/      # Vue Router configuration
    └── package.json
```

## Features

- **User Management**: Registration, login with token-based authentication
- **Role-Based Access**: Admin and User roles
- **Parking Lot Management**: Create, edit, delete parking lots (Admin)
- **Spot Booking**: Book and release parking spots (Users)
- **Reservation History**: View booking history and statistics
- **Dashboard**: Analytics and reports for both admin and users

## Tech Stack

### Backend
- Flask (Python web framework)
- SQLAlchemy (ORM)
- Flask-Login (Session management)
- SQLite (Database)

### Frontend
- Vue.js 3 (JavaScript framework)
- TypeScript
- Pinia (State management)
- Vue Router (Routing)
- Axios (HTTP client)
- Bootstrap (UI framework)

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## Default Credentials

- **Admin**: username: `admin`, password: `admin123`
- **Users**: Register new accounts through the registration page

## API Endpoints

### Authentication
- `POST /login` - Login (returns token and role)
- `POST /register` - Register new user
- `GET /logout` - Logout

### Parking Lots
- `GET /api/lots` - List all parking lots
- `GET /api/lots/<id>` - Get lot details
- `POST /admin/lots/create` - Create lot (Admin only)
- `POST /admin/lots/edit/<id>` - Update lot (Admin only)
- `POST /admin/lots/delete/<id>` - Delete lot (Admin only)

### Reservations
- `GET /api/user/<user_id>/reservations` - Get user reservations
- `POST /user/book/<lot_id>` - Book a spot
- `POST /user/release/<reservation_id>` - Release a spot

## Development

### Backend Development
- Backend uses Flask with SQLAlchemy ORM
- Database file: `backend/parking_app.db` (SQLite)
- Token-based authentication for API requests
- Session-based authentication for legacy HTML templates

### Frontend Development
- Vue 3 with Composition API
- TypeScript for type safety
- Pinia for state management
- Axios interceptors for automatic token injection

## License

This project is open source and available for use.

