# game.py
import pygame
import math

class Carro:  # TEM QUE SER Carro, NÃO CARROS (sua classe tava com nome errado)
    def __init__(self, x, y, imagem, stats):
        self.x = x
        self.y = y
        self.imagem = imagem
        self.angulo = 0
        self.velocidade = 0
        
        # Stats do carro
        self.max_speed = stats["max_speed"]
        self.acceleracao = stats["acceleration"]
        self.freio = stats["brake"]
        self.direcoes = stats["direcoes"]  # ANTES TAVA ERRADO: stats[self.direcoes] (não faz sentido)
        
        # Física
        self.atrito = 0.98
        self.vel_curva_normal = 3
        self.vel_curva_lenta = 1.5
        self.limite_alta_vel = 0.6
        
    def processar_input(self, teclas):
        # Aceleração e ré
        if teclas[pygame.K_w]:
            self.velocidade += self.acceleracao
        if teclas[pygame.K_s]:
            self.velocidade -= self.freio
            
        # Limites de velocidade
        if self.velocidade > self.max_speed:
            self.velocidade = self.max_speed
        if self.velocidade < -self.max_speed/2:
            self.velocidade = -self.max_speed/2
            
        # Atrito (carro perde velocidade naturalmente)
        self.velocidade *= self.atrito
        
        # Direção (virar fica mais difícil em alta velocidade)
        velocidade_relativa = abs(self.velocidade) / self.max_speed
        if velocidade_relativa > self.limite_alta_vel:
            forca_curva = self.vel_curva_lenta
        else:
            forca_curva = self.vel_curva_normal
            
        if teclas[pygame.K_a]:
            self.angulo += forca_curva
        if teclas[pygame.K_d]:
            self.angulo -= forca_curva
            
    def atualizar_posicao(self):
        # Move o carro baseado no ângulo e velocidade
        self.x += math.cos(math.radians(self.angulo)) * self.velocidade
        self.y -= math.sin(math.radians(self.angulo)) * self.velocidade
        
    def desenhar(self, tela):
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        rect = imagem_rotacionada.get_rect(center=(self.x, self.y))
        tela.blit(imagem_rotacionada, rect)

def main():
    pygame.init()
    
    # Configurações da tela
    LARGURA = 800
    ALTURA = 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("My Car Mechanics")
    
    # Carrega imagem
    from stats import CARROS  # isso aqui é o DICIONÁRIO do stats.py
    imagem_carro = pygame.image.load("assets/images/chevette.png")
    imagem_carro = pygame.transform.scale(imagem_carro, (128, 128))
    
    # Cria o carro (começa no centro da tela)
    stats_chevette = CARROS["chevette"]  # pega os stats do chevette
    player = Carro(LARGURA//2, ALTURA//2, imagem_carro, stats_chevette)  # AGORA É Carro, não CARROS
    
    clock = pygame.time.Clock()
    rodando = True
    
    while rodando:
        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
        
        # Input e física
        teclas = pygame.key.get_pressed()
        player.processar_input(teclas)
        player.atualizar_posicao()
        
        # Desenha tudo
        tela.fill((30, 30, 30))  # Cinza escuro
        player.desenhar(tela)
        
        # Atualiza tela
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()