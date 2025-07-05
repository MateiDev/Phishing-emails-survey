# Phishing-E-mails Survey

> **Bachelor-thesis project (2025)**  
> Collecting human input on how “human” vs “AI-generated” phishing e-mails differentiate.

| Layer | Technologies | Purpose |
|-------|------|---------|
| Front-end | Plain HTML + CSS + vanilla JS | Displays 4 mock phishing e-mails and collects input / comments. |
| Back-end API | Python **FastAPI** | Logs user-info and e-mail assessments, serves the static front-end. |
| Database | **SQLite** (`survey.db`)| Used for saving the data |
| Hosting (survey period) | **Cloudflare Tunnel** → local **Uvicorn** | Proxied `survey.voedingswaarden.com` → `localhost:8000` |

---

## Quick start (local dev)

```bash
# 1. Clone & enter the repo
git clone https://github.com/MateiDev/Phishing-emails-survey.git
cd Phishing-emails-survey

# 2. Install dependencies
pip install -r requirements.txt 

# 3. Launch the app
cd backend
uvicorn main:app --reload

# The intro page will open on http://127.0.0.1:8000
```

## View the results

Open the built-in dashboard: http://127.0.0.1:8000/results

The page shows    
* **Demographics pies** – age groups, gender, current role.  
* **Per-e-mail charts**  
  * a piechart with the reasons participants selected 
  * a 1-to-10 *Human ↔ AI* bar chart.  
* A **“View remarks”** button on each e-mail card that pops up every free-text comment.
