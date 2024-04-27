import tkinter as tk
from tkinter import ttk, simpledialog
from game.database import Database
from screens.player_entry import PlayerEntry
from game.udp import udp


# The window of the game
class App(tk.Tk):
    def __init__(self, title: str, size: tuple[int, int]):
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])
        self.configure(background="black")

        # instantiate udp and database
        self.db = Database()

        # Frame stack
        container = ttk.Frame(self)
        container.pack(side="top", fill="y", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames: dict[str, ttk.Frame] = {}

        # Instantiate frames
        playerEntry = PlayerEntry(parent=container, controller=self, database=self.db)
        playerEntry.grid(row=0, column=0, sticky="nsew")
        self.frames["PlayerEntry"] = playerEntry

        self.show_frame("PlayerEntry")

    # call this method in children component to switch between frames
    def show_frame(self, page_name: str):
        print("SWITCHING TO", page_name)
        frame: ttk.Frame = self.frames[page_name]
        frame.tkraise()
