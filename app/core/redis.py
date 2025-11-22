import redis
from app.core.config import settings

# Create Redis connection
redis_client = redis.Redis(
    host='localhost',    # Redis server address
    port=6379,           # Default Redis port
    db=0,                # Database number
    decode_responses=True # Convert responses from bytes to strings
)

def test_redis_connection():
  try:
    redis_client.ping()
    print("Redis connection successful!")
    return True
  except redis.ConnectionError:
    print("Redis connection failed!")
    return False

