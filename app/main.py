from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router as user_router
from middleware.middleware import log_request_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.middleware("http")(log_request_response)

@app.get("/")
async def root():
    return {"message": "User Microservice is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
