import random
from typing import Tuple, Dict, Any


class SecOpsTriageEnv:
    def __init__(self):
        self._state = {}
        self._step_count = 0

    # Reset environment
    def reset(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        self._step_count = 0

        self._state = {
            "alert_id": random.randint(1000, 9999),
            "severity": random.choice(["low", "medium", "high"]),
            "status": "new",
            "description": "Suspicious login attempt detected",
        }

        return self._state, {}

    # Take action on alert
    def step(self, action: Dict[str, Any]):
        self._step_count += 1

        action_type = action.get("action", "ignore")

        reward = 0.0
        done = False
        truncated = False

        # Simple logic for demo
        if action_type == "investigate":
            self._state["status"] = "under_investigation"
            reward = 1.0

        elif action_type == "escalate":
            self._state["status"] = "escalated"
            reward = 2.0
            done = True

        elif action_type == "close":
            self._state["status"] = "closed"
            reward = 1.5
            done = True

        else:
            self._state["status"] = "ignored"
            reward = -0.5

        info = {
            "step": self._step_count,
            "action_taken": action_type
        }

        return self._state, reward, done, truncated, info

    # Return current state
    def state(self) -> Dict[str, Any]:
        return self._state