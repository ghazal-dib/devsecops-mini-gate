# 🔐 DevSecOps Mini Security Gate

This project demonstrates a **Python-based Security Gate** integrated into a **GitHub Actions CI/CD pipeline**.  
It simulates real-world DevSecOps practices used to **block insecure deployments** based on security findings.

---

## 🎯 Project Goals

The security gate enforces the following policies before allowing deployment:

- Ensure required secrets are present
- Detect leaked secrets in application logs
- Parse vulnerability reports (JSON)
- Block pipelines on critical security issues
- Return proper exit codes to CI/CD

---

## 🧱 Project Structure

devsecops-mini-gate/
├── gate.py
├── report.json
├── app.log
├── README.md
└── .github/
    └── workflows/
        └── pipeline.yml


---

## ⚙️ How It Works

### 1️⃣ Secret Validation
- Reads `API_KEY` from environment variables
- If missing → pipeline **BLOCKED**

### 2️⃣ Secret Leak Detection
- Scans `app.log` for:
  - `API_KEY`
  - `PASSWORD`
  - `AWS_SECRET`
- If detected → pipeline **BLOCKED**

### 3️⃣ Vulnerability Analysis
- Parses `report.json`
- Rules:
  - Any `CRITICAL` → BLOCK
  - `HIGH` ≥ 2 → BLOCK
  - `HIGH` = 1 → WARN
  - Otherwise → OK

### 4️⃣ CI/CD Decision
- Uses `sys.exit(1)` to fail pipeline
- Uses `sys.exit(0)` to allow pipeline

---

## 🚦 Example Outcomes

| Scenario | Pipeline Result |
|--------|----------------|
| Missing API_KEY | ❌ BLOCK |
| Secret leak detected | ❌ BLOCK |
| CRITICAL vulnerability | ❌ BLOCK |
| Two HIGH vulnerabilities | ❌ BLOCK |
| One HIGH vulnerability | ⚠️ WARN |
| Clean report | ✅ OK |

---

## 🧪 Technologies Used

- Python 3
- GitHub Actions
- JSON parsing
- Environment Variables
- CI/CD Security Gates

---

## 🧠 Why This Project Matters

This project mirrors **real DevSecOps workflows** used in production environments:

- Security-first pipelines
- Automated enforcement
- Fail-fast strategy
- No hard-coded secrets

It is suitable for **Junior DevSecOps / Security Automation roles**.

---

## 🚀 How to Run Locally

### Linux / macOS
```bash
export API_KEY=test123
python gate.py


### Windows (PowerShell)
```bash
setx API_KEY "test123"
python gate.py
