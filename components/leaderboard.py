import tkinter.ttk as ttk
from typing import Dict
from game.team import Team
from game.game_manager import game_manager


PLAYER_FRAME_HEIGHT = 50
PLAYER_FRAME_WIDTH = 400
LEADERBOARD_HEIGHT = 800
LEADERBOARD_WIDTH = 400


class PlayerFrame(ttk.Frame):
    def __init__(
        self, parent: ttk.Frame, player_name: str, equipment_id: int, player_score: int
    ):
        super().__init__(parent)
        self.parent = parent
        self.player_name = player_name
        self.equipment_id = equipment_id
        self.player_score = player_score
        self.is_top_score = False
        ttk.Style().configure("Scoreboard.TLabel", font=("Helvetica", 12, "bold"))
        ttk.Style().configure("StylizedB.TLabel", font=("Helvetica", 12, "bold"))
        self.configure(style="Scoreboard.TFrame")

        self.base = ttk.Label(
            self, text="B", style="StylizedB.TLabel", font=("Agency FB", 15, "bold")
        )

        self.player_name_label = ttk.Label(
            self,
            text=self.player_name,
            style="Scoreboard.TLabel",
        )
        self.player_name_label.grid(row=0, column=1, sticky="ew", pady=3, padx=10)

        self.score_label = ttk.Label(
            self,
            text=f"Score: {self.player_score}",
            style="Scoreboard.TLabel",
        )
        self.score_label.grid(row=0, column=2, sticky="ew", pady=3, padx=10)

    def update_score(self, player_name: str, new_score: int):
        self.player_name = player_name
        self.player_score = new_score
        self.player_name_label["text"] = self.player_name
        self.score_label["text"] = f"Score: {self.player_score}"

    def show_base(self):
        self.base.grid(row=0, column=0, sticky="ew", pady=3, padx=10)

    def remove_base(self):
        self.base.grid_remove()


class Leaderboard(ttk.Frame):
    def __init__(self, parent: ttk.Frame, team: Team):
        super().__init__(parent)
        self.parent = parent
        self.team = team
        self.configure(style=f"{team.team_name}.TFrame")
        self.configure(width=400, height=800, border=1, relief="solid")
        # self.configure(padding=10)
        self.player_frames: Dict[int, PlayerFrame] = {}
        self.highest_score_label = None
        self.is_winning_team = False

        self.team_label = ttk.Label(
            self,
            text=team.team_name + " Team",
            style="Scoreboard.TLabel",
            font=("Helvetica", 15, "bold"),
            foreground="black",
        )
        self.team_label.pack(fill="both", side="top", pady=10, padx=10)

        self.team_score = ttk.Label(
            self,
            text=f"Total Score: {team.points}",
            style="Scoreboard.TLabel",
            font=("Helvetica", 15, "bold"),
        )
        self.team_score.pack(fill="both", side="top", pady=10, padx=10)

        for player in team.players.values():
            player_frame = PlayerFrame(
                self, player.name, player.equipment_id, player.points
            )
            player_frame.pack(fill="x", side="top", padx=10, pady=5)
            self.player_frames[player.equipment_id] = player_frame

        # self.after(500, self.sort_leaderboard)
        self.after(1000, lambda: self.flash_label(self.team_label))

    def flash_label(self, label: ttk.Label):
        if game_manager.get_winning_team() == self.team:
            self.is_winning_team = True
            current_color: str = label.cget("foreground")
            if str(current_color) == "black":
                label.configure(foreground="orange")
            elif str(current_color) == "orange":
                label.configure(foreground="black")

        self.after(1000, lambda: self.flash_label(label))
        self.is_winning_team = False

    def sort_leaderboard(self):
        team_leaderboard = (
            game_manager.red_leaderboard
            if self.team.team_name == "Red"
            else game_manager.green_leaderboard
        )
        for frame in self.winfo_children():
            if isinstance(frame, PlayerFrame):
                # if 1st iteration
                if frame == self.winfo_children()[2]:
                    frame.is_top_score = True
                    frame.player_name_label
                    frame.after(500, lambda: self.flash_label(frame.player_name_label))
                    frame.is_top_score = False
                (points, equipment_id, name) = team_leaderboard.get()
                frame.update_score(name, -points)
        game_manager.red_team.sum_points()
        game_manager.green_team.sum_points()
        self.team_score["text"] = f"Total Score: {self.team.points}"
