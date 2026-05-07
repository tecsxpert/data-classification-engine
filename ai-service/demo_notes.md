# Tool-134 AI Service — Demo Notes
## AI Developer 1 — Ayush

---

## Demo Script

### Opening (30 seconds)
"I built the AI microservice for Tool-134.
It uses Flask and Groq's LLaMA-3.3-70b model
to automatically classify data and provide
security recommendations."

---

## Live Demo Steps

### Step 1 — Show Health Endpoint
URL: GET http://localhost:5000/health

Say:
"This is our health endpoint.
It shows the AI model being used,
average response time, and uptime."

Expected Response:
- status: ok
- model: llama-3.3-70b-versatile
- uptime: running time

---

### Step 2 — Show /describe Endpoint
URL: POST http://localhost:5000/describe

Input:
{
    "dataset_name": "Customer_DB",
    "description": "Customer personal information",
    "fields": ["name", "email", "phone", "address"]
}

Say:
"When Java backend creates a new record,
it calls our /describe endpoint.
The AI automatically classifies the data
and identifies privacy risks."

Expected Response:
- classification: PII
- sensitivity_level: HIGH
- compliance requirements listed
- risks identified

---

### Step 3 — Show /recommend Endpoint
URL: POST http://localhost:5000/recommend

Input:
{
    "dataset_name": "Customer_DB",
    "classification": "PII",
    "sensitivity_level": "HIGH",
    "description": "Customer personal information"
}

Say:
"Based on the classification,
our AI recommends 3 specific actions
to protect this data.
Each recommendation has a priority level."

Expected Response:
- 3 recommendations
- action_type, description, priority

---

### Step 4 — Show /generate-report Endpoint
URL: POST http://localhost:5000/generate-report

Input:
{
    "dataset_name": "Customer_DB",
    "classification": "PII",
    "sensitivity_level": "HIGH",
    "description": "Customer personal information",
    "fields": ["name", "email", "phone"]
}

Say:
"Finally our /generate-report endpoint
creates a full structured report
with title, summary, overview,
key items and recommendations."

Expected Response:
- title
- summary
- overview
- key_items
- recommendations

---

## Tech Stack Explanation (60 seconds)

"Our AI service uses:
- Flask for the web framework
- Groq API with LLaMA-3.3-70b model
- Redis for caching responses
- ChromaDB for domain knowledge
- flask-limiter for rate limiting
- Security headers on all responses"

---

## Security Features (30 seconds)

"We implemented several security measures:
- Rate limiting: 30 requests per minute
- Input validation on all endpoints
- Prompt injection protection
- Security headers on all responses
- Fallback responses when AI unavailable"

---

## Response Times Recorded

| Endpoint | Response Time |
|----------|--------------|
| GET /health | Xs |
| POST /describe | Xs |
| POST /recommend | Xs |
| POST /generate-report | Xs |

---

## Backup Screenshots Saved
- health_response.png
- describe_response.png
- recommend_response.png
- report_response.png

---

## Common Questions and Answers

Q: What AI model do you use?
A: LLaMA-3.3-70b by Meta, hosted on Groq.
   It's free tier with no credit card needed.

Q: What if AI is unavailable?
A: We have fallback responses.
   is_fallback: true is returned.
   Service never crashes.

Q: How do you prevent misuse?
A: Rate limiting blocks 30+ req/min.
   Input validation on all endpoints.
   Prompt injection detection.

Q: How fast are responses?
A: Cached responses are instant.
   First requests take 2-5 seconds.
   We use Redis to cache responses.

GET /health          → 11.0 seconds
POST /describe       → 25.97 seconds
POST /recommend      → 1.22 seconds
POST /generate-report → 2.10 seconds