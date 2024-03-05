from splash_screen import Splash
from player_entry import PlayerEntry
from app import App

def main():
    splash = Splash()
    splash.root.mainloop()
    
    app = App("Laser Tag", (1050,800))
    app.mainloop()

if __name__ == "__main__":
    main()