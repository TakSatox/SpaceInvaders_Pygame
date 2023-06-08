import pygame


class Laser(pygame.sprite.Sprite):
    #Para subir, temos que ir subtraindo porque o limite da parte de cima da tela é 0 e da parte de baixo é 600, ou seja, para subir temos que diminuir o y.
    def __init__(self, pos, velocidade, altura_tela):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.velocidade = velocidade
        self.altura_y_constante = altura_tela


    #Destruindo a sprite para não acumular eternamente os sprites no grupo. É como realizar um pop() do grupo de sprites de lasers.
    def destruir(self):
        if self.rect.y <= -50 or self.rect.y >= self.altura_y_constante + 50:
            self.kill()

    def update(self):
        self.rect.y -= self.velocidade
        self.destruir()
