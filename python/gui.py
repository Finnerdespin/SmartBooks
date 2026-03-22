import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from python import books, users, transactions


class SmartBooksGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartBooks - High Speed")
        self.root.geometry("1100x650")

        # Herstel eventuele wijzigingen van een eerdere crash
        transactions.apply_and_clear()

        # Inladen in geheugen
        books.load_into_memory()
        users.load_into_memory()

        # Design settings
        self.bg_side = "#1e1e2e"
        self.bg_main = "#f5f5f5"

        self.sidebar = tk.Frame(self.root, width=220, bg=self.bg_side)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(self.root, bg=self.bg_main)
        self.content.pack(side="right", expand=True, fill="both")

        self.draw_menu()
        self.page_books()

    def draw_menu(self):
        tk.Label(self.sidebar, text="SmartBooks", fg="white", bg=self.bg_side, font=("Arial", 16, "bold")).pack(pady=25)
        btns = [
            ("Boekenvoorraad", self.page_books),
            ("Ledenlijst", self.page_users),
            ("Boek Uitlenen", self.page_lend),
            ("Boek Terug", self.page_return)
        ]
        for t, c in btns:
            tk.Button(self.sidebar, text=t, command=c, bg="#2d2d44", fg="white", relief="flat", pady=8).pack(fill="x",
                                                                                                             padx=10,
                                                                                                             pady=2)

    def clear(self):
        for w in self.content.winfo_children(): w.destroy()

    def page_books(self):
        self.clear()
        tk.Label(self.content, text="Boekenvoorraad", font=("Arial", 14, "bold"), bg=self.bg_main).pack(pady=10)
        tree = ttk.Treeview(self.content, columns=("C", "T", "A", "S"), show="headings")
        for c, h in zip(("C", "T", "A", "S"), ("Code", "Titel", "Auteur", "Status")):
            tree.heading(c, text=h);
            tree.column(c, width=150)
        tree.pack(fill="both", expand=True, padx=20, pady=10)
        for b in books.get_books():
            tree.insert("", "end", values=(b["code"], b["title"], b["author"], b["status"]))

    def page_users(self):
        self.clear()
        tk.Label(self.content, text="Ledenlijst", font=("Arial", 14, "bold"), bg=self.bg_main).pack(pady=10)
        tree = ttk.Treeview(self.content, columns=("C", "N", "B"), show="headings")
        tree.heading("C", text="ID");
        tree.heading("N", text="Naam");
        tree.heading("B", text="Geleende Boeken")
        tree.pack(fill="both", expand=True, padx=20, pady=10)
        for u in users.get_users():
            b_list = ", ".join(u["borrowed"]) if u.get("borrowed") else "-"
            tree.insert("", "end", values=(u["code"], u["name"], b_list))

    def page_lend(self):
        self.clear()
        tk.Label(self.content, text="Boek Uitlenen", font=("Arial", 14, "bold"), bg=self.bg_main).pack(pady=20)
        tk.Label(self.content, text="User Code:").pack();
        u_ent = tk.Entry(self.content);
        u_ent.pack()
        tk.Label(self.content, text="Boek Code:").pack();
        b_ent = tk.Entry(self.content);
        b_ent.pack()

        def do():
            u_c, b_c = u_ent.get().upper(), b_ent.get().upper()
            due = (datetime.now() + timedelta(weeks=3)).strftime("%Y-%m-%d")
            if books.update_status(b_c, "Uitgeleend", due):
                users.manage_loan(u_c, b_c, "add")
                messagebox.showinfo("Succes", "Geregistreerd in temp log!")
                self.page_books()
            else:
                messagebox.showerror("Fout", "Niet gevonden")

        tk.Button(self.content, text="Lenen", command=do, bg="#3498db", fg="white").pack(pady=10)

    def page_return(self):
        self.clear()
        tk.Label(self.content, text="Boek Terugbrengen", font=("Arial", 14, "bold"), bg=self.bg_main).pack(pady=20)
        tk.Label(self.content, text="User Code:").pack();
        u_ent = tk.Entry(self.content);
        u_ent.pack()
        tk.Label(self.content, text="Boek Code:").pack();
        b_ent = tk.Entry(self.content);
        b_ent.pack()

        def do():
            u_c, b_c = u_ent.get().upper(), b_ent.get().upper()
            if users.manage_loan(u_c, b_c, "remove"):
                books.update_status(b_c, "Beschikbaar", None)
                messagebox.showinfo("Succes", "Geregistreerd in temp log!")
                self.page_books()
            else:
                messagebox.showerror("Fout", "Niet gevonden")

        tk.Button(self.content, text="Terugbrengen", command=do, bg="#2ecc71", fg="white").pack(pady=10)


def start_gui():
    root = tk.Tk()
    app = SmartBooksGUI(root)

    def on_closing():
        # Bij normaal sluiten ook de log verwerken naar de echte bestanden
        transactions.apply_and_clear()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()