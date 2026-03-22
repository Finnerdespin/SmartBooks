import json
import os
import main

TEMP_FILE = main.resource_path("data/temp.json")


def log_change(module, function, args):
    """Slaat een wijziging op in temp.json."""
    data = []
    if os.path.exists(TEMP_FILE):
        try:
            with open(TEMP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list): data = []
        except:
            data = []

    data.append({
        "module": module,
        "function": function,
        "args": args
    })

    with open(TEMP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def apply_and_clear():
    """Voert wijzigingen uit temp.json door en wist het bestand."""
    if not os.path.exists(TEMP_FILE):
        return

    try:
        with open(TEMP_FILE, "r", encoding="utf-8") as f:
            changes = json.load(f)
    except:
        return

    if not changes or not isinstance(changes, list):
        return

    # Lokale imports om circular dependency te voorkomen
    from python import books, users

    # CRUCIAAL: Eerst de huidige database inladen van schijf!
    books.load_into_memory()
    users.load_into_memory()

    # Voer de acties uit de wachtrij uit
    for change in changes:
        mod_name = change.get("module")
        func_name = change.get("function")
        args = change.get("args", [])

        if mod_name == "books":
            func = getattr(books, func_name, None)
            if func: func(*args, log=False)
        elif mod_name == "users":
            func = getattr(users, func_name, None)
            if func: func(*args, log=False)

    # Nu pas de samengevoegde data opslaan naar de echte JSON bestanden
    books.save_to_disk()
    users.save_to_disk()

    # Maak temp.json leeg
    with open(TEMP_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)