from fastapi import FastAPI, Request
import uvicorn
from env import SecOpsTriageEnv

app = FastAPI()
env = SecOpsTriageEnv()

@app.post("/reset")
async def reset():
    obs, _ = env.reset()
    return obs

@app.post("/step")
async def step(request: Request):
    action = await request.json()
    obs, reward, done, truncated, info = env.step(action)
    
    return {
        "observation": obs,
        "reward": float(reward),
        "done": bool(done or truncated),
        "info": info
    }

@app.get("/state")
async def state():
    return env.state()

@app.get("/")
async def root():
    return {"status": "Running", "environment": "SecOps Triage"}

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == '__main__':
    main()
