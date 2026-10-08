from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from . import db, knowledge, llm, workflows

app = FastAPI(title="OrgMind", version="0.1.0")
conn = db.connect()


class Department(BaseModel):
    name: str


class User(BaseModel):
    name: str
    email: str
    department_id: int | None = None
    role: str = "member"


class Document(BaseModel):
    title: str
    content: str
    department_id: int | None = None


class Question(BaseModel):
    question: str


class Notes(BaseModel):
    notes: str


def current_user(x_user_id: int = Header(...)):
    user = conn.execute("SELECT * FROM users WHERE id = ?", (x_user_id,)).fetchone()
    if not user:
        raise HTTPException(401, "Unknown user")
    return user


def log(user, kind: str):
    conn.execute(
        "INSERT INTO events (user_id, department_id, kind) VALUES (?, ?, ?)",
        (user["id"], user["department_id"], kind),
    )
    conn.commit()


@app.post("/departments")
def create_department(d: Department):
    cur = conn.execute("INSERT INTO departments (name) VALUES (?)", (d.name,))
    conn.commit()
    return {"id": cur.lastrowid, "name": d.name}


@app.post("/users")
def create_user(u: User):
    cur = conn.execute(
        "INSERT INTO users (name, email, department_id, role) VALUES (?, ?, ?, ?)",
        (u.name, u.email, u.department_id, u.role),
    )
    conn.commit()
    return {"id": cur.lastrowid, **u.model_dump()}


@app.post("/documents")
def add_document(d: Document, user=Depends(current_user)):
    if user["role"] != "admin" and d.department_id not in (None, user["department_id"]):
        raise HTTPException(403, "Cannot add documents to another department")
    cur = conn.execute(
        "INSERT INTO documents (title, content, department_id) VALUES (?, ?, ?)",
        (d.title, d.content, d.department_id),
    )
    conn.commit()
    return {"id": cur.lastrowid}


@app.post("/ask")
def ask(q: Question, user=Depends(current_user)):
    docs = knowledge.search(conn, user, q.question)
    context = "\n\n".join(f"[{d['id']}] {d['title']}\n{d['content']}" for d in docs)
    answer = llm.complete(
        "Answer using only the company documents provided. Cite document ids like [3]. "
        "If the answer is not in them, say so.",
        f"Documents:\n{context or '(none)'}\n\nQuestion: {q.question}",
    )
    log(user, "ask")
    return {"answer": answer, "sources": [{"id": d["id"], "title": d["title"]} for d in docs]}


@app.post("/workflows/meeting-to-tasks")
def meeting_to_tasks(n: Notes, user=Depends(current_user)):
    tasks = workflows.meeting_to_tasks(conn, user["department_id"], n.notes)
    log(user, "meeting_to_tasks")
    return {"tasks": tasks}


@app.post("/workflows/department-report")
def department_report(user=Depends(current_user)):
    if user["department_id"] is None:
        raise HTTPException(400, "User has no department")
    log(user, "department_report")
    return {"report": workflows.department_report(conn, user["department_id"])}


@app.get("/analytics")
def analytics(user=Depends(current_user)):
    if user["role"] != "admin":
        raise HTTPException(403, "Admins only")
    rows = conn.execute(
        """SELECT d.name,
                  (SELECT COUNT(*) FROM events e WHERE e.department_id = d.id) AS ai_actions,
                  (SELECT COUNT(*) FROM tasks t WHERE t.department_id = d.id AND t.status = 'open') AS open_tasks
           FROM departments d"""
    ).fetchall()
    return [dict(r) for r in rows]
