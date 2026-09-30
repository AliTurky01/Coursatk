# Dependency Management Guide (`uv` + Docker)

This project uses **Astral's `uv`** along with a two-tiered requirements pattern (`requirements.in` and `requirements.txt`) to achieve fast, deterministic, reproducible builds across local machines and Docker environments.

---

## 1. Overview of the Strategy

| File | Purpose | Managed By |
| :--- | :--- | :--- |
| **`requirements.in`** | Human-readable list of **direct dependencies** and necessary extras (e.g., `fastapi`, `SQLAlchemy[asyncio]`). | Developers (manual edits) |
| **`requirements.txt`** | Machine-generated, fully-pinned **lockfile** listing all direct and transitive dependencies with exact versions. | `uv pip compile` (automated) |

### Why not edit `requirements.txt` manually?
Manual updates easily cause subtle dependency conflicts, broken transitive sub-dependencies (like missing `greenlet` or mismatched crypto backends), and non-reproducible builds across different environments.

---

## 2. Prerequisites

You do not necessarily need a virtual environment, but you will need `uv` on your host machine to compile locks quickly:

```bash
# macOS / Linux / WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

*(Alternatively, you can compile via Docker without installing `uv` locally—see Section 3.2).*

---

## 3. Daily Workflows

### 3.1 Adding, Removing, or Updating a Package

1. **Edit `requirements.in`:**  
   Add the top-level package or required extras. Keep entries high-level:
   ```text
   # Example: Adding httpx and SQLAlchemy with async support
   fastapi
   uvicorn[standard]
   SQLAlchemy[asyncio]
   httpx
   ```

2. **Re-compile `requirements.txt`:**  
   Run the solver from your project root:
   ```bash
   uv pip compile requirements.in -o requirements.txt
   ```

3. **Rebuild your Docker container:**
   ```bash
   docker compose up --build
   ```

---

### 3.2 Compiling Without a Local `uv` Installation (Docker-Only)

If a developer does not have `uv` installed on their host machine, use a one-off Docker container to compile:

```bash
# macOS / Linux / WSL
docker run --rm -v "$(pwd):/app" -w /app ghcr.io/astral-sh/uv:latest pip compile requirements.in -o requirements.txt

# Windows PowerShell
docker run --rm -v "${PWD}:/app" -w /app ghcr.io/astral-sh/uv:latest pip compile requirements.in -o requirements.txt
```

---

### 3.3 Upgrading All Dependencies

To upgrade all pinned packages to their latest compatible versions:

```bash
uv pip compile --upgrade requirements.in -o requirements.txt
```

To upgrade only a single package (and its sub-tree):

```bash
uv pip compile --upgrade-package fastapi requirements.in -o requirements.txt
```

---

## 4. Docker Integration Pattern

Inside your `Dockerfile`, copy the compiled `requirements.txt` and use `uv` directly against the system Python:

```dockerfile
FROM python:3.12-slim

# Copy uv binary directly from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Cache dependency layer
COPY requirements.txt .

# Install dependencies into system Python without local wheels caching
RUN uv pip install --system --no-cache -r requirements.txt

# Copy application source
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 5. Best Practices & Rules

1. **Always declare package extras explicitly:**  
   Libraries with optional async or speedup components must include their bracketed extras (e.g., `SQLAlchemy[asyncio]`, `uvicorn[standard]`, `python-jose[cryptography]`).
2. **Never commit without compiling:**  
   Whenever you change `requirements.in`, ensure `requirements.txt` is updated and committed to Git simultaneously.
3. **Keep `requirements.in` clean:**  
   Do not list indirect dependencies (like `pydantic`, `starlette`, or `greenlet`) unless your code explicitly imports them independent of their parent libraries.