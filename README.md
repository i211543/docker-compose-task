# Multi-Container Flask-Redis App with Docker

This project demonstrates how to set up and run two Docker containers: one for a Flask web application and another for a Redis database. The containers communicate using Docker networks.

## Features
- Flask web app with a visit counter
- Redis integration for persistent storage
- REST API endpoints
- Dockerized setup (no Docker Compose)

## Project Structure
```
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration for Flask app
├── README.md              # This file
├── .gitignore             # Git ignore file
└── tasks.md               # Assignment instructions
```

## Prerequisites
- Docker installed
- (Optional) Git for code management

## Setup & Usage

### 1. Create Docker Network
```
docker network create flask-redis-network
```

### 2. Start Redis Container
```
docker run -d --name redis-container --network flask-redis-network redis:alpine
```

### 3. Build Flask App Image
```
docker build -t flask-app .
```

### 4. Run Flask App Container (on port 5001)
```
docker run -d -p 5001:5000 --name flask-container --network flask-redis-network flask-app
```

### 5. Access the App
- Main page: http://localhost:5001
- API: http://localhost:5001/api/visits
- Reset counter: POST to http://localhost:5001/api/reset

## API Endpoints
- `GET /` — Main page with visit counter
- `GET /api/visits` — Returns current visit count
- `POST /api/reset` — Resets visit counter (must use POST method)

### Testing the API
You can test the API using:
1. **Browser:**
   - Visit http://localhost:5001 for the main page
   - Visit http://localhost:5001/api/visits to see the current count

2. **Reset Counter:**
   - Use curl: `curl -X POST http://localhost:5001/api/reset`
   - Or use the provided test.html file and click the "Reset Counter" button

Note: The reset endpoint only accepts POST requests, not GET requests. You cannot reset the counter by simply visiting the URL in your browser.

## Stopping & Cleaning Up

### Quick Stop (Containers Only)
```bash
docker stop flask-container redis-container
```

### Full Cleanup (Containers and Network)
```bash
# Stop containers
docker stop flask-container redis-container

# Remove containers
docker rm flask-container redis-container

# Remove network
docker network rm flask-redis-network
```

### Verify Cleanup
```bash
# Check running containers
docker ps

# Check all containers (including stopped ones)
docker ps -a

# Check networks
docker network ls
```

## Starting the App Next Time
1. **Start the Docker network (if not already created):**
   ```
   docker network create flask-redis-network
   ```
2. **Start Redis container:**
   ```
   docker run -d --name redis-container --network flask-redis-network redis:alpine
   ```
3. **Start Flask container (using your Docker Hub image):**
   ```
   docker run -d -p 5001:5000 --name flask-container --network flask-redis-network amsepi42/flask-app
   ```

## Logs & Troubleshooting
- View logs: `docker logs flask-container` or `docker logs redis-container`
- Ensure both containers are on the same network
- If port 5001 is in use, pick another port (e.g., `-p 5002:5000`)

## License
Educational use only. 