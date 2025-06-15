import uvicorn
from api import app

if __name__ == "__main__":
    """Main entry point for the API server."""
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )