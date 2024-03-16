from Udp import Udp

def main():
    # Assuming player ID is 1 for testing purposes
    player_id = 1

    # Create an instance of the Udp class with the player ID
    udp_instance = Udp(player_id)

    # Wait for any broadcasts or messages
    # Note: You may need to add some form of loop to keep the program running
    # so that it can continue receiving data or waiting for broadcasts.

if __name__ == "__main__":
    main()
