# Planventure API

A Flask-based RESTful API for managing travel itineraries and trip planning.

## Features

- User authentication with JWT tokens
- Trip management with CRUD operations
- Automatic itinerary generation
- Location coordinates support
- Secure password handling with bcrypt
- CORS support for frontend integration

## Tech Stack

- Python 3.8+
- Flask
- SQLAlchemy
- JWT Authentication
- SQLite (configurable for other databases)

## Installation

1. Clone the repository
2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:

```env
DATABASE_URL=sqlite:///planventure.db
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

5. Initialize the database:

```bash
python init_db.py
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Trips

- `GET /api/trips` - List all trips
- `POST /api/trips` - Create new trip
- `GET /api/trips/<id>` - Get trip details
- `PUT /api/trips/<id>` - Update trip
- `DELETE /api/trips/<id>` - Delete trip

## Usage Examples

### Register User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secretpass"}'
```

### Create Trip

```bash
curl -X POST http://localhost:5000/api/trips \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris, France",
    "start_date": "2024-06-15T00:00:00Z",
    "end_date": "2024-06-22T00:00:00Z",
    "latitude": 48.8566,
    "longitude": 2.3522
  }'
```

## Development

1. Start the development server:

```bash
flask run
```

2. Run tests:

```bash
pytest
```

## Models

### User

- id: Integer (Primary Key)
- email: String (Unique)
- password_hash: String
- created_at: DateTime
- updated_at: DateTime

### Trip

- id: Integer (Primary Key)
- user_id: Integer (Foreign Key)
- destination: String
- start_date: DateTime
- end_date: DateTime
- latitude: Float
- longitude: Float
- itinerary: JSON
- created_at: DateTime
- updated_at: DateTime

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Email validation
- CORS protection
- Secure password storage

## Error Handling

The API returns standard HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Server Error

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request
