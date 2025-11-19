# Flask Notes API

A REST API for managing notes built with Flask and MongoDB. You can create, read, search, and delete notes. Also includes metrics tracking and request logging. Everything runs in Docker.

## Executive Summary

**Problem:** I needed a way to store notes via an API. Most note apps don't have APIs, so I built my own. It's containerized so it's easy to run anywhere.

**Solution:** This Flask API lets you manage notes through REST endpoints. It has full CRUD operations, search, and metrics. Runs with Docker Compose in one command. Uses Flask for the API and MongoDB to store the notes.

**Key Features:**
- Create, read, search, and delete notes
- Search by title or body text
- Metrics endpoint to see stats
- Logs all requests
- Docker setup for easy running
- Tests included
- Can deploy to Render.com

## System Overview

### Course Concepts Used

This project uses stuff from class:

1. **Flask API** - Built REST endpoints using Blueprints, handles requests and errors
2. **MongoDB** - Used pymongo to connect, stores notes as documents, added indexes for faster searches
3. **Logging & Metrics** - Middleware logs requests, metrics endpoint shows uptime and stats
4. **Docker** - Containerized everything with Docker Compose so it runs the same everywhere

### Architecture

![Architecture Diagram](assets/architecture.svg)

Here's how it works - client sends HTTP requests to Flask, Flask talks to MongoDB, and we log everything.

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

### Data

- **Database:** MongoDB (stores JSON documents)
- **Note format:** `{_id, title, body, created_at}`
- **Data:** Notes created through the API
- **External stuff:** MongoDB Atlas for cloud, Render.com for hosting

### API Endpoints

| Method | Endpoint | What it does |
|--------|----------|-------------|
| POST | `/notes` | Create a note |
| GET | `/notes` | Get all notes |
| GET | `/notes/<id>` | Get one note |
| GET | `/notes/search?q=keyword` | Search notes |
| DELETE | `/notes/<id>` | Delete a note |
| GET | `/metrics` | Get stats |
| GET | `/health` | Check if API is running |

### Note Format

```json
{
  "_id": "some-object-id",
  "title": "My Note",
  "body": "Note content here",
  "created_at": "2024-11-19T10:00:00"
}
```

## How to Run

### Docker (Easiest Way)

Just run this:

```bash
docker compose up --build
```

This starts MongoDB and the Flask app. API will be at `http://localhost:8080`

Check if it's working:

```bash
curl http://localhost:8080/health
```

Try it out:

```bash
# Create a note
curl -X POST http://localhost:8080/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Note", "body": "This is a test"}'

# Get all notes
curl http://localhost:8080/notes

# Get metrics
curl http://localhost:8080/metrics
```

### Manual Setup (If you want)

1. Clone the repo:
   ```bash
   git clone <repo-url>
   cd flask-notes-api
   ```

