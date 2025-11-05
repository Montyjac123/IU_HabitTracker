from typing import List, Optional
from datetime import date, timedelta

from .models import Habit
from .db import SQLiteAdapter


class HabitManager:
    def __init__(self, db_path="data/habits.db"):
        self.db = SQLiteAdapter(db_path)

    def add_habit(self, name: str, periodicity: str, notes: str = "") -> Habit:
        habit = Habit(name=name, periodicity=periodicity, notes=notes)
        self.db.save_habit(habit)
        return habit

    def get_all_habits(self) -> List[Habit]:
        rows = self.db.load_all_habits()
        return [Habit.from_dict(r) for r in rows]

    def complete_today(self, habit_id: int):
        today = date.today().isoformat()
        self.db.add_completion(habit_id, today)

    def get_completions(self, habit_id: int):
        return self.db.fetch_completions(habit_id)

    def delete_habit(self, habit_id: int):
        self.db.delete_habit(habit_id)

    def get_streak(self, habit_id: int, periodicity: str):
        dates = self.get_completions(habit_id)
        if not dates:
            return 0

        streak = 0
        today = date.today()

        for i in range(len(dates) - 1, -1, -1):
            d = date.fromisoformat(dates[i])
            if periodicity == "daily":
                expected = today - timedelta(days=streak)
            else:  # weekly
                expected = today - timedelta(weeks=streak)

            if d == expected:
                streak += 1
            else:
                break

        return streak

    def close(self):
        self.db.close()

