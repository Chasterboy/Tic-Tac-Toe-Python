import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        # Inicialización de la aplicación y configuración de la interfaz gráfica
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("300x300")  # Se ajusta el tamaño de la ventana
        self.current_player = 'X'
        self.current_op = 'O'
        self.ganadas_jugador = 0
        self.ganadas_ia = 0
        self.empates = 0

        # Etiqueta para mostrar la puntuación
        self.score_label = tk.Label(root, text="Jugador: 0 | Empate: 0 | IA: 0", font=('normal', 12))
        self.score_label.grid(row=0, column=0, columnspan=3, sticky="nsew")  # Sticky para que abarque toda la parte superior

        # Creación de botones para el juego
        self.buttons = [[None, None, None] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                # Configuración de cada botón con un comando lambda para manejar clics
                self.buttons[i][j] = tk.Button(root, text="", font=('normal', 35),  # Se ajusta el tamaño de fuente para hacer los botones más cuadrados
                                              width=3, height=3, bg='white', fg='black',  # Se ajusta el tamaño de los botones
                                              command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i + 1, column=j, padx=5, pady=5, sticky="nsew")

        # Configuración del fondo y redimensionamiento de la ventana
        root.configure(bg='black')
        root.resizable(width=False, height=False)
        for i in range(3):
            root.grid_rowconfigure(i + 1, weight=1)

        # Inicialización de la lógica del juego y comienzo con el jugador (usuario)
        self.tablero = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        self.play_user_move()

    def on_button_click(self, row, col):
        # Manejo de clics en los botones durante el juego
        if self.quedanMovimientos() and self.tablero[row][col].isdigit():
            self.tablero[row][col] = self.current_player
            self.buttons[row][col]['text'] = self.current_player
            self.buttons[row][col]['state'] = tk.DISABLED  # Deshabilitar el botón después del movimiento
            self.check_winner()
            self.play_ai_move()

    def check_winner(self):
        # Verificación del estado del juego para determinar si hay un ganador o empate
        resultado = self.evaluar(self.tablero)
        if resultado == 10:
            messagebox.showinfo("Fin del juego", "¡La IA ha ganado!")
            self.ganadas_ia += 1
            self.update_score()
            self.restart_game()
        elif resultado == -10:
            messagebox.showinfo("Fin del juego", "¡Has ganado!")
            self.ganadas_jugador += 1
            self.update_score()
            self.restart_game()
        elif not any(cell.isdigit() for row in self.tablero for cell in row):
            messagebox.showinfo("Fin del juego", "Es un empate.")
            self.empates += 1
            self.update_score()
            self.restart_game()

    def switch_player(self):
        # Cambio entre jugadores (usuario y IA)
        self.current_player, self.current_op = self.current_op, self.current_player

    def evaluar(self, b):
        # Evaluación del estado del tablero para determinar el resultado del juego
        lineas = [b[i] for i in range(3)] + \
                [[b[j][i] for j in range(3)] for i in range(3)] + \
                [[b[i][i] for i in range(3)], [b[i][2 - i] for i in range(3)]]

        for linea in lineas:
            if all(cell == self.current_op for cell in linea):
                return 10
            elif all(cell == 'X' for cell in linea):
                return -10

        return 0

    def restart_game(self):
        # Restablecimiento del estado del juego después de que termina una partida
        self.current_player = 'X'
        self.tablero = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

        # Habilitar los botones y limpiar sus textos
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['state'] = tk.NORMAL
                self.buttons[i][j]['text'] = ""

        # Comenzar el juego con el jugador (usuario)
        self.play_user_move()

    def quedanMovimientos(self):
        # Verificación de si quedan movimientos posibles en el juego
        return any(cell.isdigit() for row in self.tablero for cell in row)

    def minimax(self, esMax, alpha, beta):
        # Implementación del algoritmo minimax para la toma de decisiones de la IA
        puntaje = self.evaluar(self.tablero)
        if puntaje != 0 or not self.quedanMovimientos():
            return puntaje

        if esMax:
            mejor_puntaje = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.tablero[i][j].isdigit():
                        self.tablero[i][j] = self.current_op
                        puntaje = self.minimax(not esMax, alpha, beta)
                        self.tablero[i][j] = str(i * 3 + j + 1)
                        mejor_puntaje = max(mejor_puntaje, puntaje)
                        alpha = max(alpha, puntaje)
                        if beta <= alpha:
                            break
            return mejor_puntaje
        else:
            mejor_puntaje = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.tablero[i][j].isdigit():
                        self.tablero[i][j] = 'X'
                        puntaje = self.minimax(not esMax, alpha, beta)
                        self.tablero[i][j] = str(i * 3 + j + 1)
                        mejor_puntaje = min(mejor_puntaje, puntaje)
                        beta = min(beta, puntaje)
                        if beta <= alpha:
                            break
            return mejor_puntaje

    def encontrarMejorMovimiento(self):
        # Encuentra el mejor movimiento para la IA utilizando el algoritmo minimax
        mejorValor = float('-inf')
        mejorMovimiento = (-1, -1)

        for i in range(3):
            for j in range(3):
                if self.tablero[i][j].isdigit():
                    self.tablero[i][j] = self.current_op
                    valorMovimiento = self.minimax(False, float('-inf'), float('inf'))
                    self.tablero[i][j] = str(i * 3 + j + 1)

                    if valorMovimiento > mejorValor:
                        mejorMovimiento = (i, j)
                        mejorValor = valorMovimiento

        return mejorMovimiento

    def play_ai_move(self):
        # Realiza el movimiento de la IA y verifica el resultado del juego
        if self.quedanMovimientos():
            movimiento = self.encontrarMejorMovimiento()
            if movimiento != (-1, -1):
                row, col = movimiento
                self.tablero[row][col] = self.current_op
                self.buttons[row][col]['text'] = self.current_op
                self.buttons[row][col]['state'] = tk.DISABLED
                self.check_winner()

                # Si quedan movimientos, permite al jugador (usuario) realizar su movimiento
                if self.quedanMovimientos():
                    self.play_user_move()

    def play_user_move(self):
        # Habilita los botones para que el jugador (usuario) realice su movimiento
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['state'] = tk.NORMAL

    def update_score(self):
        # Actualiza la etiqueta de puntuación en la interfaz gráfica
        self.score_label.config(text=f"Jugador: {self.ganadas_jugador} | Empate: {self.empates} | IA: {self.ganadas_ia}")

if __name__ == "__main__":
    # Configuración inicial del juego y ejecución de la interfaz gráfica
    root = tk.Tk()
    root.iconbitmap("C:/Users/Eduardo/OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO/Escritorio/tictac/tic-tac-toe.ico")
    game = TicTacToe(root)
    root.mainloop()

