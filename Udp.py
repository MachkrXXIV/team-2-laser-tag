from splash_screen import Splash
import socket

class Udp:

    def __init__(self) -> None:
        self.__broadcast_port = 7500
        self.__receive_port = 7501

        # Countdown timer finishes, transmit code 202
        self.broadcast_data('202', self.broadcast_port)

        # Example of receiving data and processing it
        received_data = self.receive_data(self.receive_port)
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
                self.broadcast_data(str(transmitter_id), self.broadcast_port)

        # Game ends, transmit code 221 three times
        for _ in range(3):
            self.broadcast_data('221', self.broadcast_port)

    def broadcast_data(data, port):
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcast_socket.sendto(data.encode(), ('<broadcast>', port))
        broadcast_socket.close()


    def receive_data(port):
        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receive_socket.bind(('', port))
        data, _ = receive_socket.recvfrom(1024)
        receive_socket.close()
        return data.decode()

    # def main(player_id):
    #     splash = Splash()
    #     splash.root.mainloop()


    
