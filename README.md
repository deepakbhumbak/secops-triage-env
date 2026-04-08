# 🛡️ SecOps Triage Env

> An enterprise-grade AI environment for automated security operations triage and incident response.

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![Dependency Manager](https://img.shields.io/badge/managed_by-uv-orange.svg)
![Framework](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)

## 📖 Overview
SecOps Triage Env is a Gymnasium-compatible simulation built for the OpenEnv platform that trains and evaluates AI agents in enterprise security operations. The environment challenges LLM-powered agents to ingest incoming email observations, analyze threat levels, and execute precise actions—such as inspecting links, quarantining malicious payloads, or escalating to human analysts—while earning rewards based on their mitigation accuracy.

## ✨ Key Features
* **Gymnasium Environment (`env.py`):** A custom state-action-reward loop where agents process security observations and receive dynamic scoring based on their triage decisions.
* **Multiplayer Server (`server/app.py`):** A fully dockerized FastAPI backend that allows external autograders and remote agents to interact with the environment via `/reset` and `/step` endpoints.
* **AI-Powered Inference (`inference.py`):** A pre-configured evaluation script that connects an OpenAI-compatible LLM to the environment, generating strictly formatted `START/STEP/END` logs for hackathon grading.
* **Structured Schemas (`schemas.py`):** Ensures all incoming alerts, actions, and observations conform to strict, enterprise-ready data formats.

## 🚀 Quick Start

### Prerequisites
* Python 3.10+
* [uv](https://docs.astral.sh/uv/) (Fast Python package installer and resolver)

### Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/your-username/secops-triage-env.git](https://github.com/your-username/secops-triage-env.git)
   cd secops-triage-env