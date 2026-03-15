from core.models import Game, PaidGame, FreeGame
from core.interfaces import IRepository

class GameService:
    def __init__(self, repo: IRepository):
        self.repo = repo
        # Отримуємо доступ до сесії SQLAlchemy через репозиторій
        self.session = repo.session 

    def get_all_games(self):
        return self.session.query(Game).all()

    def get_game_by_id(self, game_id):
        return self.session.query(Game).filter(Game.id == game_id).first()

    def add_game(self, title, status, price):
        price = float(price)
        if price > 0:
            new_game = PaidGame(title=title, status=status, price=price)
        else:
            new_game = FreeGame(title=title, status=status)
        
        self.session.add(new_game)
        self.session.commit()

    def update_game(self, game_id, title, status, price):
        game = self.get_game_by_id(game_id)
        if game:
            game.title = title
            game.status = status
            game.price = float(price)
            # SQLAlchemy автоматично оновить тип (polymorphic), якщо потрібно, 
            # але в межах лаби достатньо просто змінити поля
            self.session.commit()

    def delete_game(self, game_id):
        game = self.get_game_by_id(game_id)
        if game:
            self.session.delete(game)
            self.session.commit()