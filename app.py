from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import timeout_decorator

from alphabeta_ai import select_move_alphabeta
from randy_ai import select_move
from minimax_ai import select_move_minimax


app = Flask(__name__)
CORS(app)


def beautify_data(data):
    board = data["board"]
    player = data["player"] + 1
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            board[i][j] += 1
            if board[i][j] > 2:
                board[i][j] = 0
    return [board, player]


@app.route("/randy", methods=["POST"])
def randy():
    board, player = beautify_data(request.get_json())
    try:
        i, j = select_move(board, player)
        return jsonify({"x": i, "y": j})
    except:
        return make_response('Timeout', 504)


@app.route("/minimax", methods=["POST"])
def minimax():
    board, player = beautify_data(request.get_json())
    try:
        i, j = select_move_minimax(board, player)
        return jsonify({"x": i, "y": j})
    except timeout_decorator.TimeoutError:
        return make_response('Timeout', 504)
    except Exception as e:
        return make_response(str(e), 500)


@app.route("/alphabeta", methods=["POST"])
def alphabeta():
    board, player = beautify_data(request.get_json())
    try:
        i, j = select_move_alphabeta(board, player, 5)
        return jsonify({"x": i, "y": j})
    except timeout_decorator.TimeoutError:
        return make_response('Timeout', 504)
    except Exception as e:
        return make_response(str(e), 500)


if __name__ == "__main__":
    app.run()
