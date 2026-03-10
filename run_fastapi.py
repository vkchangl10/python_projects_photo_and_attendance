"""
Run FastAPI application.

Usage:
    python -m uvicorn idmitra_django.fastapi_app.main:app --reload
    
Or use this script:
    python run_fastapi.py
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "idmitra_django.fastapi_app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
