import redis
from app.core.config import settings

# Create Redis connection
redis_client = redis.Redis(
    host='localhost',   
    port=6379,           
    db=0,            
    decode_responses=True 
    
)

def test_redis_connection():
  try:
    redis_client.ping()
    print("Redis connection successful!")
    return True
  except redis.ConnectionError:
    print("Redis connection failed!")
    return False

