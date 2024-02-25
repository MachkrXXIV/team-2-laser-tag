from splash_screen import Splash
import socket

LOCAL_IP = '127.0.0.1'
BROADCAST_PORT = 7500 #server
RECEIVING_PORT = 7501 #client
BUFFER_SIZE = 1024

class Udp:

    def __init__(self) -> None:
        self.__broadcast_port = BROADCAST_PORT
        self.__broadcast_socket = broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__broadcast_socket.bind(BROADCAST_PORT)
        self.__receive_port = RECEIVING_PORT
        self.__receive_socket = broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 

        # Countdown timer finishes, transmit code 202
        # self.broadcast_data('202', self.__broadcast_port)

        # # Example of receiving data and processing it
        # received_data = self.receive_data(self.__receive_port)
        # if received_data is not None:
        #     transmission_parts = received_data.split(':')

        #     if len(transmission_parts) == 2:
        #         transmitter_id, hit_id = map(int, transmission_parts)

        #         if transmitter_id == 53:
        #             # Red base scored
        #             # Process according to team color
        #             pass
        #         elif transmitter_id == 43:
        #             # Green base scored
        #             # Process according to team color
        #             pass
        #         else:
        #             # Player hit another player
        #             # Transmit their own equipment id
        #             self.broadcast_data(str(transmitter_id), self.__broadcast_port)

        #             if hit_id == 1:
        #                 self.broadcast_player_id()
        #     # Game ends, transmit code 221 three times
        # for _ in range(3):
        #     self.broadcast_data('221', self.__broadcast_port)

    def broadcast_data(self, data, port):
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcast_socket.sendto(data.encode(), ('<broadcast>', port))
        print("Broadcasting data right now......: ")
        print("Searching for equipment ID of", self.broadcast_player_id)
        
        broadcast_socket.close()
        
    def broadcast_equipment_id(self, equipment_id):
        self.__receive_socket.sendto(str(equipment_id).encode(), (LOCAL_IP, self.__broadcast_port))
        print(f"Broadcasting equipment id: {equipment_id}......: ")
        
    def receive_equipment_id(self, equipment_id):
        while str(equipment_id) != '202':
            received, address = self.__broadcast_socket.recvfrom(BUFFER_SIZE)
            print(f"Received equipment_id: {received.decode()}")
        


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
