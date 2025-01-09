# **Jogo Minesweeper com Interface Tkinter**

"""
Nesta etapa, implementaremos a interface gráfica usando Tkinter para interagir com o usuário.
Os objetivos são:
- Exibir o tabuleiro.
- Integrar a classe `Grid` com eventos de clique.
- Atualizar visualmente o estado do jogo em resposta às interações.
- Adicionar lógica de marcação e contador de tempo.
"""

import tkinter as tk
from tkinter import messagebox
import random
import time

# **Classe Cell: Representa uma célula individual**
class Cell:
    def __init__(self):
        self.has_mine = False  # Indica se a célula contém uma mina
        self.adjacent_mines = 0  # Número de minas adjacentes
        self.state = "hidden"  # Pode ser 'hidden', 'revealed', ou 'flagged'

# **Classe Grid: Gerencia o tabuleiro do jogo**
class Grid:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.mines_positions = []

    def generate_mines(self, first_click):
        """
        Posiciona as minas aleatoriamente, garantindo que a primeira célula clicada não contenha mina.
        """
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        all_positions.remove(first_click)
        self.mines_positions = random.sample(all_positions, self.num_mines)
        for r, c in self.mines_positions:
            self.board[r][c].has_mine = True

    def calculate_adjacencies(self):
        """
        Calcula o número de minas adjacentes para cada célula do tabuleiro.
        """
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)
        ]
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c].has_mine:
                    continue
                count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.board[nr][nc].has_mine:
                            count += 1
                self.board[r][c].adjacent_mines = count

    def reveal_cell(self, row, col):
        """
        Revela o conteúdo da célula e aciona a recursão para áreas livres.
        """
        cell = self.board[row][col]
        if cell.state != "hidden":
            return

        cell.state = "revealed"

        if cell.has_mine:
            return "game_over"

        if cell.adjacent_mines == 0:
            directions = [
                (-1, -1), (-1, 0), (-1, 1),
                ( 0, -1),          ( 0, 1),
                ( 1, -1), ( 1, 0), ( 1, 1)
            ]
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    self.reveal_cell(nr, nc)
        return "continue"

    def check_victory(self):
        """
        Verifica se todas as células seguras foram reveladas.
        """
        for row in self.board:
            for cell in row:
                if not cell.has_mine and cell.state != "revealed":
                    return False
        return True

    def mark_cell(self, row, col):
        """
        Marca ou desmarca uma célula como suspeita de conter uma mina.
        """
        cell = self.board[row][col]
        if cell.state == "hidden":
            cell.state = "flagged"
        elif cell.state == "flagged":
            cell.state = "hidden"

