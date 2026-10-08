import os
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS departments (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
    department_id INTEGER REFERENCES departments(id), role TEXT NOT NULL DEFAULT 'member');
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(id));  -- NULL = company-wide
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY, title TEXT NOT NULL, owner TEXT, due TEXT,
    department_id INTEGER REFERENCES departments(id), status TEXT NOT NULL DEFAULT 'open');
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY, user_id INTEGER, department_id INTEGER, kind TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
"""


def connect(path: str | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(path or os.getenv("ORGMIND_DB", "orgmind.db"), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
