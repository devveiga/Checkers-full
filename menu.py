import tkinter as tk
from tkinter import colorchooser, messagebox
from placar import ler_melhor_tempo

TAM_CASA = 40  # tamanho da casa para o preview no menu

class MenuDamas:
    def __init__(self, root, iniciar_jogo_callback=None):
        self.root = root
        self.iniciar_jogo_callback = iniciar_jogo_callback

        self.cor_peca = "#ff0000"
        self.cor_dama = "#ffd700"

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()

        tk.Label(self.frame, text="🎮 Bem-vindo ao Jogo de Damas!", font=("Arial", 16)).pack(pady=10)

        # Canvas para peças de exemplo
        self.canvas_exemplo = tk.Canvas(self.frame, width=2 * TAM_CASA + 40, height=TAM_CASA + 20)
        self.canvas_exemplo.pack(pady=10)
        self.desenhar_exemplo()

        tk.Button(self.frame, text="Selecionar cor da peça", command=self.selecionar_cor_peca).pack(pady=5)
        tk.Button(self.frame, text="Selecionar cor da dama", command=self.selecionar_cor_dama).pack(pady=5)

        tk.Button(self.frame, text="Iniciar Jogo", command=self.iniciar_jogo).pack(pady=15)

        # Botão para mostrar o melhor tempo
        tk.Button(self.frame, text="Consultar Melhor Resultado", command=self.mostrar_melhor_tempo).pack(pady=5)

    def desenhar_exemplo(self):
        self.canvas_exemplo.delete("all")
        raio = 15
        x1 = 20 + TAM_CASA // 2
        y1 = TAM_CASA // 2 + 10
        self.canvas_exemplo.create_oval(x1 - raio, y1 - raio, x1 + raio, y1 + raio,
                                        fill=self.cor_peca, outline="black", width=2)
        self.canvas_exemplo.create_text(x1, y1 + 25, text="Peça normal")

        raio_dama = 20
        x2 = x1 + TAM_CASA + 20
        y2 = y1
        self.canvas_exemplo.create_oval(x2 - raio_dama, y2 - raio_dama, x2 + raio_dama, y2 + raio_dama,
                                        fill=self.cor_dama, outline="black", width=2)
        self.canvas_exemplo.create_oval(x2 - 7, y2 - 7, x2 - 2, y2 - 2,
                                        fill="white", outline="")
        self.canvas_exemplo.create_text(x2, y2 + 25, text="Dama")

    def selecionar_cor_peca(self):
        cor = colorchooser.askcolor(title="Escolha a cor da sua peça")[1]
        if cor:
            self.cor_peca = cor
            self.desenhar_exemplo()

    def selecionar_cor_dama(self):
        cor = colorchooser.askcolor(title="Escolha a cor da sua dama")[1]
        if cor:
            self.cor_dama = cor
            self.desenhar_exemplo()

    def iniciar_jogo(self):
        if self.iniciar_jogo_callback:
            self.iniciar_jogo_callback(self.cor_peca, self.cor_dama)
        else:
            import ui_tkinter
            self.frame.destroy()
            ui_tkinter.iniciar_com_personalizacao(self.root, self.cor_peca, self.cor_dama)

    def mostrar_melhor_tempo(self):
        melhor_tempo = ler_melhor_tempo()
        if melhor_tempo is not None:
            messagebox.showinfo("Melhor Resultado", f"O melhor tempo registrado é {melhor_tempo} segundos.")
        else:
            messagebox.showinfo("Melhor Resultado", "Nenhum tempo registrado ainda.")
