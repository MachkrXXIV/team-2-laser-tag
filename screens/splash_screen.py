from tkinter import Tk, Label, Frame
from PIL import Image, ImageTk


class Splash:
    def __init__(self):
        # set up blank screen
        width = 1000
        height = 700
        self.root = Tk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width / 2)
        y_coordinate = (screen_height / 2) - (height / 2)

        # adjust where it pops up
        self.root.geometry("%dx%d+%d+%d" % (width, height, x_coordinate, y_coordinate))

        # remove the heading on top
        self.root.overrideredirect(1)

        Frame(self.root, width=427, height=241, bg="black").place(x=50, y=100)

        # add logo
        im = Image.open("images/logo.jpg")
        logo = im.resize((width, height))
        LOGO = ImageTk.PhotoImage(logo)

        # insert logo
        logo_label = Label(image=LOGO, bg="black")
        logo_label.place(x=0, y=0)

        logo_label.image = LOGO

        # Close the splash screen after 10 seconds of inactivity
        self.root.after(3000, self.close_splash)

    def close_splash(self):
        self.root.destroy()
