# Module 8 — FastAPI Calculator

A FastAPI web application that performs basic arithmetic (add, subtract,
multiply, divide) through a REST API and a browser-based calculator UI.
It includes unit, integration, and end-to-end tests, application logging,
Docker support, and a GitHub Actions CI/CD pipeline that tests, security-scans,
and deploys the image to Docker Hub.

## Project Structure

```
.
├── main.py                  # FastAPI app: routes, validation, logging
├── app/
│   └── operations/          # Arithmetic functions (add, subtract, multiply, divide)
├── templates/
│   └── index.html           # Calculator web page (HTML + CSS + JavaScript)
├── tests/
│   ├── conftest.py          # Shared fixtures (live server, Playwright browser)
│   ├── unit/                # Unit tests for app/operations
│   ├── integration/         # API tests using FastAPI TestClient
│   └── e2e/                 # Browser tests using Playwright
├── .github/workflows/test.yml  # CI/CD pipeline (test -> security -> deploy)
├── Dockerfile               # Hardened image with non-root user + healthcheck
├── docker-compose.yml       # Local dev with live reload
├── pytest.ini               # Pytest configuration (coverage, markers)
└── requirements.txt         # Pinned Python dependencies
```

## Getting Started

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies and the Playwright browser
pip install -r requirements.txt
playwright install chromium

# 3. Run the application
python main.py
```

Open http://localhost:8000 to use the calculator. Interactive API docs are
available at http://localhost:8000/docs.

### Run with Docker

```bash
docker compose up --build
```

## Running the Tests

```bash
pytest                    # everything (51 tests) with coverage report
pytest tests/unit/        # unit tests only
pytest tests/integration/ # API integration tests only
pytest tests/e2e/         # Playwright browser tests only
```

## API Endpoints

| Method | Path        | Body                 | Success (200)     | Error (400)                          |
|--------|-------------|----------------------|-------------------|--------------------------------------|
| GET    | `/`         | —                    | HTML page         | —                                    |
| GET    | `/health`   | —                    | `{"status":"ok"}` | —                                    |
| POST   | `/add`      | `{"a": 10, "b": 5}`  | `{"result": 15}`  | `{"error": "..."}` on invalid input  |
| POST   | `/subtract` | `{"a": 10, "b": 5}`  | `{"result": 5}`   | `{"error": "..."}` on invalid input  |
| POST   | `/multiply` | `{"a": 10, "b": 5}`  | `{"result": 50}`  | `{"error": "..."}` on invalid input  |
| POST   | `/divide`   | `{"a": 10, "b": 5}`  | `{"result": 2}`   | `{"error": "Cannot divide by zero!"}`|

## Logging

The application logs every operation and error to the console and to a
rotating file at `logs/app.log` (1 MB per file, 3 backups). Validation
failures and division-by-zero attempts are logged as errors/warnings.

## CI/CD Pipeline

Every push and pull request to `main` triggers `.github/workflows/test.yml`:

1. **test** — installs dependencies and runs unit, integration, and E2E tests.
2. **security** — builds the Docker image and scans it with Trivy, failing on
   unpatched CRITICAL/HIGH vulnerabilities.
3. **deploy** — on `main` only, pushes the verified image to Docker Hub.

### One-time setup for deployment

1. On Docker Hub: create a repository named `calculator-api` and generate a
   personal access token (Account Settings → Security → Personal access
   tokens) with read/write scope.
2. On GitHub: in the repo, go to Settings → Environments and create an
   environment named `production`.
3. In Settings → Secrets and variables → Actions, add:
   - `DOCKERHUB_USERNAME` — your Docker Hub username
   - `DOCKERHUB_TOKEN` — the access token from step 1
