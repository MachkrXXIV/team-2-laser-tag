from game.player import Player
from typing import Dict
from collections import defaultdict
# TODO change to defaultdict?

'''
- Max 15 players per team
'''
class Team:
    def __init__(self, team_name: str) -> None:
        self.__team_name: str = team_name
        self.__players: Dict[int ,Player]  = {} #{equipment_id: player}
        self.__points: int = 0
    
    @property
    def team_name(self):
        return self.__team_name
    
    @property 
    def players(self): # Use this to get the player with id
        return self.__players
    
    @property
    def points(self):
        return self.__points
    
    @points.setter
    def points(self, points: int):
        self.__points = points
    
    @property
    def team_size(self):
        return len(self.__players)
        
    def add_player_to_team(self, player: Player):
        if self.team_size >= 15:
            raise Exception("Team is already full with 15 players")
        player.team = self.team_name
        self.__players[player.equipment_id] = player
    
    def remove_player_from_team(self, player: Player):
        try:
            self.__players.pop(player.equipment_id)
        except KeyError:
            raise KeyError("Player not found in team")
        
    def clear_team(self):
        self.__players.clear()
    
    def sum_points(self):
        self.__points = sum([player.points for player in self.__players.values()])
    
    # Points can be negative
    def update_points(self, points: int):
        self.points += points
        
    def increment_player_points(self, equipment_id: int, points: int):
        self.__players[equipment_id].add_points(points=points)
        self.update_points(points=points)
        
    def decrement_player_points(self, equipment_id: int, points: int):
        self.__players[equipment_id].decrease_points(points=points)
        self.update_points(points=-points)
        
    def __str__(self) -> str:
        return f'''
        Team Name: {self.team_name}\n
        Team Size: {self.team_size}\n
        Total Points: {self.points}
    '''
       