import uvicorn
import os

if __name__ == "__main__":
    print("Starting test API server...")
    port = int(os.getenv("API_PORT", 8000))
    print(f"Listening on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="debug")