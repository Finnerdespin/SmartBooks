import json
import main

FILE = main.resource_path("data/users.json")
_data = {"users": []}

def load_into_memory():
    global _data
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            _data = json.load(f)
    except:
        _data = {"users": []}

def save_to_disk():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(_data, f, indent=4, ensure_ascii=False)

def get_users():
    return _data["users"]

def add_user(code, name):
    if any(u["code"] == code for u in _data["users"]):
        return False
    _data["users"].append({"code": code, "name": name, "borrowed": []})
    return True

def manage_loan(u_code, b_code, action="add"):
    for u in _data["users"]:
        if u["code"] == u_code:
            if "borrowed" not in u or not isinstance(u["borrowed"], list):
                u["borrowed"] = []
            
            if action == "add":
                u["borrowed"].append(b_code)
            elif action == "remove" and b_code in u["borrowed"]:
                u["borrowed"].remove(b_code)
            return True
    return False