# **Classe MinesweeperApp: Interface Gráfica**
class MinesweeperApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.master.configure(bg='navy')
        
        # Cria o título texto
        self.title_label = tk.Label(self.master, 
                                  text="Minesweeper", 
                                  font=("Algerian", 24, "bold"),
                                  bg='navy',
                                  fg='white',
                                  pady=15)
        self.title_label.grid(row=0, column=0, columnspan=9, pady=10)
        
        # Frame para conter o timer e contadores
        self.info_frame = tk.Frame(self.master, bg='navy')
        self.info_frame.grid(row=1, column=0, columnspan=9, pady=5)
        
        # Contador de bandeiras
        self.flags_remaining = 10  # Começa com o número de minas
        self.flags_label = tk.Label(self.info_frame, 
                                  text=f"🚩 Restantes: {self.flags_remaining}", 
                                  font=("Arial", 12),
                                  bg='navy',
                                  fg='white')
        self.flags_label.pack(side=tk.LEFT, padx=20)
        
        # Timer
        self.timer_label = tk.Label(self.info_frame, 
                                  text="Tempo: 0s", 
                                  font=("Arial", 12),
                                  bg='navy',
                                  fg='white')
        self.timer_label.pack(side=tk.LEFT, padx=20)
        
        # Botão de reinício
        self.restart_button = tk.Button(self.info_frame,
                                      text="Reiniciar 🔄",
                                      font=("Arial", 10, "bold"),
                                      command=self.restart_game,
                                      bg='lightblue',
                                      fg='navy')
        self.restart_button.pack(side=tk.LEFT, padx=20)
        
        # Frame para conter o tabuleiro
        self.board_frame = tk.Frame(self.master, bg='navy', padx=20, pady=20)
        self.board_frame.grid(row=2, column=0, columnspan=9)
        
        self.grid = Grid(9, 9, 10)
        self.first_click = True
        self.buttons = []
        self.start_time = None
        
        self.create_widgets()

    def create_widgets(self):
        for r in range(self.grid.rows):
            row_buttons = []
            for c in range(self.grid.cols):
                btn = tk.Button(self.board_frame, 
                              width=2, 
                              height=1, 
                              font=("Arial", 14, "bold"),
                              relief="raised",
                              borderwidth=2)
                btn.bind("<Button-1>", lambda event, r=r, c=c: self.on_left_click(r, c))
                btn.bind("<Button-3>", lambda event, r=r, c=c: self.on_right_click(r, c))
                btn.grid(row=r, column=c, padx=1, pady=1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def start_timer(self):
        if self.start_time is None:
            self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        if self.start_time is not None:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Tempo: {elapsed_time}s")
            self.master.after(1000, self.update_timer)

    def on_left_click(self, row, col):
        if self.first_click:
            self.grid.generate_mines((row, col))
            self.grid.calculate_adjacencies()
            self.first_click = False
            self.start_timer()

        result = self.grid.reveal_cell(row, col)
        self.update_buttons()

        if result == "game_over":
            self.show_game_over()
        elif self.grid.check_victory():
            self.show_victory()

    def on_right_click(self, row, col):
        if self.grid.board[row][col].state == "hidden":
            self.flags_remaining -= 1
        elif self.grid.board[row][col].state == "flagged":
            self.flags_remaining += 1
        self.flags_label.config(text=f"🚩 Restantes: {self.flags_remaining}")
        self.grid.mark_cell(row, col)
        self.update_buttons()

    def update_buttons(self):
        number_colors = {
            1: '#4F94CD',  # Azul claro
            2: '#90EE90',  # Verde claro
            3: '#FF6B6B',  # Vermelho claro
            4: '#9370DB',  # Roxo
            5: '#CD5C5C',  # Vermelho escuro
            6: '#48D1CC',  # Turquesa
            7: '#2F4F4F',  # Cinza escuro
            8: '#A9A9A9'   # Cinza claro
        }
        
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell = self.grid.board[r][c]
                btn = self.buttons[r][c]
                if cell.state == "revealed":
                    if cell.has_mine:
                        btn.config(text="💣", bg="red")
                    else:
                        btn.config(bg="white")
                        if cell.adjacent_mines > 0:
                            btn.config(text=str(cell.adjacent_mines),
                                     fg=number_colors[cell.adjacent_mines])
                        else:
                            btn.config(text="")
                elif cell.state == "flagged":
                    btn.config(text="🚩", bg="yellow")
                else:
                    btn.config(text="", bg="SystemButtonFace")

    def show_game_over(self):
        for r, c in self.grid.mines_positions:
            self.buttons[r][c].config(text="💣", bg="red")
        messagebox.showinfo("Fim de Jogo", "Você perdeu!")
        self.master.quit()

    def show_victory(self):
        messagebox.showinfo("Parabéns", "Você venceu!")
        self.master.quit()

    def restart_game(self):
        # Resetar o timer
        self.start_time = None
        self.timer_label.config(text="Tempo: 0s")
        
        # Resetar o contador de bandeiras
        self.flags_remaining = 10
        self.flags_label.config(text=f"🚩 Restantes: {self.flags_remaining}")
        
        # Criar novo grid
        self.grid = Grid(9, 9, 10)
        self.first_click = True
        
        # Resetar todos os botões
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                btn = self.buttons[r][c]
                btn.config(text="", bg="SystemButtonFace")

# **Inicialização do Jogo**
if __name__ == "__main__":
    root = tk.Tk()
    
    # Configurações da janela
    root.resizable(False, False)  # Impede redimensionamento
    root.geometry("400x600")  # Define tamanho fixo
    
    app = MinesweeperApp(root)
    root.mainloop()