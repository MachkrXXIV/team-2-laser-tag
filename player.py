class Player:
    def __init__(self, id: int, name: str) -> None:
        self.__id = id
        self.__name = name
        self.__equipment_id = None
        self.__team = None
        self.__points = 0
    
    def get_id(self)->int:
        return self.__id
    
    def get_name(self)->str:
        return self.__name
    
    def get_equipment_id(self)->int:
        return self.__equipment_id
    
    def get_team(self)->str:
        return self.__team

    def get_points(self)->int:
        return self.__points

    def set_equipment_id(self, equipment_id):
        self.__equipment_id = equipment_id

    def set_team(self, team: str)->None:
        self.__team = team
    
    def add_points(self, points)->None:
        self.__points += points
        
    def decrease_points(self, points)->None:
        self.__points -= points

    # creates readable print
    def __str__(self) -> str:
        return f'Player ID: {self.__id} Equipment ID: {self.__equipment_id} Codename: {self.__name}'
