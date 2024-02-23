from supabase import create_client, Client
from player import Player

# note this would typically be in a .env file but this is for convenience sake
SUPABASE_URL="https://tpczavhudvfcgxpsbane.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwY3phdmh1ZHZmY2d4cHNiYW5lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MjI4NjMsImV4cCI6MjAyMjk5ODg2M30.IgxUCzXizjd12Rhg8FgCz9AaKwNhMIVyxgttblG4AFg"

class Database:
    def __init__(self) -> None:
        self.__url = SUPABASE_URL
        self.__key = SUPABASE_KEY
        self.__table_name = "player"
        self.__supabase: Client = create_client(self.__url,self.__key)

    # def add_player(self, name) -> None:
    #     players_table = "player"
    #     data = {"name": name}
    #     _, count = self.__supabase.table(players_table).insert(data, count=None).execute()
        
    #     print(f"Player {name} added successfully!")
    
    def get_player(self, player_id)->Player:
        player = self.__supabase.table(self.__table_name).select("*").eq("player_id", player_id).execute()
        try:
            p = Player(player.data[0]["player_id"],player.data[0]["name"])
            print("Successfully fetched player")
            return p
        except:
            return None

    def add_player(self, player_id, name = None) -> None:
        # request input of name
        data = {"player_id": player_id, "name": name}
        _, count = self.__supabase.table(self.__table_name).insert(data, count=None).execute()
        print(f"Player {name} with ID: {player_id} added successfully!")