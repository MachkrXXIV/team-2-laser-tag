import tkinter.ttk as ttk
from typing import List

EVENT_WINDOW_WIDTH = 600
EVENT_WINDOW_HEIGHT = 400
EVENT_LOG_WIDTH = 600

class EventLog(ttk.Label):
    def __init__(self, event_window: ttk.Frame, log: str):
        super().__init__(event_window, width=EVENT_LOG_WIDTH, text=log)
        self.pack(side='top', fill='both')
        self.configure(style="EventLog.TLabel")

class EventWindow(ttk.Frame):
    def __init__(self, parent: ttk.Frame):
        super().__init__(parent, width=EVENT_WINDOW_WIDTH, height=EVENT_WINDOW_HEIGHT)
        self.logs: List[EventLog] = []
        # self.pack(side='bottom', fill='none')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("EventWindow.TFrame", background="black")
        self.style.configure("EventLog.TLabel", foreground="white", background="black")
        self.configure(style="EventWindow.TFrame")
        
        for i in range(5):
            self.add_log("This works!")
    
    def add_log(self, log: str):
        event_log = EventLog(self,log=log)
        self.logs.append(event_log)
        
    def clear_window(self):
        for log in self.logs:
            log.destroy()
        self.logs = []
            