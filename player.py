import pygame

class Player:
    def __init__(self):
        # --- CARREGANDO OS SPRITES ---
        # Substitua pelos nomes exatos dos seus arquivos
        self.sprites = [
            pygame.image.load("assets/images/peter/peter.png").convert_alpha(),
            pygame.image.load("assets/images/peter/peter_walk_1.png").convert_alpha(),
            pygame.image.load("assets/images/peter/peter_walk_2.png").convert_alpha(),
            pygame.image.load("assets/images/peter/peter_walk_3.png").convert_alpha()
        ]
        
        self.image_phone = pygame.image.load("assets/images/peter/peter_celular.png").convert_alpha()

        # Controle de Animação
        self.current_frame = 0   # Qual imagem estamos mostrando (0, 1 ou 2)
        self.animation_speed = 4 # Quão rápido a perna mexe (ajuste se ficar lento/rápido)

        # Configuração Inicial (usando a primeira imagem como base para o tamanho)
        self.image = self.sprites[0] 
        self.rect = self.image.get_rect()

        # Posicionamento
        self.floor_y = 460
        self.rect.bottom = self.floor_y
        self.rect.x = 200 # Posição inicial X

        # Variáveis de Estado
        self.facing_right = True
        self.speed = 200

    def update(self, dt, keys):
        LIMITE_ESQUERDO = 0
        LIMITE_DIREITO = 820

        is_moving = False # Variável para saber se devemos animar

        if keys[pygame.K_a] and self.rect.x > LIMITE_ESQUERDO:
            self.facing_right = False
            self.rect.x -= self.speed * dt
            is_moving = True
            
        if keys[pygame.K_d] and self.rect.x < LIMITE_DIREITO:
            self.facing_right = True
            self.rect.x += self.speed * dt
            is_moving = True

        # --- LÓGICA DA ANIMAÇÃO ---
        if is_moving:
            # Aumenta o índice do frame baseado no tempo (dt)
            self.current_frame += self.animation_speed * dt
            
            # Se passar do total de frames (ex: 3.1), volta para o zero
            if self.current_frame >= len(self.sprites):
                self.current_frame = 1
        else:
            # Se parou de andar, volta para o frame 0 (postura parada)
            # Ou frame 1, dependendo de qual imagem ele fica com os dois pés no chão
            self.current_frame = 0

        # Atualiza a imagem atual baseada no índice inteiro (0, 1 ou 2)
        index = int(self.current_frame)
        self.image = self.sprites[index]

    def draw(self, screen, is_using_phone):

        if is_using_phone:
            sprite_to_draw = self.image_phone
        else:
            sprite_to_draw = self.image

        # A imagem já foi escolhida no update, aqui só cuidamos do espelhamento
        if self.facing_right:
            screen.blit(sprite_to_draw, self.rect)
        else:
            flipped_image = pygame.transform.flip(sprite_to_draw, True, False)
            screen.blit(flipped_image, self.rect)