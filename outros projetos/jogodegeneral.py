import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
import winsound

class GeneralGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de General")
        self.root.geometry("800x700")
        
        # Carregar high scores
        self.high_scores = self.load_high_scores()
        
        # Variáveis do jogo
        self.rolls_left = 3
        self.current_dice = [1, 1, 1, 1, 1]
        self.dice_states = [False] * 5
        self.current_round = 1
        self.score = 0
        self.available_sequences = {
            "General": None,
            "Quadra": None,
            "Full House": None,
            "Sequência Alta": None,
            "Sequência Baixa": None,
            "Trinca": None,
            "Par": None
        }
        
        # Criar menu
        self.create_menu()
        
        # Criar frames principais
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Frame para os dados
        self.dice_frame = ttk.LabelFrame(self.main_frame, text="Dados", padding=10)
        self.dice_frame.pack(fill='x', pady=(0, 20))
        
        # Estilo personalizado para os botões
        style = ttk.Style()
        style.configure("Dice.TButton", padding=10, font=('Arial', 12))
        style.configure("Keep.TButton", padding=5)
        
        # Criar área dos dados
        self.dice_buttons = []
        self.keep_buttons = []
        for i in range(5):
            dice_frame = ttk.Frame(self.dice_frame)
            dice_frame.grid(row=0, column=i, padx=10, pady=5)
            
            # Botão do dado com estilo melhorado
            dice_btn = ttk.Label(dice_frame, text="1",
                               font=('Arial', 24, 'bold'), width=3,
                               relief='raised', borderwidth=2)
            dice_btn.pack(pady=(0, 5))
            self.dice_buttons.append(dice_btn)
            
            # Botão de manter com estilo melhorado
            keep_btn = ttk.Button(dice_frame, text="Manter",
                                command=lambda x=i: self.toggle_dice(x),
                                style="Keep.TButton")
            keep_btn.pack()
            self.keep_buttons.append(keep_btn)
        
        # Frame de controles
        self.control_frame = ttk.Frame(self.dice_frame)
        self.control_frame.grid(row=1, column=0, columnspan=5, pady=10)
        
        # Botão de rolagem
        self.roll_button = ttk.Button(self.control_frame,
                                    text=f"Rolar Dados ({self.rolls_left} tentativas)",
                                    command=self.roll_dice)
        self.roll_button.pack(pady=5)
        
        # Informações do jogo
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Status do Jogo", padding=10)
        self.info_frame.pack(fill='x', pady=(0, 20))
        
        self.round_label = ttk.Label(self.info_frame,
                                   text=f"Rodada: {self.current_round}/7",
                                   font=('Arial', 12))
        self.round_label.pack(side='left', padx=5)
        
        self.score_label = ttk.Label(self.info_frame,
                                   text=f"Pontuação: {self.score}",
                                   font=('Arial', 12))
        self.score_label.pack(side='right', padx=5)
        
        # Frame para sequências disponíveis
        self.sequences_frame = ttk.LabelFrame(self.main_frame, text="Sequências Disponíveis", padding=10)
        self.sequences_frame.pack(fill='both', expand=True)
        
        # Botões para cada sequência
        self.sequence_buttons = {}
        for seq in self.available_sequences.keys():
            frame = ttk.Frame(self.sequences_frame)
            frame.pack(fill='x', pady=2)
            
            btn = ttk.Button(frame, text=seq,
                           command=lambda s=seq: self.select_sequence(s),
                           state='disabled')
            btn.pack(side='left', padx=5)
            
            label = ttk.Label(frame, text="---")
            label.pack(side='right', padx=5)
            
            self.sequence_buttons[seq] = (btn, label)

    def create_menu(self):
        """Cria o menu do jogo"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Jogo
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Jogo", menu=game_menu)
        game_menu.add_command(label="Novo Jogo", command=self.new_game)
        game_menu.add_command(label="High Scores", command=self.show_high_scores)
        game_menu.add_separator()
        game_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Instruções", command=self.show_instructions)
        help_menu.add_command(label="Sobre", command=self.show_about)

    def show_instructions(self):
        """Mostra as instruções do jogo"""
        instructions = """
        Como Jogar General:
        
        1. Você tem 3 tentativas por rodada para fazer combinações
        2. Após cada jogada, você pode manter alguns dados e rolar os outros
        3. As combinações possíveis são:
           - General: 5 dados iguais
           - Quadra: 4 dados iguais
           - Full House: 3 dados iguais + 2 dados iguais
           - Sequência Alta: 2-3-4-5-6
           - Sequência Baixa: 1-2-3-4-5
           - Trinca: 3 dados iguais
           - Par: 2 dados iguais
        4. Você tem 7 rodadas para fazer a maior pontuação possível
        """
        messagebox.showinfo("Instruções", instructions)

    def show_about(self):
        """Mostra informações sobre o jogo"""
        about = "Jogo de General v2.0\nDesenvolvido com Python/Tkinter"
        messagebox.showinfo("Sobre", about)

    def load_high_scores(self):
        """Carrega as maiores pontuações do arquivo"""
        try:
            if os.path.exists('high_scores.json'):
                with open('high_scores.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return []

    def save_high_score(self):
        """Salva a pontuação atual se for alta o suficiente"""
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]  # Mantém apenas os 5 melhores
        
        try:
            with open('high_scores.json', 'w') as f:
                json.dump(self.high_scores, f)
        except:
            pass

    def show_high_scores(self):
        """Mostra a tabela de high scores"""
        scores_text = "Maiores Pontuações:\n\n"
        for i, score in enumerate(self.high_scores, 1):
            scores_text += f"{i}. {score} pontos\n"
        messagebox.showinfo("High Scores", scores_text)

    def new_game(self):
        """Inicia um novo jogo"""
        self.rolls_left = 3
        self.current_dice = [1, 1, 1, 1, 1]
        self.dice_states = [False] * 5
        self.current_round = 1
        self.score = 0
        self.available_sequences = {seq: None for seq in self.available_sequences}
        
        # Atualizar interface
        self.update_ui()
        for i in range(5):
            self.dice_buttons[i].config(text="1", relief='raised')
            self.keep_buttons[i].config(text="Manter")

    def play_sound(self, sound_type):
        """Toca um efeito sonoro"""
        try:
            if sound_type == "roll":
                winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC)
            elif sound_type == "score":
                winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)
        except:
            pass

    def roll_dice(self):
        """Rola os dados não selecionados"""
        if self.rolls_left > 0:
            self.play_sound("roll")
            # Rola apenas os dados não travados
            for i in range(5):
                if not self.dice_states[i]:
                    value = random.randint(1, 6)
                    self.current_dice[i] = value
                    self.dice_buttons[i].config(text=str(value))
            
            self.rolls_left -= 1
            self.update_ui()
            
            # Verifica sequências apenas na última rolagem
            self.check_sequences()
            
            # Se acabaram as rolagens e não há sequências disponíveis
            if self.rolls_left == 0:
                has_available_sequence = False
                for seq, value in self.available_sequences.items():
                    if value is None and self.sequence_buttons[seq][0]['state'] == 'normal':
                        has_available_sequence = True
                        break
                
                if not has_available_sequence:
                    messagebox.showinfo("Nenhuma sequência disponível", 
                                      "Não há sequências disponíveis nesta rodada. Passando para a próxima rodada.")
                    self.next_round()

    def select_sequence(self, sequence):
        """Seleciona uma sequência e registra a pontuação"""
        if self.available_sequences[sequence] is None:
            value = sum(self.current_dice)
            self.available_sequences[sequence] = value
            self.score += value
            self.play_sound("score")
            
            # Atualizar interface
            self.score_label.config(text=f"Pontuação: {self.score}")
            btn, label = self.sequence_buttons[sequence]
            btn.config(state='disabled')
            label.config(text=f"{value} pontos")
            
            # Próxima rodada
            self.next_round()

    def next_round(self):
        """Prepara o jogo para a próxima rodada"""
        self.current_round += 1
        if self.current_round > 7:
            self.save_high_score()
            messagebox.showinfo("Fim do Jogo", 
                              f"Jogo terminado!\nPontuação final: {self.score}")
            self.new_game()
            return
        
        # Resetar para próxima rodada
        self.rolls_left = 3
        self.current_dice = [1, 1, 1, 1, 1]
        self.dice_states = [False] * 5
        
        # Atualizar interface
        self.update_ui()
        for i in range(5):
            self.dice_buttons[i].config(text="1", relief='raised')
            self.keep_buttons[i].config(text="Manter")

    def update_ui(self):
        """Atualiza elementos da interface"""
        self.roll_button.config(text=f"Rolar Dados ({self.rolls_left} tentativas)")
        self.round_label.config(text=f"Rodada: {self.current_round}/7")
        self.score_label.config(text=f"Pontuação: {self.score}")

    def toggle_dice(self, index):
        """Alterna o estado de seleção do dado"""
        if self.rolls_left < 3:  # Só permite selecionar após primeira rolagem
            self.dice_states[index] = not self.dice_states[index]
            if self.dice_states[index]:
                self.keep_buttons[index].config(text="Soltar")
                self.dice_buttons[index].config(relief='sunken')
            else:
                self.keep_buttons[index].config(text="Manter")
                self.dice_buttons[index].config(relief='raised')

    def check_sequences(self):
        """Verifica quais sequências estão disponíveis"""
        dice = sorted(self.current_dice)
        counts = {}
        for d in dice:
            counts[d] = counts.get(d, 0) + 1
        
        # Resetar labels
        for seq, (btn, label) in self.sequence_buttons.items():
            # Mostra a pontuação registrada se a sequência já foi usada
            if self.available_sequences[seq] is not None:
                label.config(text=f"{self.available_sequences[seq]} pontos")
            else:
                label.config(text="---")
        
        # Se não estiver na última rolagem, não mostra sequências disponíveis
        if self.rolls_left > 0:
            return
        
        # General (5 dados iguais)
        if max(counts.values()) == 5:
            value = sum(self.current_dice)
            if self.available_sequences["General"] is None:
                self.sequence_buttons["General"][1].config(text=f"{value} pontos")
                self.sequence_buttons["General"][0].config(state='normal')
                return
        
        # Quadra (4 dados iguais)
        if max(counts.values()) == 4:
            value = sum(self.current_dice)
            if self.available_sequences["Quadra"] is None:
                self.sequence_buttons["Quadra"][1].config(text=f"{value} pontos")
                self.sequence_buttons["Quadra"][0].config(state='normal')
                return
        
        # Full House (3 + 2)
        values = list(counts.values())
        if len(counts) == 2 and 2 in values and 3 in values:
            value = sum(self.current_dice)
            if self.available_sequences["Full House"] is None:
                self.sequence_buttons["Full House"][1].config(text=f"{value} pontos")
                self.sequence_buttons["Full House"][0].config(state='normal')
                return
        
        # Sequências
        if dice == [1,2,3,4,5]:
            value = sum(self.current_dice)
            if self.available_sequences["Sequência Baixa"] is None:
                self.sequence_buttons["Sequência Baixa"][1].config(text=f"{value} pontos")
                self.sequence_buttons["Sequência Baixa"][0].config(state='normal')
                return
        elif dice == [2,3,4,5,6]:
            value = sum(self.current_dice)
            if self.available_sequences["Sequência Alta"] is None:
                self.sequence_buttons["Sequência Alta"][1].config(text=f"{value} pontos")
                self.sequence_buttons["Sequência Alta"][0].config(state='normal')
                return
        
        # Trinca (3 dados iguais)
        if max(counts.values()) == 3:
            value = sum(self.current_dice)
            if self.available_sequences["Trinca"] is None:
                self.sequence_buttons["Trinca"][1].config(text=f"{value} pontos")
                self.sequence_buttons["Trinca"][0].config(state='normal')
                return
        
        # Par (2 dados iguais)
        if max(counts.values()) == 2:
            value = sum(self.current_dice)
            if self.available_sequences["Par"] is None:
                self.sequence_buttons["Par"][1].config(text=f"{value} pontos")
                self.sequence_buttons["Par"][0].config(state='normal')
                return

    def end_game(self):
        """Finaliza o jogo"""
        self.roll_button.config(state='disabled')
        for btn in self.keep_buttons:
            btn.config(state='disabled')
        
        messagebox.showinfo("Fim do Jogo",
                          f"Jogo terminado!\nPontuação final: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = GeneralGame(root)
    root.mainloop()