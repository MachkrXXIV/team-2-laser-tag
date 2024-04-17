import socket
import time
from .game_manager import game_manager

LOCAL_IP = '127.0.0.1'
BROADCAST_PORT = 7500 #server
RECEIVING_PORT = 7501 #client
RECEIVING_ADDR = (LOCAL_IP, RECEIVING_PORT)
BUFFER_SIZE = 1024
RED_BASE = 53
GREEN_BASE = 43

class Udp:

    def __init__(self) -> None:
        self.__broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__receive_socket.bind(RECEIVING_ADDR)

    @property
    def broadcast_socket(self):
        return self.__broadcast_socket
        
    def broadcast_equipment_id(self, equipment_id):
        self.__broadcast_socket.sendto(str(equipment_id).encode(), RECEIVING_ADDR)
        print(f"Broadcasting equipment id: {equipment_id}......: ")
    
    def broadcast_hit_events(self, from_id, to_id):
        self.__broadcast_socket.sendto(str(f"{from_id}:{to_id}".encode(), RECEIVING_ADDR))
    
    def broadcast_end(self):
        for i in range(3):
            self.__broadcast_socket.sendto('221'.encode(), RECEIVING_ADDR)
        self.__broadcast_socket.close()
    
    def receive_equipment_id(self):
        received = ''
        while True:
            received, _ = self.__receive_socket.recvfrom(BUFFER_SIZE)
            message = received.decode()
            if message != '202':
                print(f"Received equipment_id: {received.decode()}")
                break
    
    def receive_game_events(self):
        received = ''
        while True:
            received, _ = self.__receive_socket.recvfrom(BUFFER_SIZE)
            message = received.decode()
            
            if message == '221':
                self.__receive_socket.close()
                break
            
            if ":" in message:
                from_id, to_id = message.split(":")[0], message.split(":")[1]
                return from_id, to_id
