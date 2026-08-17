"""
============================================================================
 RAPIDOS E IRRITADOS  —  demo de jogo 2D
 Disciplina: Linguagem de Programação Aplicada — UNINTER (2026) Natan Alves da Siva Ru:5194435
============================================================================

Requisitos da atividade
  - Jogo 2D com janela gráfica
  - Controle do jogador pelo teclado (setas: virar, acelerar, frear)
  - Desafio: trânsito que se aproxima e fica mais intenso com a velocidade
  - Condição de VITÓRIA: percorrer uma certa distância
  - Condição de DERROTA: perder todas as vidas batendo o carro
  - MENU inicial exibindo os comandos de controle na própria tela
  - Carregamento de assets por CAMINHO RELATIVO (função resource_path),
"""

import os
import sys
import math
import random
import pygame

# CAMINHO RELATIVO DE RECURSOS


def resource_path(caminho_relativo):
    bases = []
    base_pyinstaller = getattr(sys, "_MEIPASS", None)
    if base_pyinstaller:
        bases.append(base_pyinstaller)
    if getattr(sys, "frozen", False):
        bases.append(os.path.dirname(sys.executable))
    bases.append(os.path.dirname(os.path.abspath(__file__)))

    for base in bases:
        candidato = os.path.join(base, caminho_relativo)
        if os.path.exists(candidato):
            return candidato
    return os.path.join(bases[0], caminho_relativo)


LARGURA, ALTURA = 800, 600
FPS = 60
TITULO = "Rapidos e Irritados"

# pista centralizada na tela
ESTRADA_X = 180
ESTRADA_LARGURA = 440

NUM_FAIXAS = 3

FAIXAS = [
    ESTRADA_X + ESTRADA_LARGURA / 6,
    ESTRADA_X + ESTRADA_LARGURA / 2,
    ESTRADA_X + ESTRADA_LARGURA * 5 / 6
]

META = 20500            # distância (em "metros") para vencer
VIDAS_INICIAIS = 3
VEL_MIN, VEL_MAX = 3.0, 15.5
ACELERACAO = 0.14
FREIO = 0.35
VEL_LATERAL = 6.0

LARG_CARRO, ALT_CARRO = 44, 76

# Estados possíveis do jogo (máquina de estados)
MENU, JOGANDO, PAUSA, VITORIA, DERROTA = "menu", "jogando", "pausa", "vitoria", "derrota"

# Paleta de cores
COR_GRAMA = (32, 96, 52)
COR_PISTA = (58, 60, 66)
COR_BORDA = (220, 200, 70)
COR_FAIXA = (240, 240, 240)
COR_JOGADOR = (60, 150, 240)
COR_TEXTO = (235, 238, 248)
COR_SUAVE = (150, 160, 185)
COR_OK = (80, 220, 140)
COR_ALERTA = (255, 210, 80)
COR_PERIGO = (235, 80, 80)
CORES_INIMIGOS = [(230, 70, 70), (240, 180, 60), (180, 90, 220),
                  (80, 200, 120), (230, 120, 160)]

FRASES_DERROTA = [

    "Seu seguro não vai cobrir isso...",

    "Dirigir irritado nunca foi uma boa ideia.",

    "O guincho já está a caminho.",

    "Talvez pegar um ônibus fosse melhor.",

    "Seu GPS sugeriu terapia.",

    "O mecânico agradece pela visita.",

    "A pressa realmente e inimiga da perfeição."

]


def carregar_fonte(tamanho, negrito=False):
    return pygame.font.SysFont("Consolas,Trebuchet MS,Arial", tamanho, bold=negrito)


def clarear(cor, fator=1.3):
    return tuple(min(255, int(c * fator)) for c in cor)


