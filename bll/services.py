from core.models import User, FreeGame, PaidGame, GameSession
from core.interfaces import IRepository, ICSVDataSource

class ImportService:
    def __init__(self, repo: IRepository, loader: ICSVDataSource):
        self.repo = repo  
        self.loader = loader

    def execute_import(self, file_path):
        data = self.loader.get_data(file_path)
        
        users, games, sessions = [], [], []
        seen_users, seen_games = set(), set()

        for row in data:
            if row['userID'] not in seen_users:
                users.append(User(id=row['userID'], email=row['email']))
                seen_users.add(row['userID'])

            gid = int(row['gameID'])
            if gid not in seen_games:
                price = float(row['price'])
                game_cls = PaidGame if price > 0 else FreeGame
                games.append(game_cls(id=gid, title=row['title'], status=row['status'], price=price))
                seen_games.add(gid)

            sessions.append(GameSession(user_id=row['userID'], game_id=gid, current_progress=row['progress']))

        self.repo.save_batch(users, games, sessions)