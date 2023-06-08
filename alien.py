import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, cor, x, y):
        super().__init__()
        diretorio = './graphics/' + cor + '.png'
        self.image = pygame.image.load(diretorio).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
        self.rotacao = True
        
        if cor == 'red': self.valor = 100
        elif cor == 'green': self.valor = 200
        elif cor == 'yellow': self.valor = 300

    def update(self, sentido):
        self.rect.x += sentido




class AlienExtra(pygame.sprite.Sprite):
    def __init__(self, lado_aparecer, largura_tela):
        super().__init__()
        self.image = pygame.image.load('./graphics/extra.png').convert_alpha()

        if lado_aparecer == 'direita':
            x = largura_tela + 50
            self.velocidade = -3
        elif lado_aparecer == 'esquerda':
            x = -50
            self.velocidade = 3

        self.rect =self.image.get_rect(topleft=(x,80))
    
    def update(self):
        self.rect.x += self.velocidade