def desenhar_carro(sup, cx, cy, cor, frente_para_cima=True):
    x = int(cx - LARG_CARRO / 2)
    y = int(cy - ALT_CARRO / 2)
    for ry in (y + 8, y + ALT_CARRO - 26):
        pygame.draw.rect(sup, (18, 18, 22),
                         (x - 4, ry, 6, 18), border_radius=2)
        pygame.draw.rect(sup, (18, 18, 22),
                         (x + LARG_CARRO - 2, ry, 6, 18), border_radius=2)

    corpo = pygame.Rect(x, y, LARG_CARRO, ALT_CARRO)
    pygame.draw.rect(sup, cor, corpo, border_radius=10)
    pygame.draw.rect(sup, clarear(cor), corpo, 2, border_radius=10)

    if frente_para_cima:
        brisa = pygame.Rect(x + 6, y + 10, LARG_CARRO - 12, 18)
        farois = [(x + 8, y + 4), (x + LARG_CARRO - 8, y + 4)]
    else:
        brisa = pygame.Rect(x + 6, y + ALT_CARRO - 28, LARG_CARRO - 12, 18)
        farois = [(x + 8, y + ALT_CARRO - 4),
                  (x + LARG_CARRO - 8, y + ALT_CARRO - 4)]
    pygame.draw.rect(sup, (165, 210, 240), brisa, border_radius=5)

    pygame.draw.rect(sup, (245, 245, 245),
                     (int(cx) - 3, y + 6, 6, ALT_CARRO - 12))

    for fx, fy in farois:
        pygame.draw.circle(sup, COR_ALERTA, (fx, fy), 3)


# ELEMENTOS DO JOGO

class Particula:
    """Fragmento da colisão"""

    def __init__(self, x, y, cor):
        angulo = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(1.5, 6.0)
        self.x, self.y = x, y
        self.vx = math.cos(angulo) * velocidade
        self.vy = math.sin(angulo) * velocidade
        self.vida = random.randint(18, 36)
        self.vida_max = self.vida
        self.cor = cor
        self.raio = random.randint(2, 4)

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.92
        self.vy *= 0.92
        self.vida -= 1

    def viva(self):
        return self.vida > 0

    def desenhar(self, sup):
        proporcao = max(0.0, self.vida / self.vida_max)
        raio = max(1, int(self.raio * proporcao))
        pygame.draw.circle(sup, self.cor, (int(self.x), int(self.y)), raio)


class Inimigo:
    """Carro do trânsito: desce em direção ao jogador"""

    def __init__(self, cor):
        meia = LARG_CARRO / 2
        esquerda = ESTRADA_X + 10 + meia
        direita = ESTRADA_X + ESTRADA_LARGURA - 10 - meia
        self.x = random.uniform(esquerda, direita)
        self.y = -ALT_CARRO
        self.cor = cor
        self.lentidao = random.uniform(0.5, 4.0)

    def atualizar(self, velocidade_jogador):
        # velocidade na tela = sua velocidade menos a do carro à frente
        # (quanto mais rápido você anda, mais rápido eles se aproximam)
        self.y += max(1.8, velocidade_jogador - self.lentidao)

    def fora_da_tela(self):
        return self.y - ALT_CARRO / 2 > ALTURA + 20

    def rect(self):
        return pygame.Rect(self.x - LARG_CARRO / 2, self.y - ALT_CARRO / 2,
                           LARG_CARRO, ALT_CARRO)

    def desenhar(self, sup):
        desenhar_carro(sup, self.x, self.y, self.cor, frente_para_cima=True)


