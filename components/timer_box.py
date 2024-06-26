import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import os
import pygame
from game.graceful_thread import GracefulThread
import time
from game.udp import udp
import random

TIMER_WINDOW_WIDTH = 200
TIMER_WINDOW_HEIGHT = 200
NUM_IMAGES = 31
DELAY = 8
COUNTDOWN = 8


class TimerWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=TIMER_WINDOW_WIDTH, height=TIMER_WINDOW_HEIGHT)
        self.parent = parent
        self.timer_label = ttk.Label(self, text="00:00", font=("Helvetica", 24))
        self.timer_label.pack(expand=True)
        pygame.mixer.init()

        self.music_thread = GracefulThread(target=self.play_music)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TimerWindow.TFrame", background="white")
        self.style.configure(
            "TimerLabel.TLabel", foreground="black", background="white"
        )

        self.configure(style="TimerWindow.TFrame")
        self.digit_images = [
            ImageTk.PhotoImage(Image.open(os.path.join("images", f"{i}.tif")))
            for i in range(NUM_IMAGES)
        ]
        self.start_countdown_timer()

    def start_countdown_timer(self, count=COUNTDOWN):
        if count >= 0:
            if count == DELAY and not self.music_thread.is_alive():
                self.music_thread.start()
            self.timer_label.config(image=self.digit_images[count])
            self.timer_label.after(2000, lambda: self.start_countdown_timer(count - 1))
        else:

            self.timer_label.config(image="")

            self.timer_label.destroy()
            self.timer_label = ttk.Label(self, text="06:00", font=("Helvetica", 24))
            self.timer_label.pack(expand=True)

            self.start_game_timer(360)
            udp.broadcast_code(202)

    def start_game_timer(self, total_seconds):
        if total_seconds >= 0:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            time_string = f"{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_string)
            self.after(1000, lambda: self.start_game_timer(total_seconds - 1))
        else:
            print("[BROADCASTING] END")
            udp.broadcast_end()

    # def play_music(self):
    #     music_path = os.path.join("Tracks/", "Track08.wav")
    #     pygame.mixer.music.load(music_path)
    #     pygame.mixer.music.play()

    def play_music(self):
        tracks_dir = "Tracks/"
        tracks = os.listdir(tracks_dir)
        track_file = random.choice(tracks)
        print("Playing track:", track_file)  # Print the name of the track being played
        music_path = os.path.join(tracks_dir, track_file)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
