import json
import os

BUDGET_FILE = "butce.json"

def load_budget():
    if os.path.exists(BUDGET_FILE):
        try:
            with open(BUDGET_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("budget", 0.0)
        except json.JSONDecodeError:
            return 0.0
    return 0.0

def save_budget(amount):
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump({"budget": amount}, f)
