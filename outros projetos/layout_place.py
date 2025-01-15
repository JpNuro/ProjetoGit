import tkinter as tk

def criar_interface_place():
    janela_place = tk.Tk()
    janela_place.title("Gerenciador place() 📍")
    janela_place.geometry("300x300")
    janela_place.configure(bg='lightblue')

    tk.Label(janela_place, text="Posição Absoluta", bg="orange", fg="black").place(x=50, y=50, width=200, height=30)
    tk.Label(janela_place, text="Outro Widget", bg="cyan", fg="black").place(x=50, y=100, width=200, height=30)

    tk.Button(janela_place, text="Fechar", command=janela_place.destroy).place(x=127, y=200)


    return janela_place

if __name__ == "__main__":
    janela = criar_interface_place()
    janela.mainloop()