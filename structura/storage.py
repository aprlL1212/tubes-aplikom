import json
import os
import sqlite3

DB_PATH = os.environ.get("STRUCTURA_DB", "structura.db")


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS projects (name TEXT PRIMARY KEY, model TEXT NOT NULL)")
    return conn


def save_project(name, model):
    with _connect() as conn: conn.execute("INSERT OR REPLACE INTO projects VALUES (?, ?)", (name, json.dumps(model)))


def list_projects():
    with _connect() as conn: return conn.execute("SELECT name, name FROM projects ORDER BY name").fetchall()


def load_project(name):
    with _connect() as conn: row = conn.execute("SELECT model FROM projects WHERE name = ?", (name,)).fetchone()
    return json.loads(row[0]) if row else {}


def delete_project(name):
    with _connect() as conn: conn.execute("DELETE FROM projects WHERE name = ?", (name,))
