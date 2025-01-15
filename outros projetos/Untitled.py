# Widgets for the GUI

import tkinter as tk

root = tk.Tk()
root.title('Minha janela interativa')
root.geometry('1280x720')
root.configure(bg='lightblue')

label = tk.Label(root, text='Bem-vindo ao Tkinter!', font=('Arial', 16), bg='white', fg='blue')
label.pack(pady=200)

entrada = tk.Entry(root, font=('Arial', 14))
entrada.pack(pady=10)

def exibir_texto():
    texto = entrada.get()
    print(f'Você digitou {texto}')

botao_exibir = tk.Button(root, text='Exibir Texto', font=('Arial', 14), bg='blue', fg='white', command=exibir_texto)
botao_exibir.pack(pady=10)

root.mainloop()