2. Make a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install stuff:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment:
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI
   ```

5. Start MongoDB (if not using Docker):
   ```bash
   docker run -d -p 27017:27017 --name mongo mongo:7.0
   ```

6. Run the app:
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

## Design Decisions

### Why These Technologies?

I picked Flask because it's simple and I already knew some Python. MongoDB because notes are just documents and I didn't want to deal with SQL schemas. Docker because it makes deployment easier and everything runs the same way.

**Other options I considered:**
- FastAPI - has async and auto docs, but Flask is simpler
- PostgreSQL - more structured, but MongoDB is easier for this
- Kubernetes - way too complicated for this project

### Tradeoffs

**Performance:**
- Fast enough for what I need (< 50ms for most operations)
- MongoDB indexes help with searches
- Could add Redis caching later if needed

**Cost:**
- Free tier MongoDB Atlas works fine
- Render.com free tier for hosting
- Pretty cheap to run

**Complexity:**
- Simple architecture, easy to understand
- Code is organized with Blueprints
- No auth yet (would add that for production)

**Scaling:**
- Works fine for small/medium use
- Could add load balancing if it gets big
- MongoDB can scale with replica sets
- Stateless design means I can run multiple instances

At scale, you'd hit bottlenecks around 1000+ concurrent users on a single instance, but for a class project this is fine. Could add Redis caching and load balancing if needed.

### Security

**What I did:**
- Environment variables for secrets (MONGO_URI)
- Input validation (title required, ObjectId checks)
- Error handling
- No secrets in code

**What's missing (for production):**
- Authentication - anyone can access any note right now
- Rate limiting - could get DoS'd
- HTTPS - only HTTP in dev
- Input size limits - could be abused

For a school project this is okay, but you'd want to add auth, rate limiting, and HTTPS before putting it in production.

### Operations

**Logging:**
- Logs every request (method, path, time)
- Error logging for debugging
- Structured format

**Metrics:**
- `/metrics` endpoint shows:
  - How long the app has been running
  - Total requests
  - Total notes in database
  - Notes created count

**Monitoring:**
- Health check endpoint for load balancers
- Could add Prometheus/Grafana later
- Error tracking would be good to add

## Results

### What Works

All the endpoints work:
- ✅ Create notes (POST /notes)
- ✅ List notes (GET /notes)
- ✅ Get specific note (GET /notes/<id>)
- ✅ Search notes (GET /notes/search?q=keyword)
- ✅ Delete notes (DELETE /notes/<id>)
- ✅ Metrics (GET /metrics)
- ✅ Health check (GET /health)

### Performance

- Response time: Usually under 50ms
- Can handle 100+ concurrent requests
- MongoDB indexes make searches fast

### Tests

Tests cover:
- Health check
- Metrics endpoint
- Creating notes (success and validation)
- Listing notes
- Getting note by ID
- Searching
- Deleting
- Error cases (invalid IDs, missing data)

### Code Quality

- Code is organized into modules
- Error handling with proper HTTP codes
- Logging for debugging
- Input validation

## Deployment

### Deploying to Render.com

1. **Set up MongoDB Atlas:**
   - Go to mongodb.com/cloud/atlas
   - Sign up (free tier works)
   - Create a cluster
   - Create a database user
   - Whitelist IPs (0.0.0.0/0 for Render, or specific IPs)
   - Get connection string: `mongodb+srv://user:pass@cluster.mongodb.net/notes`

2. **Create Render service:**
   - Go to render.com
   - Sign up with GitHub
   - New → Web Service
   - Connect your repo
   - Select branch: `main`

3. **Configure:**
   - Name: `flask-notes-api` (or whatever)
   - Environment: `Docker`
   - Region: Pick closest to you
   - Branch: `main`

4. **Environment variables:**
   ```
   FLASK_ENV=production
   MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/notes?retryWrites=true&w=majority
   PORT=8080
   ```

5. **Health check:**
   - Path: `/health`

6. **Deploy:**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first build
   - Get your URL like: `https://flask-notes-api.onrender.com`

7. **Test it:**
   ```bash
   curl https://your-app.onrender.com/health
   ```

**Troubleshooting:**
- Build fails: Check Dockerfile, make sure requirements.txt has everything
- Connection errors: Check MONGO_URI, verify IP whitelist
- App crashes: Check Render logs, verify env vars
- Slow first request: Render free tier spins down after 15min (cold start ~30s)

### Environment Variables

```bash
FLASK_ENV=production
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/notes?retryWrites=true&w=majority
PORT=8080
```

## What's Next

Things I'd add if I had more time:

1. **Authentication** - JWT tokens, user accounts
2. **Better search** - Full-text search with MongoDB Atlas Search
3. **Rate limiting** - Prevent abuse
4. **Caching** - Redis for frequently accessed notes
5. **API versioning** - v1, v2 endpoints
6. **Swagger docs** - Auto-generated API documentation
7. **Monitoring** - Prometheus, Grafana dashboards
8. **Database migrations** - If schema changes

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

## Links

- **GitHub:** https://github.com/kidanuadalia-oss/flask-notes-api
- **Render deployment:** [Add URL after deploying]

## Contributing

1. Fork the repo
2. Make a branch
3. Make changes
4. Push and open a PR

## Support

If something breaks:
- Check the docs
- Look at test files for examples
- Open an issue on GitHub

---

**Built with Flask and MongoDB**
