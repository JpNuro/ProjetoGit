import tkinter as tk

root = tk.Tk()
root.title('Interface de Usuário')
root.geometry('400x300')
root.configure(bg = 'lightpink')

def exibir_idade():
    idade = entrada_idade.get()
    print(idade)

def limpar_idade():
	entrada_idade.delete(0, tk.END)

label = tk.Label(root, text='Digite sua idade:', font=('Arial', 14), bg='lightpink')
label.pack(pady=10)

entrada_idade = tk.Entry(root, font=('Arial', 14))
entrada_idade.pack(pady=10)

frame_botoes = tk.Frame(root, bg='lightpink')
frame_botoes.pack(pady=10)

botao_exibir = tk.Button(frame_botoes, text='Exibir', font=('Arial', 14), bg='purple', fg='white', command=exibir_idade)
botao_exibir.pack(side=tk.LEFT, padx=5)

botao_limpar = tk.Button(frame_botoes, text='Limpar', font=('Arial', 14), bg='purple', fg='white', command=limpar_idade)
botao_limpar.pack(side=tk.LEFT, padx=5)

root.mainloop()