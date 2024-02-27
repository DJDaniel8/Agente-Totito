# Importamos las librerías necesarias
from tkinter import Tk, Frame, Button, Label, messagebox
import numpy as np
import random
import time

# Definimos la clase Game para la lógica del juego
class Game:
    def __init__(self):
        # Inicializar el estado del juego y las submatrices
        self.main_board = np.zeros((9, 9), dtype=int)
        self.submatrices_status = np.zeros((3, 3), dtype=int)  # 0: en juego, 1: ganó X, 2: ganó O, -1: empate
        self.current_submatrix = (0, 0)
        self.player_turn = 1  # 1: X, 2: O
        self.game_over = False

    def check_winner(self, board):
        # Verificar filas y columnas
        for i in range(3):
            if np.all(board[i, :] == board[i, 0]) and board[i, 0] != 0:
                return board[i, 0]
            if np.all(board[:, i] == board[0, i]) and board[0, i] != 0:
                return board[0, i]
        # Verificar diagonales
        if np.all(board.diagonal() == board[0, 0]) and board[0, 0] != 0:
            return board[0, 0]
        if np.all(np.fliplr(board).diagonal() == board[0, 2]) and board[0, 2] != 0:
            return board[0, 2]
        return 0  # No hay ganador


    def update_main_board(self):
        submatrix_row, submatrix_col = self.current_submatrix
        winner = self.check_winner(self.main_board[submatrix_row*3:(submatrix_row+1)*3, submatrix_col*3:(submatrix_col+1)*3])
        if winner != 0:
            self.submatrices_status[submatrix_row, submatrix_col] = winner
            self.main_board[submatrix_row*3:(submatrix_row+1)*3, submatrix_col*3:(submatrix_col+1)*3] = winner


    def ai_move(self):
        available_moves = np.where(self.main_board == 0)
        if len(available_moves[0]) > 0:  # Si hay movimientos disponibles
            idx = random.choice(range(len(available_moves[0])))
            row, col = available_moves[0][idx], available_moves[1][idx]
            self.main_board[row, col] = self.player_turn
            self.switch_player()


    def switch_player(self):
        # Cambiar el turno del jugador
        self.player_turn = 2 if self.player_turn == 1 else 1

    def is_draw(self):
        submatrix = self.main_board[self.current_submatrix[0]*3:(self.current_submatrix[0]+1)*3, self.current_submatrix[1]*3:(self.current_submatrix[1]+1)*3]
        if np.all(submatrix != 0) and self.check_winner(submatrix) == 0:
            return True
        return False
    
    def check_main_winner(self):
        # Inicializa las posiciones ganadoras como lista vacía
        winning_positions = []
        # Verifica filas
        for i in range(3):
            if np.all(self.submatrices_status[i, :] == self.submatrices_status[i, 0]) and self.submatrices_status[i, 0] != 0:
                winning_positions = [(i, j) for j in range(3)]
                return self.submatrices_status[i, 0], winning_positions
        # Verifica columnas
        for j in range(3):
            if np.all(self.submatrices_status[:, j] == self.submatrices_status[0, j]) and self.submatrices_status[0, j] != 0:
                winning_positions = [(i, j) for i in range(3)]
                return self.submatrices_status[0, j], winning_positions
        # Verifica diagonal principal
        if np.all(np.diag(self.submatrices_status) == self.submatrices_status[0, 0]) and self.submatrices_status[0, 0] != 0:
            winning_positions = [(i, i) for i in range(3)]
            return self.submatrices_status[0, 0], winning_positions
        # Verifica diagonal secundaria
        if np.all(np.diag(np.fliplr(self.submatrices_status)) == self.submatrices_status[0, 2]) and self.submatrices_status[0, 2] != 0:
            winning_positions = [(i, 2-i) for i in range(3)]
            return self.submatrices_status[0, 2], winning_positions
        # Si no hay ganador
        return 0, winning_positions



