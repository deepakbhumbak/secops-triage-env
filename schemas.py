from pydantic import BaseModel, Field
from typing import List, Literal

# ==========================================
# 1. THE OBSERVATION SPACE (What the AI sees)
# ==========================================
class Email(BaseModel):
    email_id: str = Field(description="Unique ID of the email (e.g., 'email_01')")
    sender: str = Field(description="The email address of the person sending it")
    subject: str = Field(description="The subject line of the email")
    body: str = Field(description="The main text content")
    has_attachment: bool = Field(default=False, description="True if a PDF/ZIP is attached")
    suspicious_links: int = Field(default=0, description="Count of URLs in the email body")

class SecOpsObservation(BaseModel):
    inbox: List[Email] = Field(description="The list of emails waiting to be triaged")
    action_history: List[str] = Field(default_factory=list, description="Log of what the AI has done so far")

# ==========================================
# 2. THE ACTION SPACE (What the AI can do)
# ==========================================
class SecOpsAction(BaseModel):
    action_type: Literal["ALLOW", "QUARANTINE", "INSPECT_LINK", "RUN_SANDBOX"] = Field(
        description="The specific security action to execute"
    )
    target_email_id: str = Field(
        description="The ID of the email this action applies to"
    )

# ==========================================
# 3. THE REWARD SPACE (How the AI is graded)
# ==========================================
class SecOpsReward(BaseModel):
    score: float = Field(description="The numeric reward (e.g., +0.5 for partial progress, -1.0 for failure)")
    reason: str = Field(description="Why the score was given (e.g., 'Safely allowed internal email')")