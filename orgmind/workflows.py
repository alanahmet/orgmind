import json
import re
import sqlite3

from . import llm


def meeting_to_tasks(conn: sqlite3.Connection, department_id: int | None, notes: str) -> list[dict]:
    raw = llm.complete(
        "You extract action items from meeting notes. Reply with only a JSON array of objects "
        'with keys "title", "owner" (name or null), "due" (YYYY-MM-DD or null).',
        notes,
    )
    match = re.search(r"\[.*\]", raw, re.S)
    tasks = json.loads(match.group(0)) if match else []
    for t in tasks:
        cur = conn.execute(
            "INSERT INTO tasks (title, owner, due, department_id) VALUES (?, ?, ?, ?)",
            (t["title"], t.get("owner"), t.get("due"), department_id),
        )
        t["id"] = cur.lastrowid
    conn.commit()
    return tasks


def department_report(conn: sqlite3.Connection, department_id: int) -> str:
    tasks = conn.execute(
        "SELECT title, owner, due, status FROM tasks WHERE department_id = ?", (department_id,)
    ).fetchall()
    listing = "\n".join(f"- [{t['status']}] {t['title']} (owner: {t['owner']}, due: {t['due']})" for t in tasks)
    return llm.complete(
        "You write concise weekly department status reports for leadership: progress, risks, next steps.",
        f"Tasks:\n{listing or '(no tasks)'}",
    )