# Clase GUI para la interfaz gráfica del juego
class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe Ultimate")
        self.game = Game()
        self.setup_ui()
        self.agent = Agent(1 if self.game.player_turn == 2 else 2)

    def setup_ui(self):
        # Configuración inicial de la interfaz gráfica
        self.frames = {}
        self.buttons = {}
        game_frame = Frame(self.master)
        game_frame.pack(side="left")
        main_board_frame = Frame(self.master)
        main_board_frame.pack(side="right")
        
        for row in range(3):
            for col in range(3):
                button = Button(game_frame, text='', font=('Arial', 20), height=2, width=5,
                                command=lambda r=row, c=col: self.player_move(r, c))
                button.grid(row=row, column=col)
                self.buttons[row, col] = button

        for row in range(3):
            for col in range(3):
                label = Label(main_board_frame, text='', font=('Arial', 20), height=2, width=5, relief="solid")
                label.grid(row=row, column=col)
                self.frames[row, col] = label

    def player_move(self, row, col):
        submatrix_row, submatrix_col = self.game.current_submatrix
        global_row, global_col = submatrix_row * 3 + row, submatrix_col * 3 + col
        
        if self.game.main_board[global_row, global_col] == 0:
            self.game.main_board[global_row, global_col] = self.game.player_turn
            winner = self.game.check_winner(self.game.main_board[global_row - global_row % 3: global_row - global_row % 3 + 3, global_col - global_col % 3: global_col - global_col % 3 + 3])
            
            if winner:
                self.update_ui()  # Actualizar la UI después de cada movimiento
                self.update_main_ui()
                winner_text = 'X' if winner == 1 else 'O'
                messagebox.showinfo("Resultado de la Submatriz", f"El ganador es {winner_text} en la submatriz actual.")
                self.game.submatrices_status[submatrix_row, submatrix_col] = winner
                self.advance_to_next_submatrix()
            elif self.game.is_draw():
                messagebox.showinfo("Empate", "La submatriz ha terminado en empate. Reiniciando submatriz.")
                self.reset_submatrix_ui()  # Esto limpiará la UI pero no el estado de la submatriz en `main_board`
                # Aquí necesitas resetear también el estado de la submatriz en `main_board`
                self.reset_submatrix_state(submatrix_row, submatrix_col)
            else:
                self.game.switch_player()
            
            if not self.game.game_over:
                self.master.after(1000,self.agent_move)
            
            self.update_ui()  # Actualizar la UI después de cada movimiento
            self.update_main_ui()  # Asegurarse de que la matriz principal también se actualice
            
            main_winner, winning_positions = self.game.check_main_winner()
            if main_winner:
                # Si hay un ganador, muestra el ganador y resalta las casillas ganadoras
                self.show_winner(main_winner, winning_positions)
        
    def agent_move(self):
        if self.game.player_turn != self.agent.player_number:
            # Si no es el turno del agente, simplemente retorna
            return

        row, col = self.agent.select_move(self.game)
        if row is not None and col is not None:
            # Convertir la posición en coordenadas globales si es necesario
            submatrix_row, submatrix_col = self.game.current_submatrix
            global_row, global_col = submatrix_row * 3 + row % 3, submatrix_col * 3 + col % 3
            
            # Realizar el movimiento en el tablero principal
            self.game.main_board[global_row, global_col] = self.agent.player_number
            
            # Actualizar la UI para reflejar el movimiento del agente
            self.update_ui()
            
            # Verificar si hay un ganador o un empate después del movimiento del agente
            winner = self.game.check_winner(self.game.main_board[global_row - global_row % 3: global_row - global_row % 3 + 3, global_col - global_col % 3: global_col - global_col % 3 + 3])
            if winner:
                winner_text = 'X' if winner == 1 else 'O'
                messagebox.showinfo("Resultado de la Submatriz", f"El ganador es {winner_text} en la submatriz actual.")
                self.game.submatrices_status[submatrix_row, submatrix_col] = winner
                self.advance_to_next_submatrix()
                self.update_ui()
                self.update_main_ui()
            elif self.game.is_draw():
                messagebox.showinfo("Empate", "La submatriz ha terminado en empate. Reiniciando submatriz.")
                self.reset_submatrix_ui()
                self.reset_submatrix_state(submatrix_row, submatrix_col)
            
            # Cambiar el turno al jugador humano
            self.game.switch_player()

            # Verificar si hay un ganador en la matriz principal después del movimiento del agente
            main_winner, winning_positions = self.game.check_main_winner()
            if main_winner:
                self.show_winner(main_winner, winning_positions)

    def update_ui(self):
        submatrix_row, submatrix_col = self.game.current_submatrix
        start_row, start_col = submatrix_row * 3, submatrix_col * 3

        # Solo actualizamos los botones de la submatriz actual en juego
        for row in range(3):
            for col in range(3):
                global_row, global_col = start_row + row, start_col + col
                button = self.buttons[row, col]
                value = self.game.main_board[global_row, global_col]
                text = 'X' if value == 1 else 'O' if value == 2 else ''
                button.config(text=text)

    def show_winner(self, winner, winning_positions):
        # Mostrar el ganador del juego en una ventana de mensaje
        winner_text = 'X' if winner == 1 else 'O'
        messagebox.showinfo("Fin del Juego", f"El ganador es {winner_text}!")
        
        # Resaltar las casillas ganadoras
        for row, col in winning_positions:
            self.frames[row, col].config(bg='lightgreen')  # Usa el color que prefieras
        
    def reset_submatrix_ui(self):
        # Limpiar los botones de la submatriz actual para el nuevo juego
        for row in range(3):
            for col in range(3):
                button = self.buttons[row, col]
                button.config(text='')

    def advance_to_next_submatrix(self):
        # Avanzar a la siguiente submatriz en juego
        # Esta es una simplificación. Necesitarías una lógica para determinar correctamente la siguiente submatriz
        next_submatrix = (self.game.current_submatrix[0], (self.game.current_submatrix[1] + 1) % 3)
        if next_submatrix[1] == 0:
            next_submatrix = ((next_submatrix[0] + 1) % 3, next_submatrix[1])
        self.game.current_submatrix = next_submatrix
        self.reset_submatrix_ui()
        
    def update_main_ui(self):
        for row in range(3):
            for col in range(3):
                label = self.frames[row, col]
                winner = self.game.submatrices_status[row, col]
                text = 'X' if winner == 1 else 'O' if winner == 2 else ''
                label.config(text=text)

    def reset_submatrix_state(self, submatrix_row, submatrix_col):
        start_row = submatrix_row * 3
        start_col = submatrix_col * 3
        for row in range(3):
            for col in range(3):
                self.game.main_board[start_row + row, start_col + col] = 0
                
