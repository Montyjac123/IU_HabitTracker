import sqlite3
from typing import List, Dict
from pathlib import Path
from .models import Habit

class SQLiteAdapter:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        schema_file = Path(__file__).parents[1] / 'schema.sql'
        with open(schema_file, 'r') as f:
            self.conn.executescript(f.read())
        self.conn.commit()

    def save_habit(self, h: Habit) -> int:
        cur = self.conn.cursor()
        if h.id is None:
            cur.execute(
                "INSERT INTO habits (name, periodicity, created_at, active, notes) VALUES (?,?,?,?,?)",
                (h.name, h.periodicity, h.created_at, int(h.active), h.notes)
            )
            h.id = cur.lastrowid
        else:
            cur.execute(
                "UPDATE habits SET name=?, periodicity=?, created_at=?, active=?, notes=? WHERE id=?",
                (h.name, h.periodicity, h.created_at, int(h.active), h.notes, h.id)
            )
        self.conn.commit()
        return h.id

    def load_all_habits(self) -> List[Dict]:
        cur = self.conn.cursor()
        cur.execute("SELECT id,name,periodicity,created_at,active,notes FROM habits")
        rows = cur.fetchall()
        results = []
        for r in rows:
            results.append({
                'id': r[0],
                'name': r[1],
                'periodicity': r[2],
                'created_at': r[3],
                'active': r[4],
                'notes': r[5]
            })
        return results

    def add_completion(self, habit_id: int, completion_date: str):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO completions (habit_id, completion_date) VALUES (?,?)",
            (habit_id, completion_date)
        )
        self.conn.commit()

    def fetch_completions(self, habit_id: int):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT completion_date FROM completions WHERE habit_id=? ORDER BY completion_date",
            (habit_id,)
        )
        return [r[0] for r in cur.fetchall()]

    def delete_habit(self, habit_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM habits WHERE id=?", (habit_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

