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
    """Main page showing all games"""
    games = game_service.get_all_games()
    return render_template('index.html', games=games)

@app.route('/api/games', methods=['GET'])
def get_games_api():
    """Get all games in JSON format
    ---
    responses:
      200:
        description: List of games
    """
    games = game_service.get_all_games()
    output = [{"id": g.id, "title": g.title, "status": g.status, "price": g.price} for g in games]
    return jsonify(output)

@app.route('/add', methods=['GET', 'POST'])
def add_game():
    """Add a new game
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
        description: Перенаправлення на головну
    """
    if request.method == 'POST':
        game_service.add_game(
            title=request.form.get('title'),
            status=request.form.get('status'),
            price=request.form.get('price', 0)
        )
        return redirect(url_for('index'))
    return render_template('add_game.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_game(id):
    """Edit an existing game
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: title
        in: formData
        type: string
      - name: status
        in: formData
        type: string
      - name: price
        in: formData
        type: number
    responses:
      302:
        description: Update and redirect
    """
    game = game_service.get_game_by_id(id)
    if not game:
        return "Game not found", 404

    if request.method == 'POST':
        game_service.update_game(
            game_id=id,
            title=request.form.get('title'),
            status=request.form.get('status'),
            price=request.form.get('price')
        )
        return redirect(url_for('index'))

    return render_template('edit_game.html', game=game)

@app.route('/delete/<int:id>')
def delete_game(id):
    """Delete a game by its ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      302:
        description: Delete and redirect
    """
    game_service.delete_game(id)
    return redirect(url_for('index'))
@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    """
    Upload data via CSV file
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Choose csv file 
    responses:
      200:
        description: Data uploaded successfully
      400:
        description: Error in file or request
    """
    if 'file' not in request.files:
        return jsonify({"error": "File not found"}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format. CSV file required"}), 400

    try:
        count = game_service.import_from_stream(file)
        return jsonify({
            "status": "success",
            "message": f"Imported records: {count}. Database updated."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)