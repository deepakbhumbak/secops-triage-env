from fastapi import FastAPI, Request
import uvicorn
from server.env import SecOpsTriageEnv

app = FastAPI()
env = SecOpsTriageEnv()

@app.get("/")
async def root():
    return {"status": "Running"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()