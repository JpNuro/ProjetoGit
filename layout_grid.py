import tkinter as tk

def criar_interface_com_grid():
    janela_grid = tk.Tk()
    janela_grid.title("Interface Grid")
    janela_grid.geometry("400x400")

    tk.Label(janela_grid, text="Row 0, Column 0", bg="red", fg="white").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(janela_grid, text="Row 0, Column 1", bg="green", fg="white").grid(row=0, column=1, padx=5, pady=5)
    tk.Label(janela_grid, text="Row 1, Column 0", bg="blue", fg="white").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(janela_grid, text="Row 1, Column 1", bg="yellow", fg="black").grid(row=1, column=1, padx=5, pady=5)

    tk.Button(janela_grid, text="Fechar", command=janela_grid.destroy).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    
    return janela_grid

if __name__ == "__main__":
    janela = criar_interface_com_grid()
    janela.mainloop()