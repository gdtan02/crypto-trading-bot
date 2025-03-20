import os
import signal
import uvicorn
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cross-Origin Resource Sharing (CORS) prohibits unauthorized websites, endpoints, or servers from accessing the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"Hello": "World"}

# Call this endpoint if the server cannot shut down gracefully
@app.get("/shutdown")
async def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content="Shutting down the server...")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
