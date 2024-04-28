from .team import Team
from .player import Player
from queue import PriorityQueue
from game.graceful_thread import GracefulThread

TEAM_PLAYERS_MAX = 15


class GameManager:
    """GameManager follows a singleton pattern
    - import in classes than need game logic by importing game_manager
    - provide team name to specific which team to modify
    - TODO maybe add timers here?
    - TODO maybe add udp logic here?
    - !!!Kalaya can use this for action display
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Ensure initialization only happens once
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self.__red_team = Team("Red")
        self.__green_team = Team("Green")

        # for i in range(5):  # For Testing purposes
        #     red_player = Player(i, f"red{i}")
        #     red_player.equipment_id = i
        #     green_player = Player(i + 6, f"green{i+6}")
        #     green_player.equipment_id = i + 6
        #     self.__red_team.add_player_to_team(red_player)
        #     self.__green_team.add_player_to_team(green_player)

        self.__red_leaderboard = PriorityQueue(
            TEAM_PLAYERS_MAX
        )  # (score, equipment_id, name)
        self.__green_leaderboard = PriorityQueue(TEAM_PLAYERS_MAX)

        # Adding players to the leaderboard with their scores as priority
        for player in self.red_team.players.values():
            self.__red_leaderboard.put(
                (-player.points, player.equipment_id, player.name)
            )

        for player in self.green_team.players.values():
            self.__green_leaderboard.put(
                (-player.points, player.equipment_id, player.name)
            )

    """
    - To add points to specific player, use their equipment ID as keys
    - ex: player with equipment_id 4 from red_team gets 10 points -> 
        game_manager.red_team.increment_player_points(4, 10)
    """

    @property
    def red_team(self):
        return self.__red_team

    @property
    def green_team(self):
        return self.__green_team

    @property
    def red_leaderboard(self):
        return self.__red_leaderboard

    @property
    def green_leaderboard(self):
        return self.__green_leaderboard

    def add_player_to_team(self, player: Player, team_name: str) -> None:
        if team_name == "Red":
            self.__red_team.add_player_to_team(player)
        elif team_name == "Green":
            self.__green_team.add_player_to_team(player)
        else:
            raise Exception(
                "[ERROR]: invalid team name you are trying to add player to"
            )

    def remove_player_from_team(self, player: Player, team_name: str) -> None:
        if team_name == "Red":
            self.__red_team.remove_player_from_team(player)
        elif team_name == "Green":
            self.__green_team.remove_player_from_team(player)
        else:
            raise Exception(
                "[ERROR]: invalid team name you are trying to remove a player from"
            )

    def clear_team(self, team_name: str) -> None:
        if team_name == "Red":
            self.__red_team.clear_team()
        elif team_name == "Green":
            self.__green_team.clear_team()
        else:
            raise Exception("[ERROR]: invalid team name you are trying clear")

    def reset_game_manager(self) -> None:
        del self.__red_team
        del self.__green_team
        self.__red_team = Team("Red")
        self.__green_team = Team("Green")

    def get_winning_team(self) -> Team:
        if self.__red_team.points > self.__green_team.points:
            return self.__red_team
        elif self.__red_team.points < self.__green_team.points:
            return self.__green_team
        else:
            return None

    def adjust_leaderboard(self, team_name: str) -> None:
        """
        This function reorganizes the priority queue and should be called whenever
        a player's points is modified
        """
        new_leaderboard = PriorityQueue(TEAM_PLAYERS_MAX)
        if team_name == "Red":
            for player in self.red_team.players.values():
                new_leaderboard.put((-player.points, player.equipment_id, player.name))
                self.__red_leaderboard = new_leaderboard
        elif team_name == "Green":
            for player in self.green_team.players.values():
                new_leaderboard.put((-player.points, player.equipment_id, player.name))
                self.__green_leaderboard = new_leaderboard
        else:
            raise Exception("[ERROR]: with leaderboard adjustment")

    def __str__(self) -> str:
        """
        By default the priority queue is a minheap so we need to store with negative values to be maxheap
        - This function prints the reverted version for debugging purposes
        """
        red_leaderboard = "\n".join(
            str((-score, equipment_id, player_name))
            for score, equipment_id, player_name in self.__red_leaderboard.queue
        )
        green_leaderboard = "\n".join(
            str((-score, equipment_id, player_name))
            for score, equipment_id, player_name in self.__green_leaderboard.queue
        )

        return (
            "Red Team\n"
            "---------\n"
            f"{red_leaderboard}\n"
            "\n"
            "Green Team\n"
            "---------\n"
            f"{green_leaderboard}\n"
        )


# Import this into to other files that need game logic
game_manager = GameManager()