class Carro:
    def __init__(self):
        self.faixa = 1
        self.x = FAIXAS[self.faixa]
        self.y = ALTURA - 110
        self.velocidade = VEL_MIN
        self.invulneravel = 0      # frames sem tomar dano após uma batida

    def atualizar(self, teclas, forcar_acelerar=False):
        # trocar de pista
        if teclas[pygame.K_LEFT]:
            self.x -= VEL_LATERAL
        if teclas[pygame.K_RIGHT]:
            self.x += VEL_LATERAL
        # acelerar / frear
        if teclas[pygame.K_UP] or forcar_acelerar:
            self.velocidade = min(VEL_MAX, self.velocidade + ACELERACAO)
        if teclas[pygame.K_DOWN]:
            self.velocidade = max(VEL_MIN, self.velocidade - FREIO)
        # mantém o carro dentro da pista
        meia = LARG_CARRO / 2
        esquerda = ESTRADA_X + 10 + meia
        direita = ESTRADA_X + ESTRADA_LARGURA - 10 - meia
        self.x = max(esquerda, min(direita, self.x))
        if self.invulneravel > 0:
            self.invulneravel -= 1

    def rect(self):
        return pygame.Rect(self.x - LARG_CARRO / 2, self.y - ALT_CARRO / 2,
                           LARG_CARRO, ALT_CARRO)

    def desenhar(self, sup):
        # pisca enquanto estiver invulnerável
        if self.invulneravel > 0 and (self.invulneravel // 4) % 2 == 0:
            return
        desenhar_carro(sup, self.x, self.y, COR_JOGADOR, frente_para_cima=True)


class Jogo:
    def __init__(self):
        pygame.init()

        self.audio_ok = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self.audio_ok = False

        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Rápidos e Irritados")
        self.relogio = pygame.time.Clock()

        self.fonte_g = carregar_fonte(60, True)
        self.fonte_m = carregar_fonte(30, True)
        self.fonte_p = carregar_fonte(22)
        self.fonte_pp = carregar_fonte(18)

        self.som_motor = self._carregar_som("assets/motor.wav")
        self.som_colisao = self._carregar_som("assets/colisao.wav")
        self.canal_motor = None

        self.desloca_linhas = 0.0      # rolagem das faixas da pista
        self.estado = MENU
        self.tremor = 0
        self._reiniciar_partida()
        self.frase_derrota = random.choice(FRASES_DERROTA)
        self.frames_teste = int(os.environ.get("TESTE_FRAMES", "0"))
        self.forcar_acelerar = self.frames_teste > 0
        if self.frames_teste > 0:
            self.estado = JOGANDO

    # ----- áudio ----------------------------------------------------
    def _carregar_som(self, caminho_relativo):
        if not self.audio_ok:
            return None
        try:
            return pygame.mixer.Sound(resource_path(caminho_relativo))
        except Exception:
            return None

    def _tocar(self, som, volume=0.5):
        if som is not None:
            som.set_volume(volume)
            som.play()

    def _sincronizar_motor(self):
        """Liga o som do motor apenas durante o jogo e desliga fora dele."""
        if not self.audio_ok or self.som_motor is None:
            return
        deve_tocar = (self.estado == JOGANDO)
        if deve_tocar and self.canal_motor is None:
            self.canal_motor = self.som_motor.play(loops=-1)
            if self.canal_motor:
                self.canal_motor.set_volume(0.4)
        elif not deve_tocar and self.canal_motor is not None:
            self.canal_motor.stop()
            self.canal_motor = None

    # ----- inicia uma partida ------
    def _reiniciar_partida(self):
        self.carro = Carro()
        self.inimigos = []
        self.particulas = []
        self.distancia = 0.0
        self.vidas = VIDAS_INICIAIS
        self.tempo_spawn = 0
        self.velocidade = VEL_MIN

    # ----- lógica -----
    def explodir(self, x, y, cor, quantidade=20):
        for _ in range(quantidade):
            self.particulas.append(Particula(x, y, cor))

    def spawnar(self):
        self.tempo_spawn += 2.5
        # mais trânsito conforme a velocidade e a distância percorrida
        intervalo = max(25, 90 - int(self.velocidade * 4) -
                        int(self.distancia / 2500))
        if self.tempo_spawn >= intervalo:
            self.tempo_spawn = 0
            novo = Inimigo(random.choice(CORES_INIMIGOS))
            # evita nascer colado em outro carro
            for ini in self.inimigos:
                if ini.y < 150 and abs(ini.x - novo.x) < LARG_CARRO + 14:
                    return
            self.inimigos.append(novo)

    def atualizar_jogo(self, teclas):
        self.carro.atualizar(teclas, self.forcar_acelerar)
        self.velocidade = self.carro.velocidade
        self.distancia += self.velocidade

        self.spawnar()
        for ini in self.inimigos:
            ini.atualizar(self.velocidade)
        self.inimigos = [i for i in self.inimigos if not i.fora_da_tela()]

        # colisão: carro do jogador x trânsito
        if self.carro.invulneravel == 0:
            for ini in list(self.inimigos):
                if ini.rect().colliderect(self.carro.rect()):
                    self.inimigos.remove(ini)
                    self.vidas -= 1
                    self.carro.invulneravel = 100
                    self.carro.velocidade = VEL_MIN      # perde velocidade na batida
                    self.tremor = 120
                    self.explodir(self.carro.x, self.carro.y -
                                  ALT_CARRO / 2, COR_JOGADOR, 26)
                    self._tocar(self.som_colisao, 0.6)
                    break

        for p in self.particulas:
            p.atualizar()
        self.particulas = [p for p in self.particulas if p.viva()]

        if self.tremor > 0:
            self.tremor -= 1

        # condições de fim de jogo
        if self.distancia >= META:
            self.estado = VITORIA
        elif self.vidas <= 0:
            self.estado = DERROTA

    # ----- desenho --------------------------------------------------
    def texto(self, sup, txt, fonte, cor, cx, cy, sombra=True):
        if sombra:
            s = fonte.render(txt, True, (0, 0, 0))
            sup.blit(s, s.get_rect(center=(cx + 2, cy + 2)))
        img = fonte.render(txt, True, cor)
        sup.blit(img, img.get_rect(center=(cx, cy)))

    def _desenhar_cenario(self, sup):
        sup.fill(COR_GRAMA)
        pygame.draw.rect(sup, COR_PISTA, (ESTRADA_X,
                         0, ESTRADA_LARGURA, ALTURA))
        # bordas contínuas da pista
        pygame.draw.rect(sup, COR_BORDA, (ESTRADA_X, 0, 6, ALTURA))
        pygame.draw.rect(sup, COR_BORDA, (ESTRADA_X +
                         ESTRADA_LARGURA - 6, 0, 6, ALTURA))
        # divisórias tracejadas (2 → 3 pistas), rolando para dar sensação de velocidade
        for d in (1, 2):
            lx = ESTRADA_X + ESTRADA_LARGURA * d / 3
            y = self.desloca_linhas - 40
            while y < ALTURA:
                pygame.draw.rect(sup, COR_FAIXA, (int(lx) - 3, int(y), 6, 22))
                y += 40

    def desenhar(self):
        cena = pygame.Surface((LARGURA, ALTURA))
        self._desenhar_cenario(cena)

        if self.estado in (JOGANDO, PAUSA):
            self._desenhar_jogo(cena)
        elif self.estado == MENU:
            self._desenhar_menu(cena)
        elif self.estado == VITORIA:
            self._desenhar_fim(cena, venceu=True)
        elif self.estado == DERROTA:
            self._desenhar_fim(cena, venceu=False)

        deslocamento = (0, 0)

        if self.tremor > 0:
            intensidade = max(1, min(8, self.tremor // 15))

            deslocamento = (
                random.randint(-intensidade, intensidade),
                random.randint(-intensidade, intensidade)
            )

            self.tremor -= 1

        self.tela.fill((0, 0, 0))

        self.tela.blit(cena, deslocamento)

        if self.estado == PAUSA:
            self._overlay_pausa(self.tela)

        pygame.display.flip()

    def _desenhar_jogo(self, sup):
        for p in self.particulas:
            p.desenhar(sup)
        for ini in self.inimigos:
            ini.desenhar(sup)
        self.carro.desenhar(sup)
        self._hud(sup)

    def _hud(self, sup):
        # barra de progresso da distância
        largura_barra = 240
        pygame.draw.rect(
            sup, (0, 0, 0), (12, 14, largura_barra + 4, 16), border_radius=6)
        progresso = min(1.0, self.distancia / META)
        pygame.draw.rect(sup, COR_OK, (14, 16, int(
            largura_barra * progresso), 12), border_radius=6)
        self.texto(sup, f"Meta: {int(progresso * 100)}%", self.fonte_pp, COR_TEXTO,
                   14 + largura_barra // 2, 44, sombra=False)
        # velocidade em km/h
        kmh = min(300, int(self.velocidade * 18))
        self.texto(sup, f"{kmh} km/h", self.fonte_p,
                   COR_ALERTA, LARGURA // 2, 22, sombra=True)
        # vidas (mini carros)
        for i in range(self.vidas):
            cx = LARGURA - 26 - i * 28
            pygame.draw.rect(sup, COR_JOGADOR,
                             (cx - 8, 14, 16, 26), border_radius=4)
        self.texto(sup, "Vidas", self.fonte_pp, COR_SUAVE,
                   LARGURA - 60, 50, sombra=False)

    def _desenhar_menu(self, sup):
        cx = LARGURA // 2
        # leve escurecimento para o texto destacar sobre a pista
        veu = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        veu.fill((0, 0, 0, 90))
        sup.blit(veu, (0, 0))

        self.texto(sup, "RAPIDOS E IRRITADOS",
                   self.fonte_g, COR_ALERTA, cx, 100)
        self.texto(sup, "O trânsito nunca esteve tão irritante!",
                   self.fonte_p, COR_TEXTO, cx, 150, sombra=True)

        bx, by, bw, bh = cx - 200, 200, 400, 220
        caixa = pygame.Surface((bw, bh), pygame.SRCALPHA)
        caixa.fill((10, 14, 26, 210))
        sup.blit(caixa, (bx, by))
        pygame.draw.rect(sup, COR_ALERTA, (bx, by, bw, bh),
                         2, border_radius=10)

        self.texto(sup, "COMANDOS", self.fonte_m, COR_ALERTA, cx, by + 28)
        linhas = [
            "Setas  ← →     Trocar de pista",
            "Seta   ↑       Acelerar",
            "Seta   ↓       Frear",
            "ENTER          Comecar",
            "P              Pausar",
            "ESC            Sair / Pausar",
        ]
        y = by + 60
        for linha in linhas:
            img = self.fonte_p.render(linha, True, COR_TEXTO)
            sup.blit(img, (bx + 28, y))
            y += 27

        self.texto(sup, "Sobreviva ao trânsito sem perder a paciência!",
                   self.fonte_pp, COR_SUAVE, cx, 448, sombra=True)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            self.texto(sup, "Pressione ENTER para correr",
                       self.fonte_m, COR_OK, cx, 510)

    def _desenhar_fim(self, sup, venceu):
        cx = LARGURA // 2
        veu = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        veu.fill((0, 0, 0, 140))
        sup.blit(veu, (0, 0))
        if venceu:
            self.texto(sup, "VITÓRIA!", self.fonte_g, COR_OK, cx, 200)
            self.texto(sup, "Você sobreviveu ao trânsito!",
                       self.fonte_p, COR_TEXTO, cx, 262, sombra=True)
        else:
            self.texto(sup, self.frase_derrota, self.fonte_p,
                       COR_TEXTO, cx, 262, sombra=True)
        self.texto(sup, f"Distância: {int(min(self.distancia, META))} m",
                   self.fonte_m, COR_ALERTA, cx, 322)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            self.texto(sup, "ENTER - Correr de novo      ESC - Sair",
                       self.fonte_p, COR_SUAVE, cx, 410, sombra=True)

    def _overlay_pausa(self, sup):
        veu = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        veu.fill((0, 0, 0, 150))
        sup.blit(veu, (0, 0))
        self.texto(sup, "PAUSA", self.fonte_g, COR_TEXTO,
                   LARGURA // 2, ALTURA // 2 - 20)
        self.texto(sup, "P ou ENTER para continuar",
                   self.fonte_p, COR_SUAVE, LARGURA // 2, ALTURA // 2 + 40, sombra=False)

    # ----- eventos --------------------------------------------------
    def tratar_eventos(self):
        """Processa eventos. Retorna False quando o jogo deve fechar."""
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    if self.estado in (MENU, VITORIA, DERROTA):
                        return False
                    if self.estado == JOGANDO:
                        self.estado = PAUSA
                    elif self.estado == PAUSA:
                        self.estado = JOGANDO
                elif ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if self.estado == MENU:
                        self._reiniciar_partida()
                        self.estado = JOGANDO
                    elif self.estado in (VITORIA, DERROTA):
                        self._reiniciar_partida()
                        self.estado = JOGANDO
                    elif self.estado == PAUSA:
                        self.estado = JOGANDO
                elif ev.key == pygame.K_p and self.estado in (JOGANDO, PAUSA):
                    self.estado = PAUSA if self.estado == JOGANDO else JOGANDO
        return True

    # ----- laço principal -------------------------------------------

    def rodar(self):
        rodando = True
        while rodando:
            rodando = self.tratar_eventos()
            teclas = pygame.key.get_pressed()

            # rolagem do cenário (mais rápida durante a corrida)
            vel_cenario = self.velocidade if self.estado == JOGANDO else 4.0
            self.desloca_linhas = (self.desloca_linhas + vel_cenario) % 40

            if self.estado == JOGANDO:
                self.atualizar_jogo(teclas)

            self._sincronizar_motor()
            self.desenhar()
            self.relogio.tick(FPS)

            # encerramento do modo de teste automático (headless)
            if self.frames_teste > 0:
                self.frames_teste -= 1
                if self.frames_teste <= 0:
                    rodando = False

        pygame.quit()


def main():
    jogo = Jogo()
    jogo.rodar()


if __name__ == "__main__":
    main()
