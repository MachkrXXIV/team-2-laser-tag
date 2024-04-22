import tkinter as tk
import tkinter.ttk as ttk
from components.event_window import EventWindow
from game.game_manager import game_manager
from game.udp import udp
from game.player import Player


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

    def display_scoreboard(self):
        print("displaying")

        # Variables to track the team with the higher overall score and the corresponding team label
        red_team_score = sum(
            player.points for player in game_manager.red_team.players.values()
        )
        green_team_score = sum(
            player.points for player in game_manager.green_team.players.values()
        )
        higher_score_team = "Red" if red_team_score > green_team_score else "Green"
        higher_score_team_label = (
            self.red_column if higher_score_team == "Red" else self.green_column
        )

        # Variables to track the highest player score and the corresponding player label
        highest_score = -1
        highest_score_label = None
        
        # Variables to track total scores for each team
        red_total_score = sum(player.points for player in game_manager.red_team.players.values())
        green_total_score = sum(player.points for player in game_manager.green_team.players.values())     

        for team, entries in self.player_entries.items():
            column = self.red_column if team == "Red" else self.green_column

            # Create a frame for team labels
            team_label_frame = ttk.Frame(column)
            team_label_frame.grid(row=0, column=0, sticky="ew", pady=(10, 5))

            team_label = ttk.Label(
                team_label_frame,
                text=team + " Team",
                style="Scoreboard.TLabel",
                font=("Helvetica", 15, "bold"),
            )
            team_label.pack(fill="both")

            if team == higher_score_team:
                self.flash_label(team_label)

            # Create a frame for player labels
            player_label_frame = ttk.Frame(column)
            player_label_frame.grid(row=1, column=0, sticky="nsew")

            row_num = 0
            row_num = 0
            for player_id, (user_id_entry, player_name_entry) in entries.items():
                player_name_label = ttk.Label(
                    player_label_frame,
                    text=player_name_entry.cget("text"),
                    style="Scoreboard.TLabel",
                )
                player_name_label.grid(
                    row=row_num, column=0, sticky="ew", pady=3, padx=10
                )

                # Get the player's score from game_manager and update the score label
                player_score = 0  # Initialize player score
                if team == "Red":
                    if player_id in game_manager.red_team.players:
                        player_score = game_manager.red_team.players[player_id].points
                else:
                    if player_id in game_manager.green_team.players:
                        player_score = game_manager.green_team.players[player_id].points

                score_label = ttk.Label(
                    player_label_frame,
                    text=f"Score: {player_score}",
                    style="Scoreboard.TLabel",
                )
                score_label.grid(row=row_num, column=1, sticky="ew", pady=3, padx=10)
                # Check if the current player has the highest score
                if player_score > highest_score:
                    highest_score = player_score
                    highest_score_label = player_name_label
                # Check if the current player has the highest score
                if player_score > highest_score:
                    highest_score = player_score
                    highest_score_label = player_name_label
                row_num += 1
                    
                # Adjust leaderboard based on the team
                game_manager.adjust_leaderboard(team_name=team)

        # Adjust row and column weights to make the columns expandable
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Flash the label of the highest scoring player
        self.flash_label(highest_score_label)

        # Place total score labels at the bottom
        red_total_label = ttk.Label(self.red_column, text=f"Total Score: {red_total_score}", style="Scoreboard.TLabel")
        red_total_label.grid(row=20, column=0, sticky="ew", pady=(10, 5))

        green_total_label = ttk.Label(self.green_column, text=f"Total Score: {green_total_score}", style="Scoreboard.TLabel")
        green_total_label.grid(row=20, column=0, sticky="ew", pady=(10, 5))
    
        # self.flash_label(highest_score_label)
        if highest_score_label:
            self.flash_label(highest_score_label)

    def flash_label(self, label):
        if label and label.winfo_ismapped():
            label.grid_remove()
        elif label:
            label.grid()
        self.after(500, lambda: self.flash_label(label))

    def create_f5_button(self):
        f5_button = ttk.Button(self, text="Return to main screen", command=self.switch_callback)
        f5_button.grid(row=0, column=1, sticky="e", padx=10)
        udp.action_thread.stop()
