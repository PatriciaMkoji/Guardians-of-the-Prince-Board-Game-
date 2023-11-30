from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize the game variables
board_size = 3
board = [[None] * board_size for _ in range(board_size)]
game_over = False
current_player_symbol = "X"
bomb_available = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_board', methods=['GET'])
def get_board():
    global board
    return jsonify(board)


@app.route('/make_move', methods=['POST'])
def make_move():
    global board, game_over, current_player_symbol
    if not game_over:
        data = request.get_json()
        row = data['row']
        col = data['col']

        if not board[row][col]:
            board[row][col] = current_player_symbol

            if check_winner() or check_draw():
                game_over = True

            switch_player()

    return jsonify({'game_over': game_over})


@app.route('/reset_game', methods=['POST'])
def reset_game():
    global board, game_over, current_player_symbol, bomb_available
    board = [[None] * board_size for _ in range(board_size)]
    game_over = False
    current_player_symbol = "X"
    bomb_available = True
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
