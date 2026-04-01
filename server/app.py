from fastapi import FastAPI, Request
import uvicorn
from env import SecOpsTriageEnv

app = FastAPI()
env = SecOpsTriageEnv()

@app.post("/reset")
async def reset():
    obs, _ = env.reset()
    return obs  # OpenEnv expects just the observation back

@app.post("/step")
async def step(request: Request):
    # The grader sends the AI's action as a JSON payload
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

# Health check so Hugging Face knows the server is alive
@app.get("/")
async def root():
    return {"status": "Running", "environment": "SecOps Triage"}