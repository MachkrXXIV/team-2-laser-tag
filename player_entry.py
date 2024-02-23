import tkinter as tk
from tkinter import ttk
from database import Database

class PlayerEntry:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Player Entry")
        self.root.geometry("1000x900")  # Adjusted width
        self.root.configure(bg = "black") # sets bg to black 

        # Define column weights to make the columns fit the window
        self.root.columnconfigure(0, weight=5)  # Set higher weight for column 0
        self.root.columnconfigure(1, weight=5)  # Set higher weight for column 1

        self.style = ttk.Style()
        self.style.configure('Red.TLabelframe', background='#800000')  # Darker red
        self.style.configure('Green.TLabelframe', background='green')

        self.player_counts = {'Red': 1, 'Green': 1}
        self.player_entries = []

        self.db = Database()
        self.udp = Udp()

        self.create_team_frame("Red", 0)
        self.create_team_frame("Green", 1)        

        self.create_buttons()        

    def create_team_frame(self, team_color, column):
        team_frame = ttk.LabelFrame(self.root, style=f'{team_color}.TLabelframe', borderwidth = 0)
        team_frame.grid(row=0, column=column, padx=5, pady=10, sticky="nsew")
        ttk.Label(team_frame, text=f"{team_color} Team", font=('Helvetica',15,'bold')).grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.create_player_entries(team_frame, team_color)

    def create_player_entries(self, parent_frame, team):
        ttk.Label(parent_frame, text="User ID".format(team)).grid(row=1, column=2, sticky="w", padx=5, pady=(5,0), columnspan=2)
        ttk.Label(parent_frame, text="Player Names").grid(row=1, column=5, padx=5, pady=(5,0), sticky="w", columnspan=2) 
        
        def add_player():
            print ("Adding player to team: ", team)

            # Create new user id fields
            entry = ttk.Entry(parent_frame, width=20)
            entry.grid(row=len(self.player_entries) + 2, column=2, padx=5, pady=5, sticky="w")
            
            # create new player entry fields
            entry_id = ttk.Entry(parent_frame, width=20)
            entry_id.grid(row=len(self.player_entries) + 2, column=5, padx=5, pady=5, sticky="w")

            player_number = self.player_counts[team]  # Get the current player count for the team
            ttk.Label(parent_frame, text="{}: ".format(player_number)).grid(row=len(self.player_entries) + 2, column=0, padx=5, pady=5, sticky="e")  
            print(self.player_counts[team])
            self.player_counts[team] += 1  # Increment the player count for the team

            print(self.player_counts[team])

            self.player_entries.append((entry, entry_id))

        add_player()

        ttk.Button(parent_frame, text="Add Player", command=add_player).grid(row=17, column=2, columnspan=5, pady=5)


    def create_buttons(self):
        # buttons
        buttons = {
            'F1': '      F1\nEdit Game',
            'F2': '             F2\nGame Parameters',
            'F3': '       F3\nStart Game',
            'F5': '             F5\nPre-Entered Games',
            'F7': ' F7\n',
            'F8': '        F8\nView Game',
            'F10': '     F10\nFlick Sync',
            'F12': '      F12\nClear Game'
        }

        button_frame = tk.Frame(self.root, background = "#7F886E")
        button_frame.grid(row = 10, column = 0, columnspan = 2, sticky = "s", padx = 10, pady = 10)

        for idx, (key, value) in enumerate(buttons.items()):
            ttk.Button(button_frame, text = value).grid(row=0, column = idx, padx =5, pady = 5, sticky = "w")
    
    def show(self):
        self.root.mainloop() 