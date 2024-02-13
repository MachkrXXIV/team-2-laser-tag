from splash_screen import Splash

def main():
    splash = Splash()
    splash.root.mainloop()

    # After splash screen, show player entry
    player_entry = PlayerEntry()
    player_entry.show()

if __name__ == "__main__":
    main()