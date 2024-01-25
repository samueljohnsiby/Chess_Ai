import chess
import chess.engine
from board_evaluator import evaluate
import random


class chessBot:
    def _determine_best_move(self,board, is_white, depth = 3):
        """Given a board, determines the best move.

        Args:
            board (chess.Board): A chess board.
            is_white (bool): Whether the particular move is for white or black.
            depth (int, optional): The number of moves looked ahead.

        Returns:
            chess.Move: The best predicated move.
        """

        best_move = -100000 if is_white else 100000
        best_final = None
        for move in board.legal_moves:
            board.push(move)
            value = self._minimax(depth - 1, board, -10000, 10000, not is_white)
            board.pop()
            if (is_white and value > best_move) or (not is_white and value < best_move):

                best_move = value
                best_final = move

        return best_final

    def _minimax(self, depth, board, alpha, beta, is_maximizing):
        if board.is_game_over():
            return evaluate(board)
        
        if depth <= 0 :
            return self.quiescence_search(board,alpha,beta,2)

        if is_maximizing:
            best_move = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                
                
                value = self._minimax(depth - 1, board, alpha, beta, False)
                board.pop()
                best_move = max(best_move, value)
                alpha = max(alpha, best_move)
                if beta <= alpha:
                    break
            return best_move
        else:
           

            best_move = float('inf')
            for move in board.legal_moves:
                board.push(move)
                value = self._minimax(depth - 1, board, alpha, beta, True)
                board.pop()
                best_move = min(best_move, value)
                beta = min(beta, best_move)
                if beta <= alpha:
                    break
            return best_move



    def quiescence_search(self,board, alpha, beta, depth):
        if depth <= 0 or board.is_game_over():
            return evaluate(board)

        stand_pat = evaluate(board)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score =  self.quiescence_search(board, -beta, -alpha, depth - 1)
                board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score

        return alpha
    def stockfish_move(self,board):

        stockfish_path = r"/workspaces/Chess_Ai/stockfish-ubuntu-x86-64-modern"

        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        engine.configure({"Skill Level":1})
        stockfish_move = engine.play(board, chess.engine.Limit(time=0.5))


        return stockfish_move.move

class Monitor:
    def __init__(self):
        self.white_won=0
        self.black_won = 0
        self.draw = 0
        self.no_of_games = 0
        self.no_of_moves = 0
        self.bot_won = 0

    def update_metric(self,no_of_moves,result,no_of_games,bot_won):
        if result == "white":

            self.white_won += 1
        elif result == "black":
            self.black_won += 1
        else:
            self.draw += 1
        self.no_of_moves = no_of_moves
        self.no_of_games = no_of_games
        self.bot_won += 1

    def print_metric(self):
        print(f"Bot won: {self.bot_won} out of {self.no_of_games}")
        print(f"white won: {self.white_won}")
        print(f"black won: {self.black_won}")
        print(f"draw: {self.draw}")
        print(f"percentage: {self.white_won}/{self.black_won}")
        print(f"Average no of moves: {no_of_moves/no_of_games}")

if __name__ == '__main__':
    no_of_games = 1
    bot_won = 0
    colors = [True, False]
    monitor = Monitor()
    chessbot = chessBot()

    for i in range(no_of_games):
        board = chess.Board()
        is_white = True #random.choice(colors)
        no_of_moves = 0
        while not board.is_game_over():
            if is_white:
                move = chessbot._determine_best_move(board=board, is_white=is_white)
                is_white = False
            else:
                move = chessbot.stockfish_move(board)
                is_white = True

            board.push(move)
            no_of_moves += 1
            print(board.fen())


        if board.result() == "1-0":
            if is_white:
                bot_won += 1
            print("white won")
            result = "white"
        elif board.result() == "0-1":
            print("black won")
            result = "black"
        else:
            print("draw")
            result = "draw"



        monitor.update_metric(no_of_moves,result,no_of_games,bot_won)
    monitor.print_metric()
