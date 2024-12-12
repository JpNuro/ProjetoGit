import tkinter as tk


def exibir_texto():
    texto = entrada.get()
    print(f'VocÊ digitou: {texto}')

def limpar_texto():
    entrada.delete(0, tk.END)

root = tk.Tk()
root.title('Interface Básica com Tkinter')
root.geometry('400x300')
root.configure(bg = 'lightblue')

label = tk.Label(root, text= 'Digite seu nome', font=('Arial', 14), bg='lightblue')
label.pack(pady=10)

entrada = tk.Entry(root, font=('Arial', 14))
entrada.pack(pady=10)

botao = tk.Button(root, text='Enviar', font=('Arial', 14), bg='green', fg='white', command=exibir_texto)
botao.pack(pady=10)

frame_botoes = tk.Frame(root, bg='lightblue')
frame_botoes.pack(pady=10)

botao_enviar = tk.Button(frame_botoes, text="Enviar", font=("Arial", 14), bg="blue", fg="white", command=exibir_texto)
botao_enviar.pack(side=tk.LEFT, padx=5)

botao_limpar = tk.Button(frame_botoes, text="Limpar", font=("Arial", 14), bg="red", fg="white", command=limpar_texto)
botao_limpar.pack(side=tk.LEFT, padx=5)

root.mainloop()