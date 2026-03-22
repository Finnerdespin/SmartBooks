import json
import main

FILE = main.resource_path("data/books.json")
_data = {"books": [], "genres": []}

def load_into_memory():
    global _data
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            _data = json.load(f)
    except:
        _data = {"books": [], "genres": []}

def save_to_disk():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(_data, f, indent=4, ensure_ascii=False)

def get_books():
    return _data["books"]

def get_genres():
    return _data["genres"]

def add_book(code, title, author, genre, log=True):
    if any(b["code"] == code for b in _data["books"]):
        return False, "Code bestaat al"
    _data["books"].append({
        "code": code, "title": title, "author": author,
        "genre": genre, "status": "Beschikbaar", "due_date": None
    })
    if log:
        from python import transactions
        transactions.log_change("books", "add_book", [code, title, author, genre])
    return True, "Boek toegevoegd"

def update_status(code, status, due=None, log=True):
    for b in _data["books"]:
        if b["code"] == code:
            b["status"], b["due_date"] = status, due
            if log:
                from python import transactions
                transactions.log_change("books", "update_status", [code, status, due])
            return True
    return False