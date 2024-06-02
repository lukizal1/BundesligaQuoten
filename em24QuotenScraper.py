# em24QuotenScraper.py

import pandas as pd
import tkinter as tk
from tkinter import ttk
import webbrowser
from scraping import scrape_emirbet, scrape_win2day, scrape_tipp3


def collect_odds():
    all_odds = []
    all_odds.extend(scrape_emirbet())
    all_odds.extend(scrape_win2day())
    all_odds.extend(scrape_tipp3())
    return all_odds


def open_link(url):
    webbrowser.open(url)

# Vergleiche die Quoten und markiere die besten
def compare_odds(odds):
    df = pd.DataFrame(odds)
    # Quoten von deutschen Kommazahlen in Dezimalzahlen umwandeln
    df['odds_team1'] = df['odds_team1'].str.replace(',', '.').astype(float)
    df['odds_team2'] = df['odds_team2'].str.replace(',', '.').astype(float)
    df['odds_draw'] = df['odds_draw'].str.replace(',', '.').astype(float)
    # Beste Quoten hervorheben
    df['best_team1'] = df['odds_team1'] == df.groupby(['team1', 'team2'])['odds_team1'].transform('max')
    df['best_team2'] = df['odds_team2'] == df.groupby(['team1', 'team2'])['odds_team2'].transform('max')
    df['best_draw'] = df['odds_draw'] == df.groupby(['team1', 'team2'])['odds_draw'].transform('max')
    return df

# GUI erstellen
# GUI erstellen
def create_gui(grouped_odds):
    root = tk.Tk()
    root.title("Wettquoten Fußball-EM 2024")

    # Scrollable Frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Daten im GUI anzeigen
    for (team1, team2), group in grouped_odds:
        match = f"{team1} vs {team2}"
        match_label = tk.Label(scrollable_frame, text=match, font=('Helvetica', 16, 'bold'))
        match_label.pack(pady=10)

        odds_frame = tk.Frame(scrollable_frame)
        odds_frame.pack()

        odds_1_label = tk.Label(odds_frame, text="1", padx=10, font='bold')
        odds_1_label.grid(row=0, column=0, sticky='w')

        odds_x_label = tk.Label(odds_frame, text="X", padx=10, font='bold')
        odds_x_label.grid(row=0, column=1)

        odds_2_label = tk.Label(odds_frame, text="2", padx=10, font='bold')
        odds_2_label.grid(row=0, column=2, sticky='e')

        # Initialisiere Variablen für die höchsten Quoten
        max_odds_team1 = group['odds_team1'].max()
        max_odds_draw = group['odds_draw'].max()
        max_odds_team2 = group['odds_team2'].max()

        idx = 1
        for _, row in group.iterrows():
            odds_text_team1 = f"{row['odds_team1']}"
            odds_label_team1 = tk.Label(odds_frame, text=odds_text_team1)
            if row['odds_team1'] == max_odds_team1:
                odds_label_team1.config(fg='dark green')
            else:
                odds_label_team1.config(fg='dark red')
            odds_label_team1.grid(row=idx, column=0, sticky='w')

            odds_text_draw = f"{row['odds_draw']}"
            odds_label_draw = tk.Label(odds_frame, text=odds_text_draw)
            if row['odds_draw'] == max_odds_draw:
                odds_label_draw.config(fg='dark green')
            else:
                odds_label_draw.config(fg='dark red')
            odds_label_draw.grid(row=idx, column=1)

            odds_text_team2 = f"{row['odds_team2']}"
            odds_label_team2 = tk.Label(odds_frame, text=odds_text_team2)
            if row['odds_team2'] == max_odds_team2:
                odds_label_team2.config(fg='dark green')
            else:
                odds_label_team2.config(fg='dark red')
            odds_label_team2.grid(row=idx, column=2, sticky='e')

            idx += 1

            if 'link' in row:
                link_button = tk.Button(odds_frame, text=row['source'], command=lambda url=row['link']: open_link(url))
                link_button.grid(row=idx, column=0, columnspan=3)
                idx += 1

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    root.mainloop()




if __name__ == "__main__":
    try:
        odds = collect_odds()
        comparison = compare_odds(odds)
        grouped_odds = comparison.groupby(['team1', 'team2'])
        create_gui(grouped_odds)
    except Exception as e:
        print(f"Fehler beim Ausführen des Programms: {e}")
