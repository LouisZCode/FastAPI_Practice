from fastapi import HTTPException, Security, FastAPI, Depends
from fastapi.security import APIKeyHeader

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key")

VALID_API_KEYS = {
    "flashcard-key-123": "developer_1",
    "flashcard-key-456": "developer_2",
}

usage_counts = {}
DAILY_LIMIT = 2

# Step 1: Validate the API key
def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(401, "Invalid or missing API Key")
    return api_key 


# Step 2: Check rate limit (depends on step 1!)
def check_rate_limit(api_key: str = Depends(validate_api_key)):
    current_count = usage_counts.get(api_key, 0)
    
    if current_count >= DAILY_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {current_count}/{DAILY_LIMIT}"
        )
    
    usage_counts[api_key] = current_count + 1
    
    return api_key  # Pass it forward

# Step 3: Use in endpoint (only ONE Depends needed!)
@app.get("/topics/")
async def list_topics(api_key: str = Depends(check_rate_limit)):
    return {"message": "success", "api_key": api_key}