import tkinter as tk
from tkinter import ttk

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

        self.create_team_frame("Red", 0)
        self.create_team_frame("Green", 1)

    def create_team_frame(self, team_color, column):
        team_frame = ttk.LabelFrame(self.root, style=f'{team_color}.TLabelframe')
        team_frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        ttk.Label(team_frame, text=f"{team_color} Team", font=('Helvetica',15,'bold')).grid(row=0, column=3, sticky="w", padx=5, pady=5, columnspan=2)
        self.create_player_entries(team_frame, team_color)


    def create_player_entries(self, parent_frame, team):
        ttk.Label(parent_frame, text="Player Names").grid(row=1, column=5, padx=5, pady=(10,0), sticky="w", columnspan=2) 
        ttk.Label(parent_frame, text="User ID".format(team)).grid(row=1, column=2, sticky="w", padx=5, pady=(5,0), columnspan=2)
        
        for i in range(1, 16):  # Assuming 5 players per team
            ttk.Label(parent_frame, text="{}: ".format(i)).grid(row=i+1, column=0, padx=5, pady=5, sticky="e")

            # player name
            entry = ttk.Entry(parent_frame, width=20)
            entry.grid(row=i+1, column=2, padx=5, pady=5, sticky="w")
        
            # user id
            entry_id = ttk.Entry(parent_frame, width=20)
            entry_id.grid(row=i+1, column=5, padx=5, pady=(10,0), sticky="w", columnspan=2)


        ttk.Button(parent_frame, text="Add Player", command=lambda: self.add_player(parent_frame)).grid(row=17, column=2, columnspan=5, pady=5)


    def add_player(self, parent_frame):
        player_names = []
        incomplete_entries = False

        for widget in parent_frame.winfo_children():
            if isinstance(widget, ttk.Entry):
                player_name = widget.get().strip() # get player name but remove unnecessary whitespace
                if player_name:
                    player_names.append(player_name)
                    print(widget.get())  # Here you can store the entered player names in your data structure
                else:
                    incomplete_entries = True

        if not player_names and incomplete_entries: # throws error if all filds are empty
            print("Error: Enter at least one player.")
        else:
            print("Player added successfully!")
    
    def show(self):
        self.root.mainloop() 