class Agent:
    def __init__(self, player_number):
        self.player_number = player_number  # El número del jugador (1 o 2)
        self.opponent_number = 1 if player_number == 2 else 2

    def select_move(self, game):
        # Identificar la submatriz actual
        submatrix_start_row = game.current_submatrix[0] * 3
        submatrix_start_col = game.current_submatrix[1] * 3
        submatrix = game.main_board[submatrix_start_row:submatrix_start_row+3, submatrix_start_col:submatrix_start_col+3]

        # Priorizar bloquear al oponente o ganar
        for player in [self.player_number, self.opponent_number]:
            for row in range(3):
                if self.check_line(submatrix[row, :], player) == player:
                    return submatrix_start_row + row, submatrix_start_col + np.where(submatrix[row, :] == 0)[0][0]
            for col in range(3):
                if self.check_line(submatrix[:, col], player) == player:
                    return submatrix_start_row + np.where(submatrix[:, col] == 0)[0][0], submatrix_start_col + col
            if self.check_line(submatrix.diagonal(), player) == player:
                return submatrix_start_row + np.where(submatrix.diagonal() == 0)[0][0], submatrix_start_col + np.where(submatrix.diagonal() == 0)[0][0]
            if self.check_line(np.fliplr(submatrix).diagonal(), player) == player:
                row_index = np.where(np.fliplr(submatrix).diagonal() == 0)[0][0]
                return submatrix_start_row + row_index, submatrix_start_col + 2 - row_index

        # Si no hay jugadas críticas, selecciona un movimiento al azar
        available_positions = np.argwhere(submatrix == 0)
        if len(available_positions) > 0:
            idx = np.random.choice(len(available_positions))
            chosen_move = available_positions[idx]
            global_row = submatrix_start_row + chosen_move[0]
            global_col = submatrix_start_col + chosen_move[1]
            return global_row, global_col

        return None, None

    def check_line(self, line, player):
        # Retorna el número del jugador si está a una jugada de ganar, de lo contrario 0
        if np.sum(line == player) == 2 and np.sum(line == 0) == 1:
            return player
        return 0



# Función principal para iniciar el juego
def main():
    root = Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()

# Comentar la llamada a la función principal para evitar la ejecución automática
main()
