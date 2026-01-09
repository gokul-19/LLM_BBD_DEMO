# LLM-Assisted BDD Functional Testing

## 📌 Overview
This project presents an **LLM-assisted Functional Testing framework** that transforms plain English business requirements into BDD-style Gherkin scenarios and executes happy-path test cases in a controlled and automated manner.

The solution incorporates scenario validation and a manual approval mechanism, making it suitable for enterprise-level testing workflows.

---

## 🎯 Objectives
- Automatically generate BDD scenarios using an LLM
- Produce both positive and negative scenarios
- Validate generated scenarios before execution
- Execute only approved happy-path scenarios
- Introduce a manual approval gate for execution control

---

## 🧠 System Architecture

### Architecture Flow Diagram

```
Business Requirement
        |
        v
LLM Scenario Generator
        |
        v
Gherkin BDD Scenarios
        |
        v
Scenario Validation
        |
        v
Manual Approval Gate
        |
        v
BDD Test Execution (Behave)
```

---

## 🛠️ Tech Stack
- Python
- Behave (BDD Framework)
- Gherkin
- Simulated LLM Logic

---

## ▶️ How to Run
```bash
pip install -r requirements.txt
python run_pipeline.py
behave
```

---

## 👤 Author
Gokul G  
Final Year – Data Science & Artificial Intelligence
