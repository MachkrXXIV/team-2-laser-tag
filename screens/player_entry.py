import tkinter as tk
import tkinter.ttk as ttk
import time
from tkinter import simpledialog
from game.database import Database
from game.player import Player
from game.udp import Udp
from screens.action_display import ActionDisplay
from threading import Timer
from typing import TYPE_CHECKING
from game.game_manager import game_manager

if TYPE_CHECKING:
    from app import App

class PlayerEntry(ttk.Frame):
    def __init__(self, parent: ttk.Frame, controller: 'App', database: Database, udp: Udp):
        super().__init__(parent)
        
        # Inject dependencies
        self.parent = parent
        self.controller = controller
        self.db = database
        self.udp = udp
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Red.TLabelframe', background='#800000', bordercolor= ' ')  # Darker red
        self.style.configure('Green.TLabelframe', background='green', bordercolor = ' ')

        self.player_entries = {'Red': {}, 'Green': {}} # Changed to dict 
        self.row_counters = {'Red': 2, 'Green': 2}  # Initial row counters for each team

        self.create_team_frame("Red", 0)
        self.create_team_frame("Green", 1)        

        self.create_buttons()
        self.controller.bind('<KeyPress>', self.on_key_press)          

    def create_team_frame(self, team_color: str, column: int):
        team_frame = ttk.LabelFrame(self, style=f'{team_color}.TLabelframe')
        team_frame.grid(row=0, column=column, padx=5, pady=10, sticky="nsew")
        ttk.Label(team_frame, text=f"{team_color} Team", font=('Helvetica',15,'bold')).grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.create_player_entries(team_frame, team_color)

    def create_player_entries(self, parent_frame: tk.LabelFrame, team: str):
        ttk.Label(parent_frame, text="User ID".format(team)).grid(row=1, column=3, padx=5, pady=(5, 0), sticky = "w", columnspan=2)
        ttk.Label(parent_frame, text="Player Names").grid(row=1, column=5, padx=5, pady=(5, 0), sticky="w", columnspan=2)

        def add_player(team):
            def inner_add_player():
                player_id = simpledialog.askinteger("ID", "Enter Player ID")

                # check if player_id is negative
                if player_id is not None and player_id >= 0:
                    player = self.db.get_player(player_id)
                    print(player_id)

                    # if player not found ask for name
                    if not player:
                        player_name = simpledialog.askstring("Name", "Enter Player name")
                        self.db.add_player(player_id, player_name)
                        player = self.db.get_player(player_id)
                        
                    equipment_id = simpledialog.askinteger("Equipment ID", "Enter Equipment ID")
                    
                    self.udp.broadcast_equipment_id(equipment_id)
                    player.equipment_id = equipment_id

                    user_id_entry = ttk.Label(parent_frame, text=player.id, state='readonly')
                    user_id_entry.grid(row=self.row_counters[team], column=3, sticky="w", padx=5, pady=5, columnspan=2)
                    
                    player_name_entry = ttk.Label(parent_frame, text=player.name, state='readonly')
                    player_name_entry.grid(row=self.row_counters[team], column=5, padx=5, pady=5, columnspan=2)     

                    self.player_entries[team][player_id] = (user_id_entry, player_name_entry)

                    print(f"Adding player {player} to team: ", team)
                    self.row_counters[team] += 1
                    game_manager.add_player_to_team(player=player, team_name=team)
                else:
                    tk.messagebox.showerror("Error", "Player ID cannot be negative")
            return inner_add_player
        
        ttk.Button(parent_frame, text="Add Player", command=add_player(team)).grid(row=17, column=2, columnspan=5, pady=5)

    def create_buttons(self):
        # buttons
        buttons = {
            'F1': '      F1\nEdit Game',
            'F2': '             F2\nGame Parameters',
            'F3': '       F3\nStart Game',
            'F5': '              F5\nPre-Entered Games',
            'F7': ' F7\n',
            'F8': '        F8\nView Game',
            'F10': '     F10\nFlick Sync',
            'F12': '      F12\nClear Game'
        }

        button_frame = tk.Frame(self, bg="#7F886E")
        button_frame.grid(row=10, column=0, columnspan=2, sticky="s", padx=10, pady=10)

        for idx, (key, value) in enumerate(buttons.items()):
            ttk.Button(button_frame, text=value, command=lambda k=key: self.on_button_press(k)).grid(row=0, column=idx, padx=5, pady=5, sticky="w")
    
    def switch_to_player_entry(self):
        # Logic to switch back to the player entry screen
        self.destroy()  # Destroy the action display frame
        # Re-create the player entry screen
        player_entry_screen = PlayerEntry(self.parent, self.controller, self.db, self.udp)
        player_entry_screen.grid(row=0, column=0, sticky="nsew")
    
    # Handles UI button events
    def on_button_press(self, key: str):
        if key == 'F3':
            action_display = ActionDisplay(self.parent, self.controller, self.player_entries, self.switch_to_player_entry)
            action_display.grid(row=0, column=0, sticky="nsew")
        elif key == 'F12':
            self.clear_player_entries()
    
    # Handles keyboard events
    def on_key_press(self, event: tk.Event):
        if event.keysym == 'F3':
            action_display = ActionDisplay(self.parent, self.controller, self.player_entries, self.switch_to_player_entry)
            action_display.grid(row=0, column=0, sticky="nsew")
        elif event.keysym == 'F12':
            self.clear_player_entries()

    # TODO: incorporate new team logic 
    def clear_player_entries(self):
        for team, entries in self.player_entries.items():  
            for player_id, (user_id_entry, player_name_entry) in entries.items():
                user_id_entry.config(text= '')
                player_name_entry.config(text= '')
                print("Player deleted ...")
            game_manager.clear_team(team)
           # ttk.Button(button_frame, text = value).grid(row=0, column = idx, padx =5, pady = 5, sticky = "w")
