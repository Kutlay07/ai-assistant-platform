# Development Workflow

## Overview

This document describes the development workflow followed throughout the AI Assistant project.

The project follows an architecture-first development process where every feature is designed, implemented, tested, documented, and reviewed before being merged. This workflow keeps the codebase modular, maintainable, and production-ready as it evolves.

---

# Development Lifecycle

Every feature follows the same development cycle.

```text
Issue
   ↓
Architecture Discussion
   ↓
Implementation
   ↓
Testing
   ↓
Documentation
   ↓
Pull Request
   ↓
Review
   ↓
Merge
```

This process encourages thoughtful design before implementation and keeps the repository organized as the system evolves.

---

# Git Workflow

Development follows a simple GitHub-based workflow.

Guidelines:

- Work on one logical task at a time.
- Create issues before implementing features.
- Use dedicated branches for changes.
- Keep commits small and focused.
- Write meaningful commit messages.
- Keep pull requests focused on a single logical change.
- Submit pull requests for review.
- Merge only after tests and documentation are complete.

---

# Branch Naming

Branches should describe the purpose of the change.

Examples:

```text
feature/persistent-memory
feature/agent-workflow
docs/reorganize-documentation
fix/memory-loading-error
```

---

# Commit Convention

The project follows the Conventional Commits specification.

Common commit types:

- `feat` – New features
- `fix` – Bug fixes
- `docs` – Documentation changes
- `refactor` – Code improvements without behavior changes
- `test` – Test additions or improvements
- `chore` – Maintenance and configuration

Examples:

```text
feat(memory): add persistent file storage

docs: reorganize architecture documentation

test(agent): add workflow integration tests
```

---

# Documentation

Documentation is treated as part of the implementation process.

Guidelines:

- Keep documentation synchronized with code changes.
- Keep diagrams synchronized with architectural changes.
- Record architectural decisions using ADRs.
- Update architecture documents when responsibilities change.
- Explain why decisions were made, not only what was implemented.

---

# Testing

Testing is introduced incrementally as the project grows.

Principles:

- Prefer isolated unit tests.
- Test public behavior instead of internal implementation details.
- Add integration tests for workflows and major features.
- New features should be accompanied by appropriate tests whenever possible.
- Ensure tests pass before merging changes.

---

# Running the Application

The complete stack (backend, frontend, PostgreSQL + pgvector) is orchestrated with Docker
Compose and is the recommended way to run the project:

```bash
cp .env.example .env
docker compose up
```

The sections below describe running the backend and the frontend directly, which is useful
when iterating on a single component.

Requirements for local execution:

* Python 3.11+
* Node.js 22+
* A reachable PostgreSQL instance with the `vector` extension available
  (`docker compose up postgres` is the simplest option)

---

## Backend Setup & Execution

Navigate to the `backend/` directory:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -e ".[dev]"
```

Configure the environment (the backend reads a `.env` file from the working directory):

```bash
cp ../.env.example .env
# for local execution, point POSTGRES_CONNECTION_STRING at localhost
```

Start the development server:

```bash
python main.py
```


Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

Run test suite:

```bash
python -m pytest
```

---

## Frontend Setup & Execution

In a separate terminal, navigate to the `frontend/` directory:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at:

```text
http://127.0.0.1:5173
```

---

## Local Development Flow

During development:

* Run both the backend and frontend simultaneously.
* The frontend communicates with the backend through the `/api/v1/chat` and
  `/api/v1/chat/stream` endpoints.
* Streaming responses are delivered as a chunked `text/plain` HTTP body and read in the
  browser with `fetch` + `ReadableStream`.
* Conversation history is persisted between sessions through the configured memory backend.

---

# Releases

Releases are milestone-based rather than commit-based.

Each release represents a meaningful stage in the project's evolution.

A release should include:

- Completed features
- Updated documentation
- Passing test suite
- Stable architecture

---

# Project Philosophy

The project's engineering principles are documented separately.

See:

- [ADR-0001 — Project Philosophy](decisions/ADR-0001-project-philosophy.md)
- [ADR-0002 — Provider Independence](decisions/ADR-0002-provider-independence.md)