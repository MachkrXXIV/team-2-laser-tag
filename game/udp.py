import socket
import time
import threading
from typing import List, Tuple
from .graceful_thread import GracefulThread

LOCAL_IP = "127.0.0.1"
BROADCAST_PORT = 7500  # server
RECEIVING_PORT = 7501  # client
BROADCASTING_ADDR = (LOCAL_IP, BROADCAST_PORT)
RECEIVING_ADDR = (LOCAL_IP, RECEIVING_PORT)
START_CODE = 202
END_CODE = 221
BUFFER_SIZE = 1024
RED_BASE = 53
GREEN_BASE = 43


class Udp:
    """UDP class follows the singleton pattern
    - import the udp instance for screens that require udp functionality
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        In order to receive UDP transmissions we must start the threads
        ex: udp.entry_thread.start()
        """
        # Ensure initialization only happens once
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self.__broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__receive_socket.bind(RECEIVING_ADDR)
        self.__entry_thread = GracefulThread(target=self._receive_equipment_id)
        self.__action_thread = GracefulThread(target=self._receive_game_events)
        self.__event_queue: List[Tuple[int, int]] = []

    @property
    def broadcast_socket(self):
        return self.__broadcast_socket

    @property
    def entry_thread(self):
        return self.__entry_thread

    @property
    def action_thread(self):
        return self.__action_thread

    def start_thread(self, thread_name: str):
        """Enter thread_name as 'entry' or 'action' to start the respective thread"""
        if thread_name == "entry":
            if self.__entry_thread.is_alive():
                self.__entry_thread.stop()
                self.__entry_thread = GracefulThread(target=self._receive_equipment_id)
                return
            self.__entry_thread.start()
        elif thread_name == "action":
            if self.__action_thread.is_alive():
                self.__action_thread.stop()
                self.__entry_thread = GracefulThread(target=self._receive_game_events)
                return
            self.__action_thread.start()

    def broadcast_code(self, code: int) -> None:
        self.__broadcast_socket.sendto(str(code).encode(), BROADCASTING_ADDR)

        if code == START_CODE:
            print(f"[BROADCASTING] Game Start!")
            return

        print(f"[BROADCASTING] code: {code}......")

    def broadcast_hit_event(self, from_id: int, to_id: int) -> None:
        """Sends in message to UDP socket in form of
        {FROM_PLAYER}:{TO_PLAYER} via their equipment id
        """
        self.__broadcast_socket.sendto(
            str(f"{from_id}:{to_id}").encode(), BROADCASTING_ADDR
        )

    def broadcast_end(self) -> None:
        for i in range(3):
            self.__broadcast_socket.sendto(END_CODE.encode(), BROADCASTING_ADDR)
        self.__broadcast_socket.close()

    def process_events(self) -> Tuple[int, int]:
        if self.__event_queue:
            return self.__event_queue.pop(0)
        return None

    def _receive_equipment_id(self) -> None:
        received = ""
        while True:
            received, _ = self.__receive_socket.recvfrom(BUFFER_SIZE)
            message = received.decode()
            if message != START_CODE:
                print(f"[RECEIVED] equipment_id: {received.decode()}")
                break

    def _receive_game_events(self) -> None:
        received = ""
        while True:
            received, _ = self.__receive_socket.recvfrom(BUFFER_SIZE)
            message = received.decode()

            if message == END_CODE:
                self.__receive_socket.close()
                break

            if ":" in message:
                from_id, to_id = message.split(":")[0], message.split(":")[1]
                if to_id == str(RED_BASE):
                    print(f"[RECEIVED]: Red Base Hit")

                if to_id == str(RED_BASE):
                    print(f"[RECEIVED]: Green Base Hit")

                print(f"[RECEIVED]: player: {from_id} hit player: {to_id}")
                self.__event_queue.append((from_id, to_id))


udp = Udp()
