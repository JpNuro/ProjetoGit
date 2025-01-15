import tkinter as tk

# def exibir_janela():
#     janela = tk.Tk()
#     janela.title("Exibir Labels")
#     janela.geometry("300x300")
#     janela.configure(bg='pink')

#     # Usando pack - TÍTULO
#     label1 = tk.Label(janela, text='Janela Exibida 👍', font=('Arial', 18), bg='pink', fg='white')
#     label1.pack(pady=10)

#     entrada = tk.Entry(janela, font=('Arial', 14))
#     entrada.pack(pady=10)

#     # Usando grid - TABELA DE INFORMAÇÕES
#     frame1 = tk.Frame(janela, bg='pink')
#     tk.Label(frame1, text='Faz uma pergunta que eu respondo 👍', font=('Arial', 14), bg='purple', fg='black').grid(row=0, column=0, padx=5, pady=5)


#     # Usando place - BOTÕES
#     tk.Button(janela, text='Fechar', font=('Arial', 14), bg='red', fg='white', command=janela.destroy).place(x=127, y=200)

#     return janela

# if __name__ == "__main__":
#     janela = exibir_janela()
#     janela.mainloop()





def mudar_label():
    label4.config(text="Não")

# Criação da janela principal
root = tk.Tk()
root.title("Janela Principal")
root.geometry("500x500")
root.configure(bg="lightgray")

# Frame usando "pack"
frame1 = tk.Frame(root, bg="lightgray")
frame1.pack(side="top", fill="x")

label1 = tk.Label(frame1, text="Usando pack()", font=("Arial", 18), bg="lightgray", fg="black")
label1.pack(pady=10)

# Frame usando "grid"
frame2 = tk.Frame(root, bg="lightgray")
frame2.pack(side="top", fill="both", expand=True)

label2 = tk.Label(frame2, text="Usando grid()", font=("Arial", 14), bg="white", fg="black")
label3 = tk.Label(frame2, text="Outra label com grid()", font=("Arial", 14), bg="black", fg="white")
label2.grid(row=0, column=0, padx=10, pady=10)
label3.grid(row=1, column=0, padx=10, pady=10)

# Frame com Entry fds
entry = tk.Entry(frame2, font=("Arial", 14))
entry.grid(row=2, column=0, padx=10, pady=10)
label4 = tk.Label(frame2, text="", font=("Arial", 14), bg="lightgray", fg="black")
label4.grid(row=3, column=0, padx=10, pady=10)

# Botão usando "place"
button = tk.Button(root, text="Usando place()", font=("Arial", 14), bg="lightgray", fg="black", command=mudar_label)
button.place(x=175, y=200)

# Executando a janela
root.mainloop()