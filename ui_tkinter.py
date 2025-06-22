import tkinter as tk
import time
from logica_dama import LogicaDama
from placar import salvar_tempo

TAM_CASA = 60
TAM = 8

class DamasApp:
    def __init__(self, root, cor_peca="#ff0000", cor_dama="#ffd700", voltar_menu_callback=None):
        self.root = root
        self.root.title("Jogo de Damas")
        self.voltar_menu_callback = voltar_menu_callback
        self.cor_peca = cor_peca
        self.cor_dama = cor_dama
        
        # Cria o frame container antes de qualquer widget
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Canvas dentro do frame
        self.canvas = tk.Canvas(self.frame, width=TAM * TAM_CASA, height=TAM * TAM_CASA)
        self.canvas.pack()

        self.jogo = LogicaDama()
        self.peca_selecionada = None
        self.inicio = time.time()

        self.canvas.bind("<Button-1>", self.selecionar)
        self.desenhar_tabuleiro()

        # Variável para controlar se já criou o botão voltar
        self.botao_voltar = None

    def desenhar_tabuleiro(self):
        self.canvas.delete("all")
        for y in range(TAM):
            for x in range(TAM):
                cor_casa = "white" if (x + y) % 2 == 0 else "gray"
                if self.peca_selecionada == (x, y):
                    cor_casa = "#555555"
                self.canvas.create_rectangle(x * TAM_CASA, y * TAM_CASA,
                                             (x + 1) * TAM_CASA, (y + 1) * TAM_CASA,
                                             fill=cor_casa)

                peca = self.jogo.tabuleiro[y][x]
                if peca != 0:
                    cor_peca = "black"
                    raio = 20

                    if peca == 1:
                        cor_peca = self.cor_peca
                    elif peca == 2:
                        cor_peca = "black"
                    elif peca == 3:
                        cor_peca = self.cor_dama
                        raio = 25
                    elif peca == 4:
                        cor_peca = "cyan"
                        raio = 25

                    self.canvas.create_oval(x * TAM_CASA + TAM_CASA // 2 - raio,
                                            y * TAM_CASA + TAM_CASA // 2 - raio,
                                            x * TAM_CASA + TAM_CASA // 2 + raio,
                                            y * TAM_CASA + TAM_CASA // 2 + raio,
                                            fill=cor_peca)

    def selecionar(self, event):
        x = event.x // TAM_CASA
        y = event.y // TAM_CASA

        if self.peca_selecionada:
            x1, y1 = self.peca_selecionada
            if self.jogo.movimento_valido(x1, y1, x, y, 1):
                self.jogo.movimentar(x1, y1, x, y)
                self.peca_selecionada = None
                self.desenhar_tabuleiro()
                self.root.after(500, self.jogada_ia)
                self.verificar_vitoria()
            else:
                self.peca_selecionada = None
        elif self.jogo.tabuleiro[y][x] in [1, 3]:
            self.peca_selecionada = (x, y)

        self.desenhar_tabuleiro()

    def jogada_ia(self):
        if self.jogo.turno_jogador:
            return
        self.jogo.movimento_ia()
        self.desenhar_tabuleiro()
        self.verificar_vitoria()

    def verificar_vitoria(self):
        status = self.jogo.status_jogo()
        if status in ["vitoria", "derrota"]:
            fim = time.time()
            duracao = round(fim - self.inicio)
            if status == "vitoria":
                salvar_tempo(duracao)
                msg = f"Você venceu em {duracao} segundos!"
            else:
                msg = "Você perdeu!"

            self.canvas.unbind("<Button-1>")
            self.canvas.create_text(TAM * TAM_CASA // 2, TAM * TAM_CASA // 2 - 20,
                                    text=msg, font=("Arial", 20), fill="green")

            # Cria o botão "Voltar ao Menu" apenas uma vez
            if not self.botao_voltar:
                self.botao_voltar = tk.Button(self.frame, text="Voltar ao Menu", command=self.voltar_ao_menu)
                self.botao_voltar.pack(pady=10)

    def voltar_ao_menu(self):
        # Destrói o frame container com tudo dentro (canvas, botão)
        self.frame.destroy()
        if self.voltar_menu_callback:
            self.voltar_menu_callback()

def iniciar_com_personalizacao(root, cor_peca, cor_dama, voltar_menu_callback=None):
    app = DamasApp(root, cor_peca, cor_dama, voltar_menu_callback)
    # Retorna o app e o frame para controle externo
    return app, app.frame


if __name__ == "__main__":
    root = tk.Tk()
    # Callback dummy para teste
    def dummy_menu():
        print("Voltar ao menu chamado, mas ainda sem implementação.")
    app = DamasApp(root, voltar_menu_callback=dummy_menu)
    root.mainloop()
