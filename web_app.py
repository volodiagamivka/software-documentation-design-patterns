from flask import Flask, render_template, request, redirect, url_for, jsonify
from flasgger import Swagger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dal.repository import SqlAlchemyRepository
from bll.services import GameService

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'Steam Game API',
    'uiversion': 3
}
swagger = Swagger(app)

engine = create_engine('sqlite:///data/steam.db')
Session = sessionmaker(bind=engine)
db_session = Session()

repo = SqlAlchemyRepository(db_session)
game_service = GameService(repo)

@app.route('/')
def index():
    """
    Get Main Page
    ---
    responses:
      200:
        description: HTML page with games list
    """
    games = game_service.get_all_games()
    return render_template('index.html', games=games)

@app.route('/api/games', methods=['GET'])
def get_games_api():
    """
    Get all games as JSON
    ---
    responses:
      200:
        description: A list of games
    """
    games = game_service.get_all_games()
    output = [{"id": g.id, "title": g.title, "status": g.status, "price": g.price} for g in games]
    return jsonify(output)

@app.route('/add', methods=['GET', 'POST'])
def add_game():
    """
    Add a new game
    ---
    parameters:
      - name: title
        in: formData
        type: string
        required: true
      - name: status
        in: formData
        type: string
      - name: price
        in: formData
        type: number
    responses:
      302:
        description: Redirect to index
    """
    if request.method == 'POST':
        game_service.add_game(
            title=request.form.get('title'),
            status=request.form.get('status'),
            price=request.form.get('price', 0)
        )
        return redirect(url_for('index'))
    return render_template('add_game.html')

@app.route('/delete/<int:id>')
def delete_game(id):
    """
    Delete game by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      302:
        description: Redirect to index
    """
    game_service.delete_game(id)
    return redirect(url_for('index'))
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_game(id):
    """
    Edit an existing game
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Form for editing
      302:
        description: Redirect to index after update
    """
   
    game = game_service.get_game_by_id(id)
    
    if not game:
        return "Гра не знайдена", 404

    if request.method == 'POST':
        game_service.update_game(
            game_id=id,
            title=request.form.get('title'),
            status=request.form.get('status'),
            price=request.form.get('price')
        )
        return redirect(url_for('index'))
    return render_template('edit_game.html', game=game)
if __name__ == '__main__':
    app.run(debug=True, port=5000)