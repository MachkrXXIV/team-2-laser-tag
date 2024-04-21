class Player:
    def __init__(self, id: int, name: str) -> None:
        self.__id = id
        self.__name = name
        self.__equipment_id = None
        self.__team = None
        self.__points = 0

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def equipment_id(self) -> int:
        return self.__equipment_id

    @property
    def team(self) -> str:
        return self.__team

    @team.setter
    def team(self, team: str) -> None:
        self.__team = team

    @property
    def points(self) -> int:
        return self.__points

    @property
    def equipment_id(self) -> int:
        return self.__equipment_id

    @equipment_id.setter
    def equipment_id(self, equipment_id):
        self.__equipment_id = equipment_id

    def add_points(self, points: int) -> None:
        self.__points += points

    def decrease_points(self, points: int) -> None:
        self.__points -= points

    def __str__(self) -> str:
        return (
            f"Player ID: {self.id} | "
            f"Equipment ID: {self.equipment_id} | "
            f"Codename: {self.name} | "
            f"Team: {self.team} | "
            f"Points: {self.points}"
        )
