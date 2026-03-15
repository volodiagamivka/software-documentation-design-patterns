from core.interfaces import IRepository

class SqlAlchemyRepository(IRepository):
    def __init__(self, session):
        self.session = session

    def save_batch(self, users, games, sessions):
        for u in users: self.session.merge(u)
        for g in games: self.session.merge(g)
        self.session.commit()
        for s in sessions: self.session.add(s)
        self.session.commit()