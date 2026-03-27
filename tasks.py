# tasks.py

def grade_easy_task(final_state: dict) -> float:
    """
    EASY TASK: Did the AI successfully catch the obvious phishing email?
    Checks if 'email_02' was quarantined.
    """
    action_history = final_state.get("action_history", [])
    
    # Check if the AI successfully quarantined the bad email
    quarantined_phish = any("QUARANTINE" in log and "email_02" in log for log in action_history)
    
    # Check if it made a fatal error (deleting the boss's safe email)
    deleted_boss = any("QUARANTINE" in log and "email_03" in log for log in action_history)
    
    score = 0.0
    if quarantined_phish:
        score += 1.0
    if deleted_boss:
        score -= 1.0 # Heavy penalty
        
    return max(0.0, min(1.0, score)) # Forces score to stay between 0.0 and 1.0

def grade_medium_task(final_state: dict) -> float:
    """
    MEDIUM TASK: Did the AI follow proper investigation protocols?
    It must INSPECT the link before QUARANTINING.
    """
    action_history = final_state.get("action_history", [])
    
    inspected_first = any("INSPECT_LINK" in log and "email_02" in log for log in action_history)
    quarantined = any("QUARANTINE" in log and "email_02" in log for log in action_history)
    
    score = 0.0
    if inspected_first:
        score += 0.5  # Partial credit for good investigation
    if quarantined:
        score += 0.5  # Partial credit for taking action
        
    return max(0.0, min(1.0, score))

def grade_hard_task(final_state: dict) -> float:
    """
    HARD TASK: Perfect Inbox Triage. 
    AI must allow all safe emails and quarantine all threats efficiently.
    """
    action_history = final_state.get("action_history", [])
    
    allowed_hr = any("ALLOW" in log and "email_01" in log for log in action_history)
    quarantined_phish = any("QUARANTINE" in log and "email_02" in log for log in action_history)
    allowed_boss = any("ALLOW" in log and "email_03" in log for log in action_history)
    
    score = 0.0
    if quarantined_phish: score += 0.4
    if allowed_hr: score += 0.3
    if allowed_boss: score += 0.3
    
    # Penalize if the AI was guessing wildly (took too many steps)
    if len(action_history) > 4:
        score -= 0.2
        
    return max(0.0, min(1.0, score))

# Quick test to make sure it runs without errors
if __name__ == "__main__":
    dummy_state = {"action_history": ["INSPECT_LINK on email_02: Reward 0.2", "QUARANTINE on email_02: Reward 1.0"]}
    print(f"Easy Score: {grade_easy_task(dummy_state)}")
    print(f"Medium Score: {grade_medium_task(dummy_state)}")