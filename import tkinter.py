import tkinter as tk

root = tk.Tk()
root.title('Minha Primeira Janela Tkinter')
root.geometry('400x300')
root.configure(bg='lightblue')

label = tk.Label(root, text= 'Digite seu nome', font=('Arial', 14), bg='lightblue')
label.pack(pady=10)

root.mainloop()