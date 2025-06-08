### 🚀 Site Crawler API (FastAPI Backend)

This is the backend component of the Site Crawler project. It exposes a FastAPI-based API that authenticates users and logs into selected websites, then scrapes and returns deal data.

---

### 📁 Main Dependencies
| Library          | Purpose                                   |
|------------------|-------------------------------------------|
| **FastAPI**      | Web API framework                         |
| **Uvicorn**      | ASGI server for running FastAPI           |
| **playwright**   | Headless browser automation               |

---

### 🔐 Token-Based Auth
Authenticated endpoints require a token header.
A middleware verifies token validity and returns 401 Unauthorized if invalid or missing.


### 📦 Installation
#### 1. Clone the repository (if not already cloned)
```bash
git clone https://github.com/orisimh/Crawler.git
cd Crawler/backend
```

#### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Install and configure Playwright (if used)
```bash
playwright install
```
---

### 🚀 Run the API

```bash
python main.py
```
Or 
```bash
uvicorn app.main:app --reload
```

### Runs locally at:

```bash
🔗 http://localhost:8000
```

Swagger Docs available at:
```bash
📘 http://localhost:8000/docs
```



