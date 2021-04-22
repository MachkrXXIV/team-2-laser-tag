import tkinter.ttk as ttk
from typing import List

EVENT_WINDOW_WIDTH = 800
EVENT_WINDOW_HEIGHT = 200
EVENT_LOG_WIDTH = 800


class EventLog(ttk.Label):
    def __init__(self, event_window: ttk.Frame, log: str):
        super().__init__(event_window, width=EVENT_LOG_WIDTH, text=log)
        self.pack(side="top", fill="y", expand=True, anchor="w", padx=10, pady=5)
        self.configure(style="EventLog.TLabel")


class EventWindow(ttk.Frame):
    def __init__(self, parent: ttk.Frame):
        super().__init__(parent, width=EVENT_WINDOW_WIDTH, height=EVENT_WINDOW_HEIGHT)
        self.logs: List[EventLog] = []
        # self.pack(side='bottom', fill='none')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.pack_propagate(False)

        # Create styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("EventWindow.TFrame", background="black")
        self.style.configure("EventLog.TLabel", foreground="white", background="black")
        self.configure(style="EventWindow.TFrame", padding=10)

    def add_log(self, log: str):
        if len(self.logs) > 4:
            self.logs[0].destroy()
            self.logs.pop(0)
            # self.clear_window()
        event_log = EventLog(self, log=log)
        self.logs.append(event_log)

    def clear_window(self):
        for log in self.logs:
            log.destroy()
        self.logs = []
