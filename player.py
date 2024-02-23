class Player:
    def __init__(self, id: int, name: str) -> None:
        self.__id = id
        self.__name = name
        self.__equipment_id = None
    
    def get_id(self)->int:
        return self.__id
    
    def get_name(self)->str:
        return self.__name
    
    def get_equipment_id(self)->int:
        return self.__equipment_id

    def set_equipment_id(self, equipment_id):
        self.__equipment_id = equipment_id

    # creates readable print
    def __str__(self) -> str:
        return f'Player ID: {self.__id} Equipment ID: {self.__equipment_id} Codename: {self.__name}'
