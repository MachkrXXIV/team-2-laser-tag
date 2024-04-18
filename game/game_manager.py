from .team import Team
from .player import Player
# from .udp import Udp
"""
GameManager follows a singleton pattern
- import in classes than need game logic by importing game_manager
- provide team name to specific which team to modify
- TODO maybe add timers here?
- TODO maybe add udp logic here?
- !!!Kalaya can use this for action display
"""
class GameManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Ensure initialization only happens once
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.__red_team = Team("Red")
        self.__green_team = Team("Green")
        # self.__udp = Udp()
        
    '''
    - To add points to specific player, use their equipment ID as keys
    - ex: player with equipment_id 4 from red_team gets 10 points -> 
        game_manager.red_team.increment_player_points(4, 10)
    '''
    @property
    def red_team(self):
        return self.__red_team
    
    @property
    def green_team(self):
        return self.__green_team
        
    def add_player_to_team(self, player: Player, team_name: str) -> None:
        if team_name == "Red":
            self.__red_team.add_player_to_team(player)
        elif team_name == "Green":
            self.__green_team.add_player_to_team(player)
        else:
            raise Exception("ERROR: invalid team name you are trying to add player to")
    
    def remove_player_from_team(self, player: Player, team_name: str) -> None:
        if team_name == "Red":
            self.__red_team.remove_player_from_team(player)
        elif team_name == "Green":
            self.__green_team.remove_player_from_team(player)
        else:
            raise Exception("ERROR: invalid team name you are trying to remove a player from")
        
    def clear_team(self, team_name: str) -> None:
        if team_name == "Red":
            self.__red_team.clear_team()
        elif team_name == "Green":
            self.__green_team.clear_team()
        else:
            raise Exception("ERROR: invalid team name you are trying clear")
        
    def reset_game_manager(self):
        del self.__red_team
        del self.__green_team
        self.__red_team = Team("Red")
        self.__green_team = Team("Green")
        
        
#Import this into to other files that need game logic
game_manager = GameManager()