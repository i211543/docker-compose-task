from flask import Flask, jsonify
import redis
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Redis configuration
redis_host = os.getenv('REDIS_HOST', 'redis-container')
redis_port = int(os.getenv('REDIS_PORT', 6379))

try:
    redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    raise

@app.route('/')
def index():
    try:
        visits = redis_client.incr('visits')
        return f'<h1>Welcome to the Flask-Redis Demo!</h1><p>This page has been visited {visits} times.</p>'
    except redis.RedisError as e:
        logger.error(f"Redis error: {e}")
        return '<h1>Error</h1><p>Unable to connect to Redis</p>', 500

@app.route('/api/visits')
def get_visits():
    try:
        visits = redis_client.get('visits')
        return jsonify({'visits': int(visits) if visits else 0})
    except redis.RedisError as e:
        logger.error(f"Redis error: {e}")
        return jsonify({'error': 'Unable to get visits count'}), 500

@app.route('/api/reset', methods=['POST'])
def reset_visits():
    try:
        redis_client.set('visits', 0)
        return jsonify({'message': 'Visit counter reset successfully'})
    except redis.RedisError as e:
        logger.error(f"Redis error: {e}")
        return jsonify({'error': 'Unable to reset visits count'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 