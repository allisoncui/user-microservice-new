from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router as user_router

app = FastAPI()

# Set up CORS (optional, modify origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the user router
app.include_router(user_router.router)

@app.get("/")
async def root():
    return {"message": "User Microservice is running"}

# Start the FastAPI server if run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
