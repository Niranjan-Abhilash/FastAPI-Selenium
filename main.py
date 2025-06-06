from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from extract import *
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "https://testing0.pages.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],     # or limit to ["GET", "POST"]
    allow_headers=["*"],
)


SECRET = os.getenv("SECRET")

#

class Msg(BaseModel):
    msg: str
    secret: str

@app.get("/")

async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/homepage")
async def demo_get():
    driver=createDriver()

    homepage = getGoogleHomepage(driver)
    driver.close()
    return homepage

@app.post("/backgroundDemo")
async def demo_post(inp: Msg, background_tasks: BackgroundTasks):
    
    background_tasks.add_task(doBackgroundTask, inp)
    return {"message": "Success, background task started"}
    
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # fallback for local dev
    uvicorn.run("main:app", host="0.0.0.0", port=port)

