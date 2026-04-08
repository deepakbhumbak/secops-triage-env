# 🛡️ SecOps Triage Environment

## The Problem
Companies spend thousands of hours manually investigating reported phishing emails. If an employee clicks a malicious link, it can compromise the entire network.

## The Solution
This OpenEnv environment simulates a Level 1 Security Analyst's workflow. AI agents are trained to read incoming emails, inspect suspicious URLs, and make strict ALLOW or QUARANTINE decisions without deleting legitimate business communications.

## Features
* **Pydantic Validation:** Strict Action and Observation spaces.
* **Partial Rewards:** Agents are rewarded for following safety protocols (e.g., inspecting links before quarantining) and heavily penalized for destroying safe emails.
* **Deterministic Graders:** Easy, Medium, and Hard task evaluations.

* 
