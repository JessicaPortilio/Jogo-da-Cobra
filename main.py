# Jogo da Cobra

#importar bibliotecas necessárias
import pygame
from pygame.locals import *

import random


# Inicializa o Pygame
pygame.init()


# Definir as cores utilizadas no jogo

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Definir a dimessões da janela

LARGURA = 640
ALTURA = 480

# Definir o tamanho de cada bloco da cobra e da comida

BLOCO_TAMANHO = 10

# Definir a velocidade da cobra

COBRA_VELOCIDADE = 10

# Definir a fonte utilizada no placar
FONTE = pygame.font.SysFont('Arial', 60, 'NEGRITO')

game_over_text = FONTE.render("GAME OVER", True, BRANCO)

# Definir a classe da cobra

class COBRA:

    def __init__(self, surface):
        # Representa a superfície onde o jogo será exibido
        self.surface = surface
        # Representando a posição inicial do objeto na tela
        self.x = LARGURA // 2 
        self.y = ALTURA // 2
        # Representando a quantidade de movimento nas direções x e y
        self.dx = BLOCO_TAMANHO
        self.dy = 0
        # Representa o corpo do objeto
        self.corpo = [(self.x, self.y)]
        # representa o comprimento do objeto
        self.length = 1 #comprimento

    # função  mover a cobra    
    def mover(self):
        self.x += self.dx
        self.y += self.dy
        self.corpo.insert(0, (self.x, self.y))
        # verificar colisão com a parede
        if len(self.corpo) > self.length:
            self.corpo.pop()
        # verificar colisão com a própria cobra
        if self.verificar_colisao(self.x, self.y):
            self.surface.blit(game_over_text, (LARGURA // 2 - game_over_text.get_width() // 2, ALTURA // 2 - game_over_text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            quit()
    
    # função draw é responsável por desenhar a cobra na superficie do jogo
    def draw(self):
        for x, y in self.corpo:
            pygame.draw.rect(self.surface, VERDE, (x, y, BLOCO_TAMANHO, BLOCO_TAMANHO))
    
    # função para verificar colisão
    def verificar_colisao(self, x, y):
        if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
            return True
        for corpo_part in self.corpo[1:]:
            if x == corpo_part[0] and y == corpo_part[1]:
                return True
        return False
    
    # função para verificar colisão com alimento
    def verificar_colisao_de_alimentos(self, x, y):
        if x == self.x and y == self.y:
            self.length +=1 # aumeenta o comprimento da cobra em 1
            return True
        return False


# Define a classe da comida
class COMIDA:
    #  A classe Comida é usada para criar e desenhar a comida em uma posição aleatória.
    def __init__(self):
        self.x = random.randint(0, LARGURA // BLOCO_TAMANHO - 1) * BLOCO_TAMANHO
        self.y = random.randint(0, ALTURA // BLOCO_TAMANHO - 1) * BLOCO_TAMANHO
    # desenha um retângulo vermelho nessa superfície na posição do alimento.
    def draw(self, surface):
        pygame.draw.rect(surface, VERMELHO, (self.x, self.y, BLOCO_TAMANHO, BLOCO_TAMANHO))


# Define a função principal do jogo

def main():
    count = 0
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption('JOGO DA COBRA')

    # Cria a cobra
    cobra = COBRA(tela)
    # Cria a comida
    comida = COMIDA()

    # Define o relógio
    relogio = pygame.time.Clock()
    # responde à entrada do usuário, atualiza a posição da cobra e desenha os objetos na tela.
    while True:
        # Verificar eventos
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif eventos.type == pygame.KEYDOWN:
                if eventos.key == pygame.K_LEFT:
                    cobra.dx = -BLOCO_TAMANHO
                    cobra.dy = 0
                elif eventos.key == pygame.K_RIGHT:
                    cobra.dx = BLOCO_TAMANHO
                    cobra.dy = 0
                elif eventos.key == pygame.K_UP:
                    cobra.dx = 0
                    cobra.dy = -BLOCO_TAMANHO
                elif eventos.key == pygame.K_DOWN:
                    cobra.dx = 0
                    cobra.dy = BLOCO_TAMANHO

        # Mover a cobra
        cobra.mover()

        # Desenhar a cobra na tela
        tela.fill(PRETO)

        cobra.draw()

        if cobra.verificar_colisao_de_alimentos(comida.x, comida.y):
            comida = COMIDA()
            count += 0.1
        comida.draw(tela)

        if cobra.verificar_colisao(cobra.x, cobra.y):
            tela.blit(game_over_text, (LARGURA // 2 - game_over_text.get_width() // 2, ALTURA // 2 -game_over_text.get_height() // 2))
        pygame.display.update()

        
        # Define o relógio
        relogio.tick(COBRA_VELOCIDADE + count)
        


main()