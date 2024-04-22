import tkinter as tk
import tkinter.ttk as ttk
from components.event_window import EventWindow
from game.udp import udp
from game.udp import RED_BASE, GREEN_BASE


class ActionDisplay(ttk.Frame):
    def __init__(self, parent, controller, player_entries, switch_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.controller = controller
        self.player_entries = player_entries
        self.switch_callback = (
            switch_callback  # Function to switch back to player entry screen
        )

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Red.TFrame", background="#800000")
        self.style.configure("Green.TFrame", background="green")
        self.style.configure("TeamLabel.TLabel", foreground="black", font=("Helvetica"))
        self.style.configure(
            "PlayerName.TLabel", foreground="#white", font=("Helvetica")
        )
        self.style.configure("Score.TLabel", foreground="#white", font=("Helvetica"))

        self.red_column = ttk.Frame(self, style="Red.TFrame")
        self.red_column.grid(row=0, column=0, sticky="nsew")

        self.green_column = ttk.Frame(self, style="Green.TFrame")
        self.green_column.grid(row=0, column=1, sticky="nsew")

        self.display_scoreboard()
        self.create_f5_button()
        udp.entry_thread.stop()
        udp.broadcast_code(202)
        udp.action_thread.start()

        # implementation for the countdown timer

        self.timer_label = ttk.Label(self, text="", font=("Helvetica", 30))
        self.timer_label.grid(row=2, column=0, columnspan=2)
        self.event_window = EventWindow(self)
        self.event_window.grid(row=3, columnspan=2, padx=6, pady=6)

        self.start_timer()

    def start_timer(self, count=5):
        if count > 0:
            self.timer_label.configure(text=str(count))
            self.parent.after(1000, lambda: self.start_timer(count - 1))
        else:
            self.timer_label.configure(text="")

    def display_scoreboard(self):
        for team, entries in self.player_entries.items():
            column = self.red_column if team == "Red" else self.green_column

            ttk.Label(column, text=team + " Team", style="Scoreboard.TLabel").grid(
                row=0, column=0, sticky="ew", pady=(10, 5)
            )

            row_num = 1
            for player_id, (user_id_entry, player_name_entry) in entries.items():
                player_name_label = ttk.Label(
                    column,
                    text=player_name_entry.cget("text"),
                    style="Scoreboard.TLabel",
                )
                player_name_label.grid(
                    row=row_num, column=0, sticky="ew", pady=3, padx=10
                )
                player_name_label.configure

                score_label = ttk.Label(
                    column, text="Score: 0", style="Scoreboard.TLabel"
                )
                score_label.grid(row=row_num, column=1, sticky="ew", pady=3, padx=10)
                score_label.configure
                row_num += 1

        # Adjust row and column weights to make the columns expandable
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def create_f5_button(self):
        f5_button = ttk.Button(self, text="Return to Entry Screen", command=self.switch_callback)
        f5_button.grid(row=1, column=0, columnspan=2, pady=10)

def base_scores(self, from_id, to_id):
    if to_id == RED_BASE:
        scoring_team = "Green"
    elif to_id == GREEN_BASE:
        scoring_team = "Red"
    else:
        return
    
    if from_id in self.player_entries[scoring_team]:
        # Add 100 points to the player's score
        self.player_entries[scoring_team][from_id].score += 100
        # Add a "B" to the left of the player's codename
        player_name_entry = self.player_entries[scoring_team][from_id].player_name_entry
        player_name_entry.config(text="B" + player_name_entry.cget("text"))

        # Update the score label in the UI
        score_label = self.red_column if scoring_team == "Red" else self.green_column
        score_label = score_label.grid_slaves(row=1 + list(self.player_entries[scoring_team].keys()).index(from_id), column=1)[0]
        score_label.config(text=f"Score: {self.player_entries[scoring_team][from_id].score}")

        print(f"Player {from_id} scored at the {scoring_team.lower()} base!")
    else:
        print(f"Player {from_id} is not on the {scoring_team.lower()} team.")