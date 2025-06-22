import json
import os
from tkinter import messagebox

ARQUIVO_PLACAR = "melhor_tempo.json"

def salvar_tempo(tempo):
    """
    Salva um novo tempo no arquivo placar.json.
    """
    dados = []
    if os.path.exists(ARQUIVO_PLACAR):
        with open(ARQUIVO_PLACAR, "r") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = []
    dados.append(tempo)
    with open(ARQUIVO_PLACAR, "w") as f:
        json.dump(dados, f, indent=4)

def ler_melhor_tempo():
    if not os.path.exists(ARQUIVO_PLACAR):
        return None
    with open(ARQUIVO_PLACAR, "r") as f:
        try:
            dados = json.load(f)
            return dados.get("melhor_tempo")
        except json.JSONDecodeError:
            return None


def mostrar_melhor_tempo():
    melhor_tempo = ler_melhor_tempo()
    if isinstance(melhor_tempo, (str, int)):
        messagebox.showinfo("Melhor Resultado", f"O melhor tempo registrado é {melhor_tempo} segundos.")
    else:
        messagebox.showinfo("Melhor Resultado", "Nenhum tempo registrado ainda.")