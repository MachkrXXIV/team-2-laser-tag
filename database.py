from supabase import create_client, Client

# note this would typically be in a .env file but this is for convenience sake
SUPABASE_URL="https://tpczavhudvfcgxpsbane.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwY3phdmh1ZHZmY2d4cHNiYW5lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MjI4NjMsImV4cCI6MjAyMjk5ODg2M30.IgxUCzXizjd12Rhg8FgCz9AaKwNhMIVyxgttblG4AFg"

class Database:
    def __init__(self) -> None:
        self.__url = SUPABASE_URL
        self.__key = SUPABASE_KEY
        self.__supabase: Client = create_client(self.__url,self.__key)

    def add_player(self, name) -> None:
        players_table = "player"
        data = {"name": name}
        _, count = self.__supabase.table(players_table).insert(data, count=None).execute()
        
        print(f"Player {name} added successfully!")