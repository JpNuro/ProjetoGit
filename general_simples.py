import tkinter as tk
from tkinter import messagebox
import random

def criar_janela():
    """Cria a janela principal do jogo"""
    janela = tk.Tk()
    janela.title("Jogo de General")
    janela.geometry("600x800")
    return janela

def criar_dados(frame):
    """Cria os dados e botões de reserva"""
    # Lista para guardar os valores dos dados
    dados = [1, 1, 1, 1, 1]
    # Lista para controlar quais dados estão reservados (True = reservado)
    dados_reservados = [False, False, False, False, False]
    # Lista para guardar os labels dos dados
    labels_dados = []
    # Lista para guardar os botões de reserva
    botoes_reserva = []

    # Criar frame para cada dado
    for i in range(5):
        frame_dado = tk.Frame(frame)
        frame_dado.pack(side=tk.LEFT, padx=10)

        # Label para mostrar o valor do dado
        label = tk.Label(frame_dado, text="1", font=('Arial', 24), width=2, relief='raised')
        label.pack(pady=5)
        labels_dados.append(label)

        # Botão para reservar o dado
        botao = tk.Button(frame_dado, text="Reservar")
        botao.pack()
        botoes_reserva.append(botao)

    return dados, dados_reservados, labels_dados, botoes_reserva

