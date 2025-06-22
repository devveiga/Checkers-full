import tkinter as tk
from menu import MenuDamas
import ui_tkinter

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.frame_atual = None
        self.mostrar_menu()

    def iniciar_jogo(self, cor_peca, cor_dama):
        if self.frame_atual:
            self.frame_atual.destroy()
        app, frame = ui_tkinter.iniciar_com_personalizacao(
            self.root, cor_peca, cor_dama, voltar_menu_callback=self.mostrar_menu)
        self.frame_atual = frame

    def mostrar_menu(self):
        if self.frame_atual:
            self.frame_atual.destroy()
        self.menu = MenuDamas(self.root, iniciar_jogo_callback=self.iniciar_jogo)
        self.frame_atual = self.menu.frame

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
