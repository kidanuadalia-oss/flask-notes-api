# Flask Notes API

A REST API for managing notes built with Flask and MongoDB. Supports full CRUD operations, search functionality, metrics tracking, and request logging. Fully containerized with Docker for easy deployment.

## About This Project

I built this Flask API for managing notes. The idea was to create something simple that lets you store and retrieve notes through a REST API. I used Flask for the backend and MongoDB to store the data.

**What it does:**
- Create, read, update, and delete notes
- Search through notes by title or body
- Track metrics like request counts and uptime
- Log all requests for debugging
- Run everything with Docker Compose
- Has tests to make sure everything works

## Course Concepts Used

This project uses stuff we learned in class:

1. **Flask API** - Made REST endpoints with Flask Blueprints, handled requests and errors
2. **MongoDB** - Connected to MongoDB using pymongo, set up the database schema and added indexes
3. **Logging & Metrics** - Added logging for requests and made a metrics endpoint
4. **Docker** - Put everything in Docker containers so it's easy to run

### How It Works

![Architecture Diagram](assets/architecture.svg)

Pretty straightforward - clients send HTTP requests to the Flask app, which talks to MongoDB to save/retrieve data. I log all requests so I can see what's happening.

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌──────────────────────────────────┐
│      Flask Application           │
│  ┌────────────────────────────┐  │
│  │  Routes (Blueprints)       │  │
│  │  - /notes (CRUD)          │  │
│  │  - /notes/search          │  │
│  │  - /metrics               │  │
│  └────────────────────────────┘  │
│  ┌────────────────────────────┐  │
│  │  Metrics & Logging         │  │
│  └────────────────────────────┘  │
└──────────────┬───────────────────┘
               │
               │ pymongo
               ▼
┌──────────────────┐
│    MongoDB       │
│  (Docker/Atlas)  │
└──────────────────┘
```

### Data Storage

- Using MongoDB to store notes as JSON documents
- Each note has: `_id`, `title`, `body`, and `created_at`
- Notes are created through the API
- Can deploy to MongoDB Atlas and Render.com for cloud hosting

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes` | Create a new note |
| GET | `/notes` | List all notes |
| GET | `/notes/<id>` | Get a specific note by ID |
| GET | `/notes/search?q=keyword` | Search notes by title or body |
| DELETE | `/notes/<id>` | Delete a note |
| GET | `/metrics` | Get application metrics |
| GET | `/health` | Health check endpoint |

### Note Schema

```json
{
  "_id": "string (ObjectId)",
  "title": "string (required)",
  "body": "string",
  "created_at": "datetime (ISO format)"
}
```

## How to Run

### Docker (Recommended)

To build and run the entire application:

```bash
docker compose up --build
```

This command will start both MongoDB and the Flask application. The API will be available at `http://localhost:8080`.

Verify it's running:

```bash
curl http://localhost:8080/health
```

Example API calls:

```bash
# Create a note
curl -X POST http://localhost:8080/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Note", "body": "This is a test"}'

# List all notes
curl http://localhost:8080/notes

# Get metrics
curl http://localhost:8080/metrics
```

### Manual Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd flask-notes-api
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI
   ```

5. **Start MongoDB** (if not using Docker):
   ```bash
   docker run -d -p 27017:27017 --name mongo mongo:7.0
   ```

6. **Run the application:**
   ```bash
   python -m src.app
   ```

### Running Tests

```bash
# Install dependencies first
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

## Why I Chose These Technologies

I went with Flask because it's simple and easy to use. MongoDB seemed like a good fit since notes are just documents - no need to deal with SQL tables and migrations. Docker makes it easy to run everything the same way on different machines.

I thought about using FastAPI or PostgreSQL, but Flask and MongoDB were simpler for this project. Docker Compose is enough - no need for Kubernetes or anything fancy.

## Performance & Limitations

The API responds pretty fast (under 50ms usually). I added indexes to MongoDB to make searches quick. It can handle a decent amount of traffic, but if you had thousands of users you'd probably want to add caching with Redis or something.

For this class project, the free tiers of MongoDB Atlas and Render.com work fine. The code is organized with Flask Blueprints so it's easy to understand.

## Security Notes

Right now I'm using environment variables for the MongoDB connection string. I validate inputs and handle errors. There's no authentication yet - anyone can access any note. For a real production app you'd want to add user authentication, rate limiting, and HTTPS.

## Testing

I wrote tests for all the endpoints:
- Creating notes (including validation)
- Getting notes
- Searching notes
- Deleting notes
- Error cases (invalid IDs, missing data)
- Health check and metrics endpoints

Everything passes! ✅

## Deployment

### Render.com Deployment

1. **Set up MongoDB Atlas:**
   - Create account at mongodb.com/cloud/atlas
   - Create a free cluster
   - Create a database user
   - Whitelist IP addresses (0.0.0.0/0 for Render, or specific IPs)
   - Get connection string: `mongodb+srv://user:pass@cluster.mongodb.net/notes`

2. **Create Render service:**
   - Sign up at render.com with GitHub
   - Click "New +" → "Web Service"
   - Connect your repository
   - Select branch: `main`

3. **Configure service:**
   - Name: `flask-notes-api` (or your preference)
   - Environment: `Docker`
   - Region: Choose closest to your location
   - Branch: `main`

4. **Set environment variables:**
   ```
   FLASK_ENV=production
   MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/notes?retryWrites=true&w=majority
   PORT=8080
   ```

5. **Configure health check:**
   - Health check path: `/health`

6. **Deploy:**
   - Click "Create Web Service"
   - First deployment takes 5-10 minutes
   - You'll receive a URL like: `https://flask-notes-api.onrender.com`

7. **Verify deployment:**
   ```bash
   curl https://your-app.onrender.com/health
   ```

**Troubleshooting:**
- Build failures: Check Dockerfile syntax and ensure all dependencies are in requirements.txt
- Connection errors: Verify MONGO_URI is correct and check IP whitelist settings
- Application crashes: Check Render logs and verify environment variables
- Slow first request: Render free tier spins down after 15 minutes of inactivity (cold start takes ~30 seconds)

### Environment Variables

```bash
FLASK_ENV=production
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/notes?retryWrites=true&w=majority
PORT=8080
```

## Future Improvements

If I had more time, I'd add:
- User authentication (JWT tokens)
- Better search (full-text search)
- Rate limiting to prevent abuse
- Caching with Redis
- API documentation with Swagger
- Better monitoring tools

## API Examples

### Create a Note

```bash
curl -X POST http://localhost:8080/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Note",
    "body": "This is the note content"
  }'
```

### List All Notes

```bash
curl http://localhost:8080/notes
```

### Search Notes

```bash
curl http://localhost:8080/notes/search?q=python
```

### Get Metrics

```bash
curl http://localhost:8080/metrics
```

Response:
```json
{
  "uptime_seconds": 3600,
  "uptime_formatted": "1h 0m 0s",
  "total_requests": 150,
  "total_notes_in_db": 25,
  "total_notes_created": 30
}
```

## CI/CD

I set up GitHub Actions to run tests automatically when I push code. It spins up MongoDB, runs all the tests, and makes sure everything compiles. Pretty useful for catching bugs before they get merged.

## Links

- **GitHub Repository:** https://github.com/kidanuadalia-oss/flask-notes-api
- **Render Deployment:** https://flask-notes-api-1.onrender.com

---

Built with Flask and MongoDB