def criar_interface():
    """Cria toda a interface do jogo"""
    janela = criar_janela()
    
    # Variáveis do jogo
    jogadas_restantes = 3
    rodada_atual = 1
    pontuacao = 0
    
    # Dicionário para controlar as sequências disponíveis
    sequencias = {
        "General": None,
        "Quadra": None,
        "Full House": None,
        "Sequência Alta": None,
        "Sequência Baixa": None,
        "Trinca": None,
        "Par": None
    }

    # Frame principal
    frame_principal = tk.Frame(janela, padx=20, pady=20)
    frame_principal.pack(expand=True, fill='both')

    # Frame para os dados
    frame_dados = tk.LabelFrame(frame_principal, text="Dados", padx=10, pady=10)
    frame_dados.pack(fill='x', pady=(0, 20))

    # Criar dados e seus controles
    dados, dados_reservados, labels_dados, botoes_reserva = criar_dados(frame_dados)

    # Frame para informações do jogo
    frame_info = tk.LabelFrame(frame_principal, text="Status do Jogo", padx=10, pady=10)
    frame_info.pack(fill='x', pady=(0, 20))

    # Labels para mostrar informações do jogo
    label_rodada = tk.Label(frame_info, text=f"Rodada: {rodada_atual}/7")
    label_rodada.pack(side=tk.LEFT, padx=5)

    label_pontos = tk.Label(frame_info, text=f"Pontuação: {pontuacao}")
    label_pontos.pack(side=tk.RIGHT, padx=5)

    # Frame para sequências
    frame_sequencias = tk.LabelFrame(frame_principal, text="Sequências", padx=10, pady=10)
    frame_sequencias.pack(fill='both', expand=True)

    # Dicionário para guardar os botões e labels das sequências
    botoes_sequencias = {}
    
    # Criar botões e labels para cada sequência
    for seq in sequencias.keys():
        frame_seq = tk.Frame(frame_sequencias)
        frame_seq.pack(fill='x', pady=2)
        
        # Botão da sequência (começa desativado)
        botao = tk.Button(frame_seq, text=seq, state='disabled')
        botao.pack(side=tk.LEFT, padx=5)
        
        # Label para mostrar pontos possíveis
        label = tk.Label(frame_seq, text="---")
        label.pack(side=tk.RIGHT, padx=5)
        
        # Guarda o botão e label no dicionário
        botoes_sequencias[seq] = (botao, label)

    def reservar_dado(indice):
        """Função para reservar/liberar um dado"""
        dados_reservados[indice] = not dados_reservados[indice]
        if dados_reservados[indice]:
            botoes_reserva[indice].config(text="Liberar")
            labels_dados[indice].config(relief='sunken')
        else:
            botoes_reserva[indice].config(text="Reservar")
            labels_dados[indice].config(relief='raised')

    def verificar_sequencias():
        """Verifica quais sequências são possíveis com os dados atuais"""
        # Se ainda não rolou os dados nesta rodada, não mostra sequências
        if jogadas_restantes == 3:
            return
            
        # Ordenar dados para facilitar verificação
        dados_ordenados = sorted(dados)
        
        # Contar quantidade de cada número
        contagem = {}
        for d in dados_ordenados:
            contagem[d] = contagem.get(d, 0) + 1
        
        # Maior quantidade de números iguais
        maior_contagem = max(contagem.values())
        
        # Resetar todos os botões e labels
        for seq, (botao, label) in botoes_sequencias.items():
            if sequencias[seq] is None:  # Se a sequência ainda não foi usada
                botao.config(state='disabled')
                label.config(text="---")
            else:  # Se já foi usada, mantém a pontuação visível
                label.config(text=f"{sequencias[seq]} pontos")
        
        # Se não for a última jogada, não mostra sequências disponíveis
        if jogadas_restantes > 0:
            return
            
        # Soma dos dados para pontuação
        soma = sum(dados)
        
        # Verificar cada sequência possível
        if maior_contagem == 5 and sequencias["General"] is None:
            botoes_sequencias["General"][0].config(state='normal')
            botoes_sequencias["General"][1].config(text=f"{soma} pontos")
            
        if maior_contagem >= 4 and sequencias["Quadra"] is None:
            botoes_sequencias["Quadra"][0].config(state='normal')
            botoes_sequencias["Quadra"][1].config(text=f"{soma} pontos")
            
        valores = list(contagem.values())
        if len(contagem) == 2 and 2 in valores and 3 in valores and sequencias["Full House"] is None:
            botoes_sequencias["Full House"][0].config(state='normal')
            botoes_sequencias["Full House"][1].config(text=f"{soma} pontos")
            
        if dados_ordenados == [1,2,3,4,5] and sequencias["Sequência Baixa"] is None:
            botoes_sequencias["Sequência Baixa"][0].config(state='normal')
            botoes_sequencias["Sequência Baixa"][1].config(text=f"{soma} pontos")
            
        if dados_ordenados == [2,3,4,5,6] and sequencias["Sequência Alta"] is None:
            botoes_sequencias["Sequência Alta"][0].config(state='normal')
            botoes_sequencias["Sequência Alta"][1].config(text=f"{soma} pontos")
            
        if maior_contagem >= 3 and sequencias["Trinca"] is None:
            botoes_sequencias["Trinca"][0].config(state='normal')
            botoes_sequencias["Trinca"][1].config(text=f"{soma} pontos")
            
        if maior_contagem >= 2 and sequencias["Par"] is None:
            botoes_sequencias["Par"][0].config(state='normal')
            botoes_sequencias["Par"][1].config(text=f"{soma} pontos")

    def proxima_rodada():
        """Prepara o jogo para a próxima rodada"""
        nonlocal jogadas_restantes, rodada_atual
        
        rodada_atual += 1
        if rodada_atual > 7:
            messagebox.showinfo("Fim do Jogo", f"Jogo terminado! Pontuação final: {pontuacao}")
            janela.quit()
            return
            
        # Resetar jogadas e dados
        jogadas_restantes = 3
        for i in range(5):
            dados[i] = 1
            dados_reservados[i] = False
            labels_dados[i].config(text="1", relief='raised')
            botoes_reserva[i].config(text="Reservar")
            
        # Atualizar interface
        botao_rolar.config(text=f"Rolar Dados ({jogadas_restantes})")
        label_rodada.config(text=f"Rodada: {rodada_atual}/7")
        
        # Resetar sequências disponíveis
        verificar_sequencias()

    def registrar_sequencia(sequencia):
        """Registra a pontuação de uma sequência"""
        nonlocal pontuacao
        
        # Só permite registrar se não houver mais jogadas
        if jogadas_restantes > 0:
            return
            
        # Calcula pontos
        pontos = sum(dados)
        sequencias[sequencia] = pontos
        pontuacao += pontos
        
        # Atualiza interface
        label_pontos.config(text=f"Pontuação: {pontuacao}")
        botoes_sequencias[sequencia][1].config(text=f"{pontos} pontos")
        
        # Desativa o botão da sequência usada
        botoes_sequencias[sequencia][0].config(state='disabled')
        
        # Vai para próxima rodada
        proxima_rodada()

    def rolar_dados():
        """Rola os dados não reservados"""
        nonlocal jogadas_restantes
        
        if jogadas_restantes > 0:
            # Rola apenas dados não reservados
            for i in range(5):
                if not dados_reservados[i]:
                    dados[i] = random.randint(1, 6)
                    labels_dados[i].config(text=str(dados[i]))
            
            jogadas_restantes -= 1
            botao_rolar.config(text=f"Rolar Dados ({jogadas_restantes})")
            
            # Verifica sequências possíveis
            verificar_sequencias()
            
            # Se acabaram as jogadas, verifica se há sequências disponíveis
            if jogadas_restantes == 0:
                tem_sequencia = False
                for seq in sequencias:
                    if sequencias[seq] is None and botoes_sequencias[seq][0]['state'] == 'normal':
                        tem_sequencia = True
                        break
                
                if not tem_sequencia:
                    if messagebox.askyesno("Sem sequências", 
                                         "Não há sequências disponíveis. Deseja ir para a próxima rodada?"):
                        proxima_rodada()

    # Configurar botões de reserva
    for i in range(5):
        botoes_reserva[i].config(command=lambda x=i: reservar_dado(x))

    # Configurar botões de sequência
    for seq in sequencias:
        botoes_sequencias[seq][0].config(command=lambda s=seq: registrar_sequencia(s))

    # Botão para rolar dados
    botao_rolar = tk.Button(frame_dados, text=f"Rolar Dados ({jogadas_restantes})", 
                           command=rolar_dados)
    botao_rolar.pack(pady=10)

    return janela

# Iniciar o jogo
if __name__ == "__main__":
    janela_jogo = criar_interface()
    janela_jogo.mainloop()
