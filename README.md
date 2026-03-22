# 📚 SmartBooks

**SmartBooks** is een lichtgewicht en razendsnel bibliotheekbeheersysteem gebouwd in Python. Het project is ontworpen met een focus op snelheid door middel van *in-memory* verwerking en robuustheid dankzij een slim *transaction logging* systeem.

---

## ✨ Belangrijkste functionaliteiten

* **High-Speed Interface:** Alle data (boeken en gebruikers) wordt bij het opstarten ingeladen in het geheugen. Dit zorgt voor een vertragingsvrije ervaring, zelfs bij grotere databases.
* **Crash-Bestendig (Transaction Logging):** Elke wijziging wordt direct opgeslagen in `data/temp.json`. Mocht het programma onverwacht afsluiten of crashen, dan worden de openstaande wijzigingen automatisch verwerkt bij de volgende start.
* **Boekenbeheer:** Houd de volledige voorraad bij, inclusief auteurs, genres en de huidige status (Beschikbaar of Uitgeleend).
* **Ledenbeheer:** Beheer een database met leden en zie in één oogopslag wie welke boeken in bezit heeft.
* **Gebruiksvriendelijke GUI:** Een modern ogende interface gebouwd met de `Tkinter` library, inclusief een zijbalk voor snelle navigatie.

---

## 🏗️ Architectuur & Veiligheid

SmartBooks maakt gebruik van een **Write-Ahead Logging (WAL)** principe om je data veilig te houden:

1.  **Interactie:** Je voert een actie uit in de GUI (bijv. een boek uitlenen).
2.  **Logging:** De actie wordt direct als een kleine transactie opgeslagen in `temp.json`.
3.  **Sync:** Bij het normaal afsluiten van de app (of bij herstel na een crash) worden deze transacties definitief verwerkt in de hoofd-bestanden (`books.json` en `users.json`) en wordt de log gewist.

Dit voorkomt dat je volledige database corrupt raakt als de verbinding of stroom wegvalt tijdens het schrijven van grote bestanden.

---

## 🚀 Installatie & Gebruik

### Vereisten
* Python 3
* Tkinter (standaard inbegrepen bij de meeste Python-installaties)

### Starten
1.  Clone deze repository naar je lokale machine.
2.  Zorg dat de mappenstructuur intact is (zie hieronder).
3.  Start de applicatie via de terminal of command prompt:
    ```bash
    python main.py
    ```

---

## 📁 Projectstructuur

```text
SmartBooks/
├── main.py              # Het startpunt van de applicatie
├── data/                # Bevat alle JSON databases
│   ├── books.json       # Database met boekgegevens
│   ├── users.json       # Database met ledengegevens
│   └── temp.json        # Tijdelijke transactie-log (crash-safe)
└── python/              # De broncode van de applicatie
    ├── books.py         # Logica voor boeken (laden/opslaan/wijzigen)
    ├── users.py         # Logica voor gebruikers en leningen
    ├── transactions.py  # De herstel- en log-engine
    └── gui.py           # De visuele interface (Tkinter)
```
