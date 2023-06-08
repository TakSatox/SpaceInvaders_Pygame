import pygame
from laser import Laser


class Jogador (pygame.sprite.Sprite):
    #Position
    def __init__(self, pos, constante_x, constante_y, velocidade):
        super().__init__()
        self.image = pygame.image.load('./graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.velocidade = velocidade
        #Passando por argumento o tamanho máximo da tela.
        self.max_x_constante = constante_x
        self.max_y_constante = constante_y

        self.pronto = True
        self.laser_tempo = 0
        self.laser_recarga_tempo = 600

        self.lasers = pygame.sprite.Group()

        self.laser_som = pygame.mixer.Sound('./audio/laser.wav')
        self.laser_som.set_volume(0.5)

    def teclas(self):
        teclas = pygame.key.get_pressed()

        #O retangulo onde está contido o sprite irá se mover através do eixo x para a direita ou esquerda de acordo com a velocidade passada na inicialização desse objeto.
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        elif teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
    
        if teclas[pygame.K_SPACE] and self.pronto:
            self.atira_laser()
            self.pronto = False
            #Esse get ticks é chamado uma vez por tempo.
            self.laser_tempo = pygame.time.get_ticks()
            self.laser_som.play()
        

    def recarregar(self):
        if not self.pronto:
            #Esse get ticks é chamado continuamente.
            momento_atual = pygame.time.get_ticks()
            '''
            Como aqui o get ticks está rodando sem parar, precisamos utilizar um if para verificar se está chegando no cooldown que estabelecemos (no caso é 600).
            Para isso iremos comparar a subtração de current_time com laser_time. O laser_time é get_ticks que puxamos sempre que atiramos. Assim a partir do 
            momento/tempo específico que atiramos, o tempo irá correr até chegar em 600 através da subtração que é o momento em que a variável ready irá se tornar
            True e permitir atirar novamente. 
            '''
            if (momento_atual - self.laser_tempo) >= self.laser_recarga_tempo:
                self.pronto = True

    '''
    Função que irá fazer o player ficar travado dentro da screen criada. Sempre que indo para a esquerda o rect do player for menor do que 0, ele irá retornar ao zero. Dessa
    forma o player não irá conseguir sair pela esquerda. O mesmo pode ser feito pela direita, mas no caso vai depender do tamanho máximo da tela que recebemos pelo argumento
    da função init da classe Player.
    '''
    def constante(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constante:
            self.rect.right = self.max_x_constante

    def atira_laser(self):
        self.lasers.add(Laser(self.rect.center, 8, self.max_y_constante))


    def update(self):
        self.teclas()
        self.constante()
        self.recarregar()
        self.lasers.update()
        