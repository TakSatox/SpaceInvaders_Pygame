import pygame, sys
from jogador import Jogador
import defesa
from alien import Alien, AlienExtra
from random import choice, randint
from laser import Laser


class Game:
    def __init__(self):
        #Variáveis para auxiliar nas funções.
        self.fim = False
        self.derrota = False

        #Centraliza imagem do jogador.
        jogador_sprite = Jogador((largura_tela / 2, altura_tela), largura_tela, altura_tela, 4)
        self.jogador = pygame.sprite.GroupSingle(jogador_sprite)
        self.jogador_superficie = pygame.image.load('./graphics/player.png').convert_alpha()

        #Adicionando sistema de vida, pontuação e fases.
        self.vidas = 3
        self.pontos = 0
        self.fase = 1

        #Carregando a fonte pixelada.
        self.fonte = pygame.font.Font('./font/Pixeled.ttf')

        #Passando o formato da defesa para a classe game.
        self.formato = defesa.formato
        self.tamanho_bloco = 6
        self.blocos = pygame.sprite.Group()

        #Criando 4 barreiras de defesa bem distribuidas pela largura da tela.
        self.quantidade_defesa = 4
        #Definindo a posição de cada barreira.
        self.defesa_x_pos = [num * (largura_tela / self.quantidade_defesa) for num in range(self.quantidade_defesa)]
        #Desempacotando as posições das barreiras e inserindo a posição inicial de onde todas serão desenhadas.
        self.criar_defesas(*self.defesa_x_pos, x_inicio=largura_tela / 15, y_inicio=480)

        #Criando os aliens
        self.aliens = pygame.sprite.Group()
        self.configuração_alien(linhas=6, colunas=10)
        self.alien_sentido = 1
        self.alien_lasers = pygame.sprite.Group()
        self.alien_laser_time = 800
        
        #Criando o alien de ponto extra e escolhendo um tempo aleatório para ele aparecer.
        self.alien_extra = pygame.sprite.GroupSingle()
        self.alien_extra_tempo = randint(400, 800)

        #Configurações de áudio.
        self.music = pygame.mixer.Sound('./audio/music.wav')
        self.music.set_volume(0.1)
        self.music.play(loops=-1)
        self.laser_som = pygame.mixer.Sound('./audio/laser.wav')
        self.laser_som.set_volume(0.5)
        self.explosao_som = pygame.mixer.Sound('./audio/explosion.wav')
        self.explosao_som.set_volume(0.3)
        self.vitoria_som = pygame.mixer.Sound('./audio/proximafase.wav')
        self.vitoria_som.set_volume(0.5)
        self.acertado_som = pygame.mixer.Sound('./audio/acertado.wav')
        self.acertado_som.set_volume(0.5)
        self.derrota_som = pygame.mixer.Sound('./audio/derrota.wav')
        self.derrota_som.set_volume(0.5)
        self.alien_extra_acertado_som = pygame.mixer.Sound('./audio/alienextraacertado.wav')
        self.alien_extra_acertado_som.set_volume(0.5)
    
    #Função para criar tudo novamente incrementando 1 na fase e aumentando a velocidade de tiro dos aliens.
    def proxima_fase(self):
        self.vidas = 3
        self.criar_defesas(*self.defesa_x_pos, x_inicio=largura_tela / 15, y_inicio=480)
        self.configuração_alien(linhas=6, colunas=10)
        self.fase += 1
        self.music.play(loops=-1)
        if self.alien_laser_time > 450:
            self.alien_laser_time -= 50
            pygame.time.set_timer(ALIENLASER, game.alien_laser_time)
    
    #Função para criar uma barreira
    def criar_defesa(self, x_inicio, y_inicio, mover_x):
        for linha_indice, linha_elemento in enumerate(self.formato):
            for coluna_indice, caractere in enumerate(linha_elemento):
                if caractere == 'x':
                    x = x_inicio + coluna_indice * self.tamanho_bloco + mover_x
                    y = y_inicio + linha_indice * self.tamanho_bloco

                    bloco = defesa.Bloco(self.tamanho_bloco, (241, 79, 80), x, y)
                    self.blocos.add(bloco)

    #Função para criar várias barreiras dependendo do que é passado no *mover.
    def criar_defesas(self, *mover, x_inicio, y_inicio):
        for mover_x in mover:
            self.criar_defesa(x_inicio, y_inicio, mover_x)

    #Função para desenhar todos os aliens, sendo que na linha 0 tem aliens amarelos, entre a linha 1 e 2 aliens verdes e as demais linhas aliens vermelhos.
    def configuração_alien(self, linhas, colunas, x_distancia=60, y_distancia=48, x_mover=70, y_mover=100):
        for linha_indice, linha_elemento in enumerate(range(linhas)):
            for coluna_indice, caractere in enumerate(range(colunas)):
                x = coluna_indice * x_distancia + x_mover
                y = linha_indice * y_distancia + y_mover
                
                if linha_indice == 0: 
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= linha_indice <= 2: 
                    alien_sprite = Alien('green', x, y)
                else: 
                    alien_sprite = Alien('red', x, y)

                self.aliens.add(alien_sprite)

    #Função para destruir todos os aliens.
    def destruir_todos_aliens(self):
        for alien in self.aliens:
            alien.kill()
    
    #Função para trocar o sentido da movimentação dos aliens ao detectar os aliens tocando em uma borda.
    def alien_mudar_sentido(self):
        todos_aliens = self.aliens.sprites()
        for alien in todos_aliens:
            if alien.rect.right >= largura_tela:
                self.alien_sentido = -1
                self.alien_mover_baixo(2)
            elif alien.rect.left <= 0:
                self.alien_sentido = 1 
                self.alien_mover_baixo(2)

    #Função que move os aliens para baixo ao tocarem qualquer borda.
    def alien_mover_baixo(self, y_mover):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += y_mover

    #Função que faz um alien aleatório atirar.
    def alien_atirar(self):
        if self.aliens.sprites():
            alien_aleatorio = choice(self.aliens.sprites())
            laser_sprite = Laser(alien_aleatorio.rect.center, -6, altura_tela)
            self.alien_lasers.add(laser_sprite)
            self.laser_som.play()

    #Função que faz o alien do ponto extra aparecer.
    def alien_extra_aparecer(self):
        self.alien_extra_tempo -= 1
        if self.alien_extra_tempo <= 0 and not self.fim:
            self.alien_extra.add(AlienExtra(choice(['direita', 'esquerda']), largura_tela))
            self.alien_extra_tempo = randint(400, 800)

    #Função que determina o que ocorre quando tanto o laser do jogador quanto dos aliens acertam algo.
    def colisoes(self):
        #Lasers do jogador.
        if self.jogador.sprite.lasers:
            for laser in self.jogador.sprite.lasers:
                #Colisão com os obstáculos.
                if pygame.sprite.spritecollide(laser, self.blocos, True):
                    laser.kill()

                #Colisão com os aliens.
                aliens_acerto = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_acerto:
                    for alien in aliens_acerto:
                        self.pontos += alien.valor
                    laser.kill()
                    self.explosao_som.play()
                

                #Colisão com o alien extra.
                if pygame.sprite.spritecollide(laser, self.alien_extra, True):
                    self.pontos += 500
                    laser.kill()
                    self.explosao_som.play()
                    self.alien_extra_acertado_som.play()
                    
        
        #Lasers dos aliens.
        if self.alien_lasers:
                for laser in self.alien_lasers:
                    #Colisão com os obstáculos.
                    if pygame.sprite.spritecollide(laser, self.blocos, True):
                        laser.kill()

                    #Colisão com o jogador.
                    if pygame.sprite.spritecollide(laser, self.jogador, False):
                        laser.kill()
                        if self.vidas > 0:
                            self.vidas -= 1
                        self.acertado_som.play()
                        if self.vidas <= 0:
                            self.destruir_todos_aliens()
        
        #Os blocos quebram quando os aliens tocam neles.
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocos, True)
                if pygame.sprite.spritecollide(alien, self.jogador, False):
                    self.destruir_todos_aliens()

    #Função para exibir a quantidade de vidas na tela.
    def exibir_vidas(self):
        vidas_exib = self.fonte.render(f'VIDAS RESTANTES: {self.vidas}', False, 'white')
        vidas_rect = vidas_exib.get_rect(topright = (790, -10))
        tela.blit(vidas_exib, vidas_rect)
 
    #Função para exibir a quantidade de pontos na tela.
    def exibir_pontos(self):
        pontos_exib = self.fonte.render(f'Pontos: {self.pontos}', False, 'white')
        pontos_rect = pontos_exib.get_rect(topleft=(10, 10))
        tela.blit(pontos_exib, pontos_rect)

    #Função para exibir a fase atual na tela.
    def exibir_fase(self):
        fase_exib = self.fonte.render(f'Fase: {self.fase}', False, 'white')
        fase_rect = fase_exib.get_rect(topleft=(10, -10))
        tela.blit(fase_exib, fase_rect)

    #Função que puxa a função da próxima fase quando o jogador ganha ou que exibe derrota ao perder.
    def final(self):
        if not self.aliens.sprites():
            if self.vidas > 0:
                vitoria_exib = self.fonte.render("Parabens!! Inciando proxima fase...", False, 'white')
                vitoria_rect = vitoria_exib.get_rect(center = (largura_tela / 2, altura_tela / 2))
                tela.blit(vitoria_exib, vitoria_rect)
                pygame.display.flip()
                self.music.stop()
                self.vitoria_som.play()
                pygame.time.wait(3000)
                self.proxima_fase()

            #Mensagem de derrota
            if self.vidas < 1:
                derrota_exib = self.fonte.render("Derrota... Que tristeza", False, 'white')
                derrota_rect = derrota_exib.get_rect(center = (largura_tela / 2, altura_tela / 2))
                tela.blit(derrota_exib, derrota_rect)

                if not self.derrota: 
                    self.derrota_som.play()
                    self.music.stop()
                    self.derrota = True
                    for extra in self.alien_extra:
                        extra.kill()

                self.fim = True

    #Função que realiza todos os desenhos e updates dos objetos.
    def run(self):
        self.jogador.update()
        self.aliens.update(self.alien_sentido)
        self.alien_extra.update()
        
        self.alien_mudar_sentido()
        self.alien_lasers.update()
        self.alien_extra_aparecer()
        self.colisoes()
       

        self.jogador.sprite.lasers.draw(tela)
        self.jogador.draw(tela)
        self.blocos.draw(tela)
        self.aliens.draw(tela)
        self.alien_lasers.draw(tela)
        self.alien_extra.draw(tela)
        self.exibir_vidas()
        self.exibir_pontos()
        self.exibir_fase()

        self.final()



