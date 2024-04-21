import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import os
import winsound
from game.graceful_thread import GracefulThread
import time 
import asyncio

TIMER_WINDOW_WIDTH = 200
TIMER_WINDOW_HEIGHT = 100

class TimerWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=TIMER_WINDOW_WIDTH, height=TIMER_WINDOW_HEIGHT)
        self.parent = parent
        self.timer_label = ttk.Label(self, text="00:00", font=("Helvetica", 24))
        self.timer_label.pack(expand=True)

        self.music_thread = GracefulThread(target=self.play_music)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TimerWindow.TFrame", background="white")
        self.style.configure("TimerLabel.TLabel", foreground="black", background="white")

        self.configure(style="TimerWindow.TFrame")
        self.digit_images = [ImageTk.PhotoImage(Image.open(os.path.join("images", f"{i}.tif"))) for i in range(6)]
        self.music_thread.start()
        # time.sleep(10)
        # self.start_countdown_timer()
        # self.start_game_timer()
        

    def start_countdown_timer(self, count=5):
        if count >= 0:
            self.timer_label.config(image=self.digit_images[count])
            self.timer_label.after(2000, lambda: self.start_countdown_timer(count - 1))
        else:
            print("stops1")
            for img in self.digit_images:
                img.tkinter_image = ""
            self.timer_label.config(image="")
            del self.timer_label
            self.digit_images.clear()
            self.timer_label = ttk.Label(self, text="00:00", font=("Helvetica", 24))
            self.timer_label.pack(expand=True)
            

            print("Stops2")
            self.start_game_timer()
            print("Stops3")
        self.timer_label.destroy()

    def start_game_timer(self):
        total_seconds = 390  # 6 minutes and 30 seconds
        while total_seconds >= 0:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            time_string = f"{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_string)
            time.sleep(1)  # Wait for 1 second
            total_seconds -= 1


    def play_music(self):
        music_path = os.path.join("Tracks/", "Track08.wav")
        winsound.PlaySound(music_path, winsound.SND_FILENAME)

