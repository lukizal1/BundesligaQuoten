# Importieren der erforderlichen Bibliotheken
import tkinter as tk
import requests
from bs4 import BeautifulSoup

# Hauptklasse für die GUI-Anwendung
class SportwettenScraperApp:
    def __init__(self, master):
        self.master = master
        master.title("Sportwetten Scraper")

        # Erstellen von GUI-Elementen
        self.label = tk.Label(master, text="Willkommen zum Sportwetten Scraper!")
        self.label.pack()

        # Extrahiere Bundesliga-Teams und Quoten
        self.extract_bundesliga_teams_and_odds()

    # Funktion zum Extrahieren der Bundesliga-Teams und Quoten
    def extract_bundesliga_teams_and_odds(self):
        url = "https://www.win2day.at/sport/fussball/deutschland/bundesliga-wetten"
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Finden aller divs mit der Klasse "t3-list-entry__info"
        team_info_divs = soup.find_all("div", class_="t3-list-entry__info")

        # Extrahieren der Namen der Bundesliga-Teams und der Quoten
        for i, team_info_div in enumerate(team_info_divs):
            team_names = team_info_div.find_all("a", class_="t3-list-entry__player")
            team1_name = team_names[0].get_text().strip().split("\n")[0]
            team2_name = team_names[1].get_text().strip().split("\n")[0]

            # Beispiel für Quoten von verschiedenen Webseiten
            # Hier müsstest du die Quoten von den verschiedenen Webseiten extrahieren
            # und in einer geeigneten Datenstruktur speichern
            win2day_odds = {"1": 3.40, "X": 4.70, "2": 1.80}
            bwin_odds = {"1": 3.20, "X": 4.60, "2": 1.75}

            # Erstellen der Tabelle für jedes Spiel
            table_frame = tk.Frame(self.master, borderwidth=2, relief="groove", padx=10, pady=10)
            table_frame.pack(pady=10)

            # Anzeigen der Namen der Teams
            team_label = tk.Label(table_frame, text=f"{team1_name} vs {team2_name}")
            team_label.grid(row=0, column=1, columnspan=4)

            # Erstellen der Überschriften für die Quoten
            odds_header_labels = [tk.Label(table_frame, text=""),
                                   tk.Label(table_frame, text="1"),
                                   tk.Label(table_frame, text="X"),
                                   tk.Label(table_frame, text="2")]
            for i, header_label in enumerate(odds_header_labels):
                header_label.grid(row=1, column=i+1)

            # Anzeigen der Quoten von win2day
            win2day_label = tk.Label(table_frame, text="win2day")
            win2day_label.grid(row=2, column=0)
            for i, (bet, value) in enumerate(win2day_odds.items(), start=1):
                odds_label = tk.Label(table_frame, text=f"{value:.2f}")
                odds_label.grid(row=2, column=i+1)

            # Anzeigen der Quoten von bwin
            bwin_label = tk.Label(table_frame, text="bwin")
            bwin_label.grid(row=3, column=0)
            for i, (bet, value) in enumerate(bwin_odds.items(), start=1):
                odds_label = tk.Label(table_frame, text=f"{value:.2f}")
                odds_label.grid(row=3, column=i+1)

# Hauptfunktion, um die Anwendung zu starten
def main():
    root = tk.Tk()
    app = SportwettenScraperApp(root)
    root.mainloop()

# Prüfen, ob die Datei direkt ausgeführt wird
if __name__ == "__main__":
    main()