#Estamos importando e trabalhando com bastantes arquivos e módulos, então este if certifica que para executar todo o código abaixo, esse arquivo tem que ser executado diretamente.
if __name__ == '__main__':
    #Inicia o pygame
    pygame.init()

    #Armazenando em variáveis o tamanho da tela em largura e altura.
    largura_tela = 800
    altura_tela = 600

    #De fato definindo o tamanho da tela através do display.set_mode() e passando uma tupla como argumento que contém justamente a largura e altura.
    tela = pygame.display.set_mode((largura_tela, altura_tela))

    #Criando o objeto clock para definir o tick rate que é a taxa de atualização do game.
    clock = pygame.time.Clock()

    #Instanciando o jogo.
    game = Game()

    #Criando um evento personalizado que para o alien atirar.
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, game.alien_laser_time)


    #Loop pro game rodar eternamente até o que seja fechado.
    while True:
        for evento in pygame.event.get():
            if evento.type == ALIENLASER:
                game.alien_atirar()
            elif evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        #Caso o jogador pressionar o shift direito, o jogo vai para a próxima fase.
        if pygame.key.get_pressed()[pygame.K_RSHIFT]:
            game.destruir_todos_aliens()

        #Preenche a tela com a cor RGB 30, 30, 30.
        tela.fill((30, 30, 30))

        #Chama a função run para eternamente nesse loop estar atualizando os objetos.
        game.run()

        #Atualiza o que está sendo exibido na tela.
        pygame.display.flip()

        #Definindo o tick rate como 60.
        clock.tick(60)

        #Reinicia o game caso o jogador pressionar F1.
        if pygame.key.get_pressed()[pygame.K_F1]:
            game.music.stop()
            game = Game()
