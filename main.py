from screens.splash_screen import Splash
from app import App

WINDOW_WIDTH = 1050
WINDOW_HEIGHT = 800

def main():
    splash = Splash()
    splash.root.mainloop()
    
    app = App("Laser Tag", (WINDOW_WIDTH, WINDOW_HEIGHT))
    app.mainloop()

if __name__ == "__main__":
    main()