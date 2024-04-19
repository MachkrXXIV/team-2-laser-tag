import socket
import time
import threading

LOCAL_IP = '127.0.0.1'
BROADCAST_PORT = 7500 #server
RECEIVING_PORT = 7501 #client
RECEIVING_ADDR = (LOCAL_IP, RECEIVING_PORT)
START_CODE = '202'
END_CODE = '221'
BUFFER_SIZE = 1024
RED_BASE = '53'
GREEN_BASE = '43'
'''
UDP class follows the singleton method
- import the udp instance for screens that require udp functionality
'''
class Udp:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        '''
        In order to receive UDP transmissions we must start the threads
        ex: udp.entry_thread.start()
        '''
        # Ensure initialization only happens once
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.__broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__receive_socket.bind(RECEIVING_ADDR)
        self.__entry_thread = threading.Thread(target=self._receive_equipment_id)
        self.__action_thread = threading.Thread(target=self._receive_game_events)

    @property
    def broadcast_socket(self):
        return self.__broadcast_socket
    
    @property
    def entry_thread(self):
        return self.__entry_thread
    
    @property
    def action_thread(self):
        return self.__action_thread
        
    def broadcast_equipment_id(self, equipment_id: int) -> None:
        self.__broadcast_socket.sendto(str(equipment_id).encode(), RECEIVING_ADDR)
        print(f"Broadcasting equipment id: {equipment_id}......: ")
    
    def broadcast_hit_event(self, from_id: int, to_id: int) -> None:
        '''
        Sends equipment_id of player hit
        '''
        self.__broadcast_socket.sendto(str(f"{from_id}:{to_id}").encode(), RECEIVING_ADDR)
    
    def broadcast_end(self) -> None:
        for i in range(3):
            self.__broadcast_socket.sendto(END_CODE.encode(), RECEIVING_ADDR)
        self.__broadcast_socket.close()
    
    def _receive_equipment_id(self) -> None:
        received = ''
        while True:
            received, _ = self.__receive_socket.recvfrom(BUFFER_SIZE)
            message = received.decode()
            if message != START_CODE:
                print(f"Received equipment_id: {received.decode()}")
                break
    
    def _receive_game_events(self) -> None:
        received = ''
        while True:
            received, _ = self.__receive_socket.recvfrom(BUFFER_SIZE)
            message = received.decode()
            
            if message == END_CODE:
                self.__receive_socket.close()
                break
            
            if ":" in message:
                from_id, to_id = message.split(":")[0], message.split(":")[1]
                return from_id, to_id
        
udp = Udp()