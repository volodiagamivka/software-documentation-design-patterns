import io
import csv
from core.models import Game, PaidGame, FreeGame, User, GameSession
from core.interfaces import IRepository

class GameService:
    def __init__(self, repo: IRepository):
        self.repo = repo
        self.session = repo.session 

    def get_all_games(self):
        return self.session.query(Game).all()

    def get_game_by_id(self, game_id):
        return self.session.query(Game).filter(Game.id == game_id).first()

    def add_game(self, title, status, price):
        price = float(price)
        game = PaidGame(title=title, status=status, price=price) if price > 0 else FreeGame(title=title, status=status)
        self.session.add(game)
        self.session.commit()

    def update_game(self, game_id, title, status, price):
        game = self.get_game_by_id(game_id)
        if game:
            game.title = title
            game.status = status
            game.price = float(price)
            self.session.commit()

    def delete_game(self, game_id):
        game = self.get_game_by_id(game_id)
        if game:
            self.session.delete(game)
            self.session.commit()

 
    def import_from_stream(self, file_stream):
        stream = io.StringIO(file_stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        
        users_map = {}
        games_map = {}
        sessions = []

        for row in reader:
            uid = row['userID']
            if uid not in users_map:
                users_map[uid] = User(id=uid, email=row['email'])

            gid = int(row['gameID'])
            if gid not in games_map:
                price = float(row['price'])
                if price > 0:
                    games_map[gid] = PaidGame(id=gid, title=row['title'], status=row['status'], price=price)
                else:
                    games_map[gid] = FreeGame(id=gid, title=row['title'], status=row['status'])

            sessions.append(GameSession(user_id=uid, game_id=gid, current_progress=row['progress']))

        self.repo.save_batch(users_map.values(), games_map.values(), sessions)
        return len(sessions)