from player import Player
from typing import List
class Team:
    def __init__(self, team_name: str) -> None:
        self.team_name: str = team_name
        self.players: List[Player] = []
        self.points: int = 0
        
    def add_player_to_team(self, player: Player):
        self.players.append(player)
    
    def remove_player_from_team(self, player):
        self.players.remove(player)
        
    def clear_team(self):
        self.players = []
        
    def get_points(self):
        return self.points
    
    def update_points(self):
        self.points = sum([player.get_points() for player in self.players])
        
        