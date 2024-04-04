from screens.splash_screen import Splash
from app import App

def main():
    splash = Splash()
    splash.root.mainloop()
    
    app = App("Laser Tag", (1050,800))
    app.mainloop()

if __name__ == "__main__":
    main()