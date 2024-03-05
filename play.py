import tkinter as tk
from tkinter import ttk
class Play(ttk.Frame): # This is just to test the switching, can be deleted later
    def __init__(self, parent, controller, database, udp):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.db = database
        self.udp = udp
        
        label = ttk.Label(self,text="is working")
        label.pack()
        self.create_text()
        
    def create_text(self):
        print("creating text")
        button = ttk.Button(self,text="click me", command=lambda: self.controller.show_frame("PlayerEntry"))
        button.pack()