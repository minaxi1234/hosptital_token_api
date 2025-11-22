import json
from typing import Optional, Any
from app.core.redis import redis_client

CACHE_EXPIRE_SECONDS = 15 * 60

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Convert UUID to string
        if hasattr(obj, 'hex'):
            return str(obj)
        # Convert Pydantic models to dict
        if hasattr(obj, 'model_dump'):
            return obj.model_dump()
        elif hasattr(obj, 'dict'):
            return obj.dict()
        return super().default(obj)

def cache_doctors_list(doctors_data: list):
    try:
        # Use custom encoder to handle UUIDs and Pydantic models
        doctors_json = json.dumps(doctors_data, cls=CustomJSONEncoder)
        
        redis_client.setex(
            "doctors_list", 
            CACHE_EXPIRE_SECONDS, 
            doctors_json
        )
        print("✅ Doctors list cached successfully!")
    except Exception as e:
        print(f"❌ Failed to cache doctors: {e}")
        
def get_cached_doctors() -> Optional[list]:
  try:
    cached_data = redis_client.get("doctors_list")
    if cached_data:
      print("Returning doctors from cache!")
      return json.loads(cached_data)
    print("No cached doctors found")
    return None
  except Exception as e:
    print("Error getting cached doctors:{e}")
    return None

def invalidate_doctors_cache():
    
    try:
        redis_client.delete("doctors_list")
        print("✅ Doctors cache invalidated!")
    except Exception as e:
        print(f"❌ Error invalidating cache: {e}")

