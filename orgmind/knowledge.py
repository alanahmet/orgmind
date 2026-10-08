"""Permission-aware keyword retrieval. Swap for pgvector embeddings in production."""
import re
import sqlite3


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"\w+", text.lower()) if len(t) > 2}


def visible_documents(conn: sqlite3.Connection, user: sqlite3.Row) -> list[sqlite3.Row]:
    if user["role"] == "admin":
        return conn.execute("SELECT * FROM documents").fetchall()
    return conn.execute(
        "SELECT * FROM documents WHERE department_id IS NULL OR department_id = ?",
        (user["department_id"],),
    ).fetchall()


def search(conn: sqlite3.Connection, user: sqlite3.Row, query: str, k: int = 4) -> list[sqlite3.Row]:
    q = _tokens(query)
    scored = [(len(q & _tokens(d["title"] + " " + d["content"])), d) for d in visible_documents(conn, user)]
    return [d for score, d in sorted(scored, key=lambda x: -x[0]) if score > 0][:k]
