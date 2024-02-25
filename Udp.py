from splash_screen import Splash
import socket

class Udp:

    def __init__(self, player_id) -> None:
        self.__broadcast_port = 7500
        self.__receive_port = 7501
        self.player_id = player_id

        # Countdown timer finishes, transmit code 202
        self.broadcast_data('202', self.__broadcast_port)

        # Example of receiving data and processing it
        received_data = self.receive_data(self.__receive_port)
        if received_data is not None:
            transmission_parts = received_data.split(':')

            if len(transmission_parts) == 2:
                transmitter_id, hit_id = map(int, transmission_parts)

                if transmitter_id == 53:
                    # Red base scored
                    # Process according to team color
                    pass
                elif transmitter_id == 43:
                    # Green base scored
                    # Process according to team color
                    pass
                else:
                    # Player hit another player
                    # Transmit their own equipment id
                    self.broadcast_data(str(transmitter_id), self.__broadcast_port)

                    if hit_id == 1:
                        self.broadcast_player_id()
            # Game ends, transmit code 221 three times
        for _ in range(3):
            self.broadcast_data('221', self.__broadcast_port)

    def broadcast_data(self, data, port):
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcast_socket.sendto(data.encode(), ('<broadcast>', port))
        print("Broadcasting data right now......: ")
        print("Searching for equipment ID of", self.broadcast_player_id)
        
        broadcast_socket.close()


    def receive_data(self, port):
        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receive_socket.bind(('', port))
        receive_socket.settimeout(10)
        try:
            data, _ = receive_socket.recvfrom(1024)
        except socket.timeout:
            data = None
        finally:
            receive_socket.close()
        return data.decode() if data else None
    
    def broadcast_player_id(self):
        self.broadcast_data(str(self.player_id), self.__broadcast_port)

    # def main(player_id):
    #     splash = Splash()
    #     splash.root.mainloop()

if __name__ == "__main__":
    # Assuming player ID is 1 for testing purposes
    player_id = 1

    # Create an instance of the Udp class with the player ID
    udp_instance = Udp(player_id)

    # Here you can continue with the rest of your program logic


    
