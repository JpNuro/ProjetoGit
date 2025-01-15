import tkinter as tk
from tkinter import font
import random

def create_bingo_card(frame, size=5, number_range=(1, 75)):
    numbers = random.sample(range(*number_range), size * size - 1)  # Retira 1 para o "livre"
    index = 0
    for i in range(size):
        for j in range(size):
            if i == size // 2 and j == size // 2:  # Centro "livre"
                button = tk.Button(frame, text="FREE", state="disabled", bg="lightgray", width=5, height=2)
            else:
                button = tk.Button(frame, text=numbers[index], bg="white", width=5, height=2)
                index += 1
            button.grid(row=i, column=j, padx=5, pady=5)

def update_drawn_numbers(frame, number):
    label = tk.Label(frame, text=str(number), bg="white", width=5, height=2, borderwidth=2, relief="solid")
    label.pack(side=tk.LEFT, padx=5)

def main():
    # Criação da janela principal
    root = tk.Tk()
    root.title("BINGO!!")
    root.geometry("800x600")  # Tamanho inicial da janela
    root.configure(bg="lightblue")

    # Título do Jogo
    title_font = font.Font(family="Arial Black", size=24, weight="bold")
    title_label = tk.Label(root, text="BINGO!!", font=title_font, bg="lightblue", fg="darkred")
    title_label.pack(pady=10)

    # Frame para números sorteados
    drawn_numbers_frame = tk.Frame(root, bg="white", height=100, width=600)
    drawn_numbers_frame.pack(pady=10)
    drawn_numbers_frame.pack_propagate(False)  # Evita redimensionamento automático

    # Retângulo para informações
    info_frame = tk.Frame(root, bg="gray", height=400, width=200)
    info_frame.pack(side=tk.LEFT, padx=10)
    info_frame.pack_propagate(False)

    # Frame da cartela
    card_frame = tk.Frame(root, bg="white", height=300, width=600)
    card_frame.pack(side=tk.BOTTOM, pady=10)
    card_frame.pack_propagate(False)

    create_bingo_card(card_frame)

    root.mainloop()

if __name__ == "__main__":
    main()