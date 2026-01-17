from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

# Define where the key should be in the request
api_key_header = APIKeyHeader(name="X-API-Key")

# Your valid keys (in production: store in database/env variables)
VALID_API_KEYS = {
    "flashcard-key-123": "developer_1",
    "flashcard-key-456": "developer_2",
}

# Function that validates the key
def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key"
        )
    return api_key  # Return key if valid