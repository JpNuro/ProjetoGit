import tkinter as tk
from tkinter import ttk, messagebox
import random

class AmigoSecreto:
    def __init__(self, root):
        self.root = root
        self.root.title("Amigo Secreto")
        self.root.geometry("600x400")

        # Lista para armazenar participantes
        self.participantes = []
        
        # Valores padrão para preços
        self.preco_minimo = tk.StringVar(value="0")
        self.preco_maximo = tk.StringVar(value="100")

        # Criar notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        # Criar as abas
        self.tab_cadastro = ttk.Frame(self.notebook)
        self.tab_config = ttk.Frame(self.notebook)
        self.tab_sorteio = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_cadastro, text='Cadastro')
        self.notebook.add(self.tab_config, text='Configurações')
        self.notebook.add(self.tab_sorteio, text='Sorteio')

        self.setup_cadastro()
        self.setup_config()
        self.setup_sorteio()

    def setup_cadastro(self):
        # Frame para entrada de dados
        frame_cadastro = ttk.LabelFrame(self.tab_cadastro, text="Cadastro de Participante")
        frame_cadastro.pack(padx=10, pady=10, fill='x')

        # Campos de entrada
        ttk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = ttk.Entry(frame_cadastro)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_cadastro, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(frame_cadastro)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_cadastro, text="Sugestão de Presente:").grid(row=2, column=0, padx=5, pady=5)
        self.sugestao_entry = ttk.Entry(frame_cadastro)
        self.sugestao_entry.grid(row=2, column=1, padx=5, pady=5)

        # Botão de cadastro
        ttk.Button(frame_cadastro, text="Cadastrar", command=self.cadastrar_participante).grid(row=3, column=0, columnspan=2, pady=10)

        # Lista de participantes
        frame_lista = ttk.LabelFrame(self.tab_cadastro, text="Participantes Cadastrados")
        frame_lista.pack(padx=10, pady=10, fill='both', expand=True)

        self.lista_participantes = tk.Listbox(frame_lista)
        self.lista_participantes.pack(padx=5, pady=5, fill='both', expand=True)

    def setup_config(self):
        frame_config = ttk.LabelFrame(self.tab_config, text="Configurações de Preço")
        frame_config.pack(padx=10, pady=10, fill='x')

        ttk.Label(frame_config, text="Preço Mínimo (R$):").grid(row=0, column=0, padx=5, pady=5)
        self.preco_min_entry = ttk.Entry(frame_config, textvariable=self.preco_minimo)
        self.preco_min_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_config, text="Preço Máximo (R$):").grid(row=1, column=0, padx=5, pady=5)
        self.preco_max_entry = ttk.Entry(frame_config, textvariable=self.preco_maximo)
        self.preco_max_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_config, text="Salvar Configurações", command=self.salvar_config).grid(row=2, column=0, columnspan=2, pady=10)

    def setup_sorteio(self):
        frame_sorteio = ttk.Frame(self.tab_sorteio)
        frame_sorteio.pack(padx=10, pady=10, fill='both', expand=True)

        ttk.Button(frame_sorteio, text="Realizar Sorteio", command=self.realizar_sorteio).pack(pady=20)
        
        # Área para mostrar resultados
        self.resultado_text = tk.Text(frame_sorteio, height=10, width=50)
        self.resultado_text.pack(padx=5, pady=5, fill='both', expand=True)

    def cadastrar_participante(self):
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().strip()
        sugestao = self.sugestao_entry.get().strip()

        if nome and email and sugestao:
            participante = {
                'nome': nome,
                'email': email,
                'sugestao': sugestao
            }
            self.participantes.append(participante)
            self.lista_participantes.insert(tk.END, f"{nome} ({email})")
            
            # Limpar campos
            self.nome_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.sugestao_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")

    def salvar_config(self):
        try:
            min_preco = float(self.preco_minimo.get())
            max_preco = float(self.preco_maximo.get())
            
            if min_preco >= max_preco:
                messagebox.showerror("Erro", "O preço mínimo deve ser menor que o preço máximo!")
                return
                
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos!")

    def realizar_sorteio(self):
        if len(self.participantes) < 2:
            messagebox.showwarning("Aviso", "É necessário ter pelo menos 2 participantes para realizar o sorteio!")
            return

        # Criar uma cópia da lista de participantes para o sorteio
        sorteados = self.participantes.copy()
        resultado = []
        
        # Para cada participante, sortear um amigo secreto
        for i in range(len(self.participantes)):
            sorteador = self.participantes[i]
            # Remover o próprio participante da lista de possíveis sorteados
            possiveis_sorteados = [p for p in sorteados if p != sorteador]
            
            if not possiveis_sorteados:
                # Se não há possíveis sorteados, reiniciar o sorteio
                self.realizar_sorteio()
                return
                
            sorteado = random.choice(possiveis_sorteados)
            resultado.append((sorteador, sorteado))
            sorteados.remove(sorteado)

        # Mostrar resultados
        self.resultado_text.delete(1.0, tk.END)
        for sorteador, sorteado in resultado:
            self.resultado_text.insert(tk.END, 
                f"\n{sorteador['nome']} tirou {sorteado['nome']}\n"
                f"Sugestão de presente: {sorteado['sugestao']}\n"
                f"Email para contato: {sorteado['email']}\n"
                f"{'='*50}\n")

if __name__ == '__main__':
    root = tk.Tk()
    app = AmigoSecreto(root)
    root.mainloop()