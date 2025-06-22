import random

TAM = 8
JOGADOR = 1
IA = 2
DAMA_JOGADOR = 3
DAMA_IA = 4

class LogicaDama:
    def __init__(self):
        self.tabuleiro = [[0] * TAM for _ in range(TAM)]
        self.turno_jogador = True
        self.iniciar_tabuleiro()

    def iniciar_tabuleiro(self):
        for y in range(3):
            for x in range(TAM):
                if (x + y) % 2 == 1:
                    self.tabuleiro[y][x] = IA
        for y in range(5, 8):
            for x in range(TAM):
                if (x + y) % 2 == 1:
                    self.tabuleiro[y][x] = JOGADOR

    def eh_dama(self, peca):
        return peca == DAMA_JOGADOR or peca == DAMA_IA

    def movimento_valido(self, x1, y1, x2, y2, jogador):
        if not (0 <= x2 < TAM and 0 <= y2 < TAM):
            return False
        if self.tabuleiro[y2][x2] != 0:
            return False

        peca = self.tabuleiro[y1][x1]
        inimigos = [IA, DAMA_IA] if jogador == JOGADOR else [JOGADOR, DAMA_JOGADOR]

        dx = x2 - x1
        dy = y2 - y1
        abs_dx = abs(dx)
        abs_dy = abs(dy)

        # Peça comum
        if not self.eh_dama(peca):
            # Movimento simples: só pra frente
            direcao = -1 if jogador == JOGADOR else 1
            if abs_dx == 1 and dy == direcao:
                return True

            # Captura: salto de 2 casas, pode ser para frente ou para trás
            if abs_dx == 2 and abs_dy == 2:
                meio_x = x1 + dx // 2
                meio_y = y1 + dy // 2
                if self.tabuleiro[meio_y][meio_x] in inimigos:
                    return True

            return False

        # Peça dama
        else:
            # Movimento deve ser em diagonal (mesma quantidade de passos em x e y)
            if abs_dx != abs_dy or abs_dx == 0:
                return False

            # Checa se caminho está livre para movimento simples
            if self.caminho_livre(x1, y1, x2, y2):
                # Movimento simples (sem pular peças)
                if not self.tem_peca_intermediaria(x1, y1, x2, y2):
                    return True

            # Movimento de captura da dama: pulando exatamente uma peça inimiga no caminho
            if self.captura_dama_valida(x1, y1, x2, y2, inimigos):
                return True

            return False

    def caminho_livre(self, x1, y1, x2, y2):
        dx = (x2 - x1) // abs(x2 - x1)
        dy = (y2 - y1) // abs(y2 - y1)
        x, y = x1 + dx, y1 + dy
        while (x, y) != (x2, y2):
            if self.tabuleiro[y][x] != 0:
                return False
            x += dx
            y += dy
        return True

    def tem_peca_intermediaria(self, x1, y1, x2, y2):
        dx = (x2 - x1) // abs(x2 - x1)
        dy = (y2 - y1) // abs(y2 - y1)
        x, y = x1 + dx, y1 + dy
        while (x, y) != (x2, y2):
            if self.tabuleiro[y][x] != 0:
                return True
            x += dx
            y += dy
        return False

    def captura_dama_valida(self, x1, y1, x2, y2, inimigos):
        dx = (x2 - x1) // abs(x2 - x1)
        dy = (y2 - y1) // abs(y2 - y1)
        x, y = x1 + dx, y1 + dy

        pecas_puladas = 0
        while (x, y) != (x2, y2):
            if self.tabuleiro[y][x] != 0:
                if self.tabuleiro[y][x] in inimigos:
                    pecas_puladas += 1
                else:
                    return False
            x += dx
            y += dy

        return pecas_puladas == 1

    def movimentar(self, x1, y1, x2, y2):
        peca = self.tabuleiro[y1][x1]
        inimigos = [IA, DAMA_IA] if peca in [JOGADOR, DAMA_JOGADOR] else [JOGADOR, DAMA_JOGADOR]

        self.tabuleiro[y2][x2] = peca
        self.tabuleiro[y1][x1] = 0

        capturou = False

        # Remover peças capturadas (movimentos normais e damas)
        if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
            meio_x = (x1 + x2) // 2
            meio_y = (y1 + y2) // 2
            if self.tabuleiro[meio_y][meio_x] in inimigos:
                self.tabuleiro[meio_y][meio_x] = 0
                capturou = True

        elif self.eh_dama(peca):
            dx = (x2 - x1) // abs(x2 - x1)
            dy = (y2 - y1) // abs(y2 - y1)
            x, y = x1 + dx, y1 + dy
            while (x, y) != (x2, y2):
                if self.tabuleiro[y][x] in inimigos:
                    self.tabuleiro[y][x] = 0
                    capturou = True
                    break  # só pula uma peça por movimento
                x += dx
                y += dy

        # Promoção para dama ao chegar na base inimiga
        if peca == JOGADOR and y2 == 0:
            self.tabuleiro[y2][x2] = DAMA_JOGADOR
        elif peca == IA and y2 == TAM - 1:
            self.tabuleiro[y2][x2] = DAMA_IA

        # Se capturou e pode continuar capturando, mantém turno, senão troca turno
        if capturou and self.pode_capturar(x2, y2):
            # mantém turno para captura múltipla
            return
        else:
            self.turno_jogador = not self.turno_jogador

    def pode_capturar(self, x, y):
        peca = self.tabuleiro[y][x]
        jogador = JOGADOR if peca in [JOGADOR, DAMA_JOGADOR] else IA
        inimigos = [IA, DAMA_IA] if jogador == JOGADOR else [JOGADOR, DAMA_JOGADOR]

        # Verifica movimentos de captura possíveis a partir da posição (x,y)
        for dy in range(-TAM, TAM):
            for dx in range(-TAM, TAM):
                nx, ny = x + dx, y + dy
                if 0 <= nx < TAM and 0 <= ny < TAM:
                    # Só movimentos de captura (diagonal e salto >= 2)
                    if abs(dx) == abs(dy) and abs(dx) >= 2:
                        if self.movimento_valido(x, y, nx, ny, jogador):
                            return True
        return False

    def tem_movimentos_possiveis(self, jogador):
        pecas_jogador = [JOGADOR, DAMA_JOGADOR] if jogador == JOGADOR else [IA, DAMA_IA]

        for y in range(TAM):
            for x in range(TAM):
                if self.tabuleiro[y][x] in pecas_jogador:
                    # testa todos movimentos possíveis (simples e captura)
                    for dy in range(-TAM, TAM):
                        for dx in range(-TAM, TAM):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < TAM and 0 <= ny < TAM:
                                if self.movimento_valido(x, y, nx, ny, jogador):
                                    return True
        return False

    def movimento_ia(self):
        movimentos_captura = []
        movimentos_simples = []

        for y in range(TAM):
            for x in range(TAM):
                peca = self.tabuleiro[y][x]
                if peca in [IA, DAMA_IA]:
                    if not self.eh_dama(peca):
                        # Peça comum da IA
                        for dx, dy in [(-2, 2), (2, 2)]:
                            nx, ny = x + dx, y + dy
                            if self.movimento_valido(x, y, nx, ny, IA):
                                movimentos_captura.append((x, y, nx, ny))
                        for dx, dy in [(-1, 1), (1, 1)]:
                            nx, ny = x + dx, y + dy
                            if self.movimento_valido(x, y, nx, ny, IA):
                                movimentos_simples.append((x, y, nx, ny))
                    else:
                        # Dama da IA: verificar movimentos em todas as diagonais até o limite
                        for dx_dir in [-1, 1]:
                            for dy_dir in [-1, 1]:
                                dist = 1
                                while True:
                                    nx = x + dx_dir * dist
                                    ny = y + dy_dir * dist
                                    if not (0 <= nx < TAM and 0 <= ny < TAM):
                                        break
                                    if self.movimento_valido(x, y, nx, ny, IA):
                                        if abs(nx - x) > 1:
                                            movimentos_captura.append((x, y, nx, ny))
                                        else:
                                            movimentos_simples.append((x, y, nx, ny))
                                        dist += 1
                                    else:
                                        break

        if movimentos_captura:
            movimento = random.choice(movimentos_captura)
        elif movimentos_simples:
            movimento = random.choice(movimentos_simples)
        else:
            movimento = None

        if movimento:
            self.movimentar(*movimento)

        self.turno_jogador = True

    def status_jogo(self):
        pecas_ia = any(p in [IA, DAMA_IA] for linha in self.tabuleiro for p in linha)
        pecas_jogador = any(p in [JOGADOR, DAMA_JOGADOR] for linha in self.tabuleiro for p in linha)
        ia_pode = pecas_ia and self.tem_movimentos_possiveis(IA)
        jogador_pode = pecas_jogador and self.tem_movimentos_possiveis(JOGADOR)
        if not pecas_ia or not ia_pode:
            return "vitoria"
        if not pecas_jogador or not jogador_pode:
            return "derrota"
        return "em_andamento"
