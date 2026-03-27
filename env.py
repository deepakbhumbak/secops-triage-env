import gymnasium as gym
import random
from schemas import Email, SecOpsObservation, SecOpsAction, SecOpsReward

class SecOpsTriageEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.state_data = None
        self.max_steps = 10  # Prevents infinite loops (as requested in rubric)
        self.current_step = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        
        # Generate a mock inbox with 1 malicious and 2 safe emails
        mock_inbox = [
            Email(
                email_id="email_01",
                sender="hr@company.com",
                subject="Updated Holiday Policy",
                body="Please review the new policy attached.",
                has_attachment=True,
                suspicious_links=0
            ),
            Email(
                email_id="email_02",
                sender="admin@paypa1-support.com", # The Phishing Attempt (Notice the '1' instead of 'l')
                subject="URGENT: Account Locked",
                body="Click here to verify your identity.",
                has_attachment=False,
                suspicious_links=1
            ),
            Email(
                email_id="email_03",
                sender="boss@company.com",
                subject="Project Deadline",
                body="Are we on track for Friday?",
                has_attachment=False,
                suspicious_links=0
            )
        ]
        
        self.state_data = SecOpsObservation(
            inbox=mock_inbox,
            action_history=[]
        )
        
        return self.state_data.model_dump(), {}

    def state(self):
        # Required by OpenEnv: returns the current state at any time
        return self.state_data.model_dump()

    def step(self, action_dict: dict):
        # 1. Validate the AI's action using our Pydantic schema
        try:
            action = SecOpsAction(**action_dict)
        except Exception as e:
            # Penalize invalid actions format
            return self.state_data.model_dump(), -1.0, False, False, {"error": "Invalid action format"}

        self.current_step += 1
        reward = 0.0
        reason = ""
        done = False

        # 2. Find the email the AI is trying to interact with
        target_email = next((e for e in self.state_data.inbox if e.email_id == action.target_email_id), None)

        if not target_email:
            reward = -0.5
            reason = "Invalid email ID targeted."
        else:
            # 3. PARTIAL REWARD LOGIC (High Scoring Rubric Item)
            if action.action_type == "INSPECT_LINK":
                if target_email.suspicious_links > 0:
                    reward = 0.2
                    reason = "Good practice: Inspected a suspicious link."
                else:
                    reward = 0.0
                    reason = "Inspected link, but none were suspicious."
                    
            elif action.action_type == "QUARANTINE":
                if target_email.sender == "admin@paypa1-support.com":
                    reward = 1.0 # Max reward
                    reason = "Success! Quarantined the phishing threat."
                    done = True # Task complete
                else:
                    reward = -1.0 # Fatal penalty 
                    reason = "Failed: Quarantined a legitimate business email."
                    done = True
                    
            elif action.action_type == "ALLOW":
                if target_email.sender == "admin@paypa1-support.com":
                    reward = -1.0 # Fatal penalty
                    reason = "Failed: Allowed a phishing email into the secure network."
                    done = True
                else:
                    reward = 0.5
                    reason = "Correctly allowed a safe email."
                    self.state_data.inbox.remove(target_email) # Clear from inbox

        # Log the action
        log_entry = f"{action.action_type} on {action.target_email_id}: Reward {reward}"
        self.state_data.action_history.append(log_entry)

        # Check for infinite loops
        truncated = self.current_step >= self.max_steps
        if truncated:
            reward -= 0.5
            reason += " | Penalty: Reached max steps."

        # Package the reward info
        info = SecOpsReward(score=reward, reason=reason).model_dump()

        return self.state_data.model_dump(), reward, done, truncated, info