#!/bin/bash
python3 - << END
from game.game_manager import game_manager
from game.player import Player
red1 = Player(1,"silly")
red1.equipment_id = 1
red2 = Player(2, "boy")
red2.equipment_id = 2
green1 = Player(3, "das")
green1.equipment_id = 3
green2 = Player(4, "morg")
green2.equipment_id = 4

game_manager.add_player_to_team(red1, "Red")
game_manager.add_player_to_team(red2, "Red")
game_manager.add_player_to_team(green1, "Green")
game_manager.add_player_to_team(green2, "Green")

game_manager.red_team.increment_player_points(1, 10)
game_manager.red_team.increment_player_points(2, 40)
game_manager.green_team.increment_player_points(3, 60)
game_manager.green_team.increment_player_points(3, 20)
game_manager.adjust_leaderboard("Red")
game_manager.adjust_leaderboard("Green")

print(game_manager.red_team)
for p in game_manager.red_team.players.values():
    print(p)
    
print(game_manager.green_team)
for p in game_manager.green_team.players.values():
    print(p)

print(game_manager)
END