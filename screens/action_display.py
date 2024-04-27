import tkinter as tk
import tkinter.ttk as ttk
from components.event_window import EventWindow
from game.game_manager import game_manager
from game.udp import udp
from game.player import Player
import os
import time
from components.leaderboard import Leaderboard

from components.event_window import EventWindow
from components.timer_box import TimerWindow
from game.udp import udp

RED_BASE = 53
GREEN_BASE = 43
UDP_REFRESH_RATE = 500
GAME_START_TIME = 22_000
TIMER_WINDOW_WIDTH = 200
TIMER_WINDOW_HEIGHT = 200


class ActionDisplay(ttk.Frame):
    def __init__(
        self, parent: ttk.Frame, controller, player_entries, switch_callback, **kwargs
    ):
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
        self.configure(width=1050, height=800)
        self.style.configure("Score.TLabel", foreground="#white", font=("Helvetica"))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.grid(row=0, column=0, sticky="nsew", columnspan=3, rowspan=3)
        self.timer = TimerWindow(self)
        self.timer.grid(row=0, column=0, columnspan=2)

        self.red_column = Leaderboard(self, game_manager.red_team)
        self.red_column.grid(row=1, column=0, sticky="w", padx=150)
        self.red_column.configure(style="Red.TFrame")

        self.green_column = Leaderboard(self, game_manager.green_team)
        self.green_column.grid(row=1, column=1, sticky="e", padx=150)
        self.green_column.configure(style="Green.TFrame")

        self.event_window = EventWindow(self)
        self.event_window.grid(row=2, columnspan=3, padx=6, pady=6, sticky="s")
        self.create_f5_button()

        # Check for udp events every second
        self.after(UDP_REFRESH_RATE, self.process_udp)

    def create_f5_button(self):
        f5_button = ttk.Button(
            self, text="Return to main screen", command=self.switch_callback
        )
        f5_button.grid(row=0, column=1, sticky="e", padx=10)
        udp.action_thread.stop()

    def process_udp(self):
        has_started = False
        if len(udp.event_queue) > 0:
            from_id, to_id = udp.event_queue.pop()

            red_player = game_manager.red_team.players.get(from_id)
            red_hit = game_manager.red_team.players.get(to_id)
            green_player = game_manager.green_team.players.get(from_id)
            green_hit = game_manager.green_team.players.get(to_id)

            if from_id == 202 and to_id == 202 and not has_started:
                has_started = True
                self.event_window.add_log("[START] GAME HAS STARTED")

            if from_id == 221 and to_id == 221:
                self.event_window.add_log("[END] GAME HAS ENDED")
                # udp.action_thread.stop()

            # Check for friendly fire
            if udp.action_thread.is_alive():
                if red_player and red_hit or green_player and green_hit:
                    udp.broadcast_code(from_id)
                else:
                    udp.broadcast_code(to_id)

            if red_player:
                if to_id == GREEN_BASE:
                    red_player.add_points(100)
                    self.event_window.add_log(
                        f"Red Team: {red_player.name} hit the base! (+100)"
                    )
                    self.red_column.player_frames.get(from_id).show_base()
                elif red_hit:
                    red_player.decrease_points(10)
                    self.event_window.add_log(
                        f"Red Team: {red_player.name} hit {red_hit.name} (-10)"
                    )
                else:
                    red_player.add_points(10)
                    self.event_window.add_log(
                        f"Red Team: {red_player.name} hit {green_hit.name} (+10)"
                    )
                game_manager.adjust_leaderboard("Red")
                self.red_column.sort_leaderboard()

            if green_player:
                if to_id == RED_BASE:
                    green_player.add_points(100)
                    self.event_window.add_log(
                        f"Green Team: {green_player.name} hit the base! (+100)"
                    )
                    self.green_column.player_frames.get(from_id).show_base()
                elif green_hit:
                    green_player.decrease_points(10)
                    self.event_window.add_log(
                        f"Green Team: {green_player.name} hit {green_hit.name} (-10)"
                    )
                else:
                    green_player.add_points(10)
                    self.event_window.add_log(
                        f"Green Team: {green_player.name} hit {red_hit.name} (+10)"
                    )
                game_manager.adjust_leaderboard("Green")
                self.green_column.sort_leaderboard()

        self.after(UDP_REFRESH_RATE, self.process_udp)
