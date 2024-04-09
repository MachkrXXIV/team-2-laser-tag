from game.player import Player
from typing import List
class Team:
    def __init__(self, team_name: str) -> None:
        self.__team_name: str = team_name
        self.__players: List[Player] = [] # Max 15 players per team
        self.__points: int = 0
    
    @property
    def team_name(self):
        return self.__team_name
    
    @property
    def points(self):
        return self.__points
    
    @property
    def team_size(self):
        return len(self.__players)
        
    def add_player_to_team(self, player: Player):
        if len(self.__players) >= 15:
            raise Exception("Team is already full with 15 players")
        self.__players.append(player)
    
    def remove_player_from_team(self, player: Player):
        self.__players.remove(player)
        
    def clear_team(self):
        self.__players = []
    
    def update_points(self):
        self.__points = sum([player.points for player in self.__players])
        
    def __str__(self) -> str:
        return f'''
        Team Name: {self.team_name}\n
        Team Size: {self.team_size}\n
        Total Points: {self.points}
    '''
       