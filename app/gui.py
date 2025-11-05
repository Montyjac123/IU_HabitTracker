import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from .manager import HabitManager


class HabitApp:
    def __init__(self, root):
        self.manager = HabitManager()
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("500x500")

        # Main Frame
        frame = tk.Frame(root)
        frame.pack(pady=10)

        # Habit Name
        tk.Label(frame, text="Habit Name").grid(row=0, column=0)
        self.habit_name = tk.Entry(frame)
        self.habit_name.grid(row=0, column=1)

        # Periodicity
        tk.Label(frame, text="Periodicity").grid(row=1, column=0)
        self.periodicity = ttk.Combobox(frame, values=["daily", "weekly"])
        self.periodicity.current(0)
        self.periodicity.grid(row=1, column=1)

        # Add habit button
        tk.Button(frame, text="Add Habit", command=self.add_habit).grid(row=2, column=1, pady=10)

        # Habit list
        self.habit_list = tk.Listbox(root, height=10, width=40)
        self.habit_list.pack(pady=10)

        # Buttons
        tk.Button(root, text="Mark Completed", command=self.mark_completed).pack()
        tk.Button(root, text="Delete Habit", command=self.delete_habit).pack()
        tk.Button(root, text="Show Streak", command=self.show_streak).pack()

        self.refresh_habits()

    def add_habit(self):
        name = self.habit_name.get()
        periodicity = self.periodicity.get()

        if not name:
            messagebox.showwarning("Warning", "Habit name cannot be empty.")
            return

        self.manager.add_habit(name, periodicity)
        self.refresh_habits()
        self.habit_name.delete(0, tk.END)

    def refresh_habits(self):
        self.habit_list.delete(0, tk.END)

        habits = self.manager.get_all_habits()
        for h in habits:
            self.habit_list.insert(tk.END, f"{h.id} | {h.name} ({h.periodicity})")

    def get_selected_habit_id(self):
        try:
            selection = self.habit_list.get(self.habit_list.curselection())
            habit_id = int(selection.split("|")[0].strip())
            return habit_id
        except:
            messagebox.showwarning("Warning", "Select a habit first.")
            return None

    def mark_completed(self):
        habit_id = self.get_selected_habit_id()
        if habit_id:
            self.manager.complete_today(habit_id)
            messagebox.showinfo("Success", "Habit marked completed!")

    def delete_habit(self):
        habit_id = self.get_selected_habit_id()
        if habit_id:
            self.manager.delete_habit(habit_id)
            self.refresh_habits()

    def show_streak(self):
        habit_id = self.get_selected_habit_id()
        if habit_id:
            habits = self.manager.get_all_habits()
            habit = next(h for h in habits if h.id == habit_id)
            streak = self.manager.get_streak(habit_id, habit.periodicity)
            messagebox.showinfo("Streak", f"Current streak: {streak}")


