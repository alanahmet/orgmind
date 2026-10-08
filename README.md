# OrgMind

**Open-source AI productivity for the whole organization, not just individual employees.**

Most AI tools make one person faster. OrgMind makes the *company* faster: a shared knowledge base,
department-scoped AI workflows, role-based access, and org-level insight into where time is lost.

## Features (v0.1)
- **Company knowledge base**: ingest docs, policies and SOPs; ask questions answered with sources.
- **Workflow agents**: turn meeting notes into tasks with owners and deadlines; draft weekly department reports.
- **Roles & departments**: every user and document belongs to a department; the AI only sees what the user may see.
- **Org analytics**: track AI usage and tasks per department to find bottlenecks.
- **Self-hosted & free**: MIT license, SQLite by default, Docker Compose included. Bring your own Claude API key.

## Quick start
```bash
pip install -e .
cp .env.example .env        # add ANTHROPIC_API_KEY
uvicorn orgmind.api:app --reload
# open http://localhost:8000/docs
```
Or with Docker: `docker compose up`.

## API overview
| Endpoint | Purpose |
|---|---|
| `POST /departments` / `POST /users` | Set up org structure |
| `POST /documents` | Add knowledge (scoped to a department or `company`) |
| `POST /ask` | Ask the knowledge base (permission-filtered) |
| `POST /workflows/meeting-to-tasks` | Extract tasks from meeting notes |
| `POST /workflows/department-report` | Generate a department status report |
| `GET /analytics` | Usage and tasks per department |

All requests identify the user with the `X-User-Id` header.

## Roadmap
Connectors (Gmail, Drive, Slack, Trello via MCP), vector search (pgvector), approval workflows, SSO.

## License
MIT. Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
