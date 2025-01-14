# Importação das bibliotecas necessárias
import tkinter as tk  # Biblioteca para criar a interface gráfica
from tkinter import messagebox  # Módulo para exibir mensagens em janelas pop-up
import random  # Biblioteca para gerar números aleatórios
import os  # Biblioteca para operações do sistema operacional

class CartelaBingo:
    def __init__(self, master):
        """
        Inicializa a interface da cartela de Bingo.
        
        Parâmetros:
            master: Janela principal do Tkinter
        """
        # Configuração da janela principal
        self.master = master
        self.master.title("Bingo Game - SENAC")
        
        # Criação do frame para o título
        self.frame_logo = tk.Frame(master)
        self.frame_logo.pack(pady=10)
        
        # Criação do título do jogo
        self.criar_titulo()
        
        # Configuração do layout principal
        self.frame_principal = tk.Frame(master)
        self.frame_principal.pack(padx=10, pady=10)
        
        # Frame para a cartela do bingo
        self.frame_cartela = tk.Frame(self.frame_principal)
        self.frame_cartela.pack(side=tk.LEFT, padx=10)
        
        # Frame para os controles e números sorteados
        self.frame_controles = tk.Frame(self.frame_principal)
        self.frame_controles.pack(side=tk.LEFT, padx=10)
        
        # Inicialização das variáveis do jogo
        self.numeros_sorteados = []  # Lista para armazenar números já sorteados
        self.labels_numeros = {}  # Dicionário para armazenar referências aos labels dos números
        self.numeros_cartela = {}  # Dicionário para controlar números marcados
        
        # Criação dos elementos da interface
        self.criar_cartela()
        self.criar_controles()
        
    def criar_titulo(self):
        """
        Cria um título estilizado para o jogo
        """
        # Criação do label do título com estilização
        titulo = tk.Label(
            self.frame_logo,
            text="BINGO SENAC",
            font=('Helvetica', 24, 'bold'),
            fg='blue'
        )
        titulo.pack(pady=10)
        
    def criar_cartela(self):
        """
        Gera a cartela de Bingo com números aleatórios e exibe na interface.
        """
        # Geração dos números aleatórios para cada coluna (B-I-N-G-O)
        colunas = {
            'B': random.sample(range(1, 16), 5),    # Números de 1 a 15
            'I': random.sample(range(16, 31), 5),   # Números de 16 a 30
            'N': random.sample(range(31, 46), 5),   # Números de 31 a 45
            'G': random.sample(range(46, 61), 5),   # Números de 46 a 60
            'O': random.sample(range(61, 76), 5)    # Números de 61 a 75
        }

        # Definição do espaço central como "LIVRE"
        colunas['N'][2] = "LIVRE"

        # Criação dos labels para as letras B-I-N-G-O
        for idx, letra in enumerate("BINGO"):
            tk.Label(self.frame_cartela, text=letra, font=('Helvetica', 16, 'bold')).grid(row=0, column=idx)

        # Criação dos labels para os números da cartela
        for col_idx, letra in enumerate("BINGO"):
            for row_idx, numero in enumerate(colunas[letra]):
                # Criação do label com estilização
                label = tk.Label(
                    self.frame_cartela,
                    text=numero,
                    font=('Helvetica', 14),
                    width=5,
                    height=2,
                    borderwidth=2,
                    relief="groove",
                    bg='white'
                )
                label.grid(row=row_idx + 1, column=col_idx)
                # Armazenamento das referências dos labels, exceto para o espaço "LIVRE"
                if numero != "LIVRE":
                    self.labels_numeros[numero] = label
                    self.numeros_cartela[numero] = False

    def criar_controles(self):
        """
        Cria os controles do jogo e área de exibição dos números sorteados.
        """
        # Criação do botão de sorteio
        self.btn_sortear = tk.Button(
            self.frame_controles,
            text="Sortear Número",
            command=self.sortear_numero,
            font=('Helvetica', 12),
            bg='lightblue'
        )
        self.btn_sortear.pack(pady=10)

        # Label para mostrar o último número sorteado
        self.lbl_ultimo_sorteado = tk.Label(
            self.frame_controles,
            text="Último número:",
            font=('Helvetica', 12)
        )
        self.lbl_ultimo_sorteado.pack(pady=5)

        # Frame para lista de números sorteados
        self.frame_numeros = tk.Frame(self.frame_controles)
        self.frame_numeros.pack(pady=10)
        
        # Label para título da lista de números sorteados
        tk.Label(
            self.frame_numeros,
            text="Números Sorteados:",
            font=('Helvetica', 12)
        ).pack()

        # Lista para exibir números sorteados
        self.lista_sorteados = tk.Listbox(
            self.frame_numeros,
            width=20,
            height=10,
            font=('Helvetica', 10)
        )
        self.lista_sorteados.pack()

    def sortear_numero(self):
        """
        Sorteia um novo número e atualiza a interface.
        """
        # Verifica se ainda existem números disponíveis para sorteio
        numeros_disponiveis = set(range(1, 76)) - set(self.numeros_sorteados)
        
        # Se não houver mais números disponíveis, exibe mensagem e encerra
        if not numeros_disponiveis:
            messagebox.showinfo("Fim do Jogo", "Todos os números já foram sorteados!")
            return

        # Sorteia um novo número dentre os disponíveis
        numero = random.choice(list(numeros_disponiveis))
        self.numeros_sorteados.append(numero)
        
        # Atualiza o label com o último número sorteado
        self.lbl_ultimo_sorteado.config(text=f"Último número: {numero}")
        
        # Adiciona o número à lista de sorteados
        self.lista_sorteados.insert(0, str(numero))
        
        # Se o número estiver na cartela, marca ele
        if numero in self.labels_numeros:
            self.labels_numeros[numero].config(bg='lightgreen')
            self.numeros_cartela[numero] = True
            
            # Verifica se o jogador ganhou
            if self.verificar_vitoria():
                messagebox.showinfo("BINGO!", "Parabéns! Você completou a cartela!")
                self.btn_sortear.config(state='disabled')

    def verificar_vitoria(self):
        """
        Verifica se todos os números da cartela foram marcados.
        """
        return all(self.numeros_cartela.values())

# Inicialização do jogo
if __name__ == "__main__":
    root = tk.Tk()  # Cria a janela principal
    app = CartelaBingo(root)  # Inicializa o jogo
    root.mainloop()  # Inicia o loop principal da interface gráfica