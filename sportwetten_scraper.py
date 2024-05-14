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

        # Button zum Extrahieren des Seitentitels
        self.extract_title_button = tk.Button(master, text="Titel der Seite extrahieren", command=self.extract_title)
        self.extract_title_button.pack()

        # Button zum Extrahieren der Bundesliga-URLs von bwin
        self.extract_bundesliga_urls_button = tk.Button(master, text="Bundesliga-Spiel URLs extrahieren",
                                                        command=self.extract_bundesliga_urls)
        self.extract_bundesliga_urls_button.pack()

    # Funktion zum Extrahieren des Seitentitels
    def extract_title(self):
        url = "https://www.win2day.at"
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.title.string
        print("Seitentitel:", title)

    # Funktion zum Extrahieren der URLs der Bundesliga-Spiele von bwin
    def extract_bundesliga_urls(self):
        url = "https://www.win2day.at/sport/fussball/deutschland/bundesliga-wetten"
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Finde alle Links zu den Bundesliga-Spielen
        links = soup.find_all("a", class_="marketboard-event-without-link")

        # Extrahiere die URLs der Bundesliga-Spiele
        bundesliga_urls = [link["href"] for link in links]

        # Ausgabe der extrahierten URLs
        print("Bundesliga-Spiel URLs:")
        for url in bundesliga_urls:
            print(url)


# Hauptfunktion, um die Anwendung zu starten
def main():
    root = tk.Tk()
    app = SportwettenScraperApp(root)
    root.mainloop()


# Prüfen, ob die Datei direkt ausgeführt wird
if __name__ == "__main__":
    main()
