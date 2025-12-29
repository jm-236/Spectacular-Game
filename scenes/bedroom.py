import pygame
from scenes.base_scene import Scene
from ui.dialogue import DialogueBox
from ui.phone import Phone
from player import Player

class Bedroom(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player()
        self.phone = Phone()
        self.show_phone = False
        self.decisao = False

        self.paused = False

        self.overlay = pygame.Surface((960, 540), pygame.SRCALPHA)
        self.overlay.set_alpha(150) # Transparência (0 = invisível, 255 = sólido)
        self.overlay.fill((0, 0, 0)) # Cor preta
        
        self.font_pause = pygame.font.SysFont("arial", 40, bold=True)

        self.background = pygame.image.load(
            "assets/images/bedroom.png"
        ).convert()
        self.background = pygame.transform.scale(
            self.background, (960, 540)
        )


        self.dialogue = DialogueBox()

        self.interaction_text = None

        # zonas de interação
        self.bed = pygame.Rect(0, 320, 300, 60)
        self.desk = pygame.Rect(400, 330, 250, 60)
        self.door = pygame.Rect(750, 280, 140, 120)

    def handle_event(self, event):
        # Primeiro checa se foi uma tecla apertada
        if event.type == pygame.KEYDOWN:
            # 1. Checa o Pause primeiro (Tecla ESC)
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                return # Impede que o ESC faça outra coisa
            # 2. Se estiver pausado, bloqueia qualquer outro input
            if self.paused:
                return
            
            # 1. O TAB abre/fecha o celular
            if event.key == pygame.K_TAB:
                self.show_phone = not self.show_phone
                return # Para não processar mais nada se acabou de abrir/fechar

            # 2. SE o celular estiver ABERTO, quem manda é ele
            if self.show_phone:
                self.phone.handle_event(event) # <--- O SEGREDO TÁ AQUI
            
            if self.decisao:
                self.dialogue.handle_event(event)

            else:
                if event.key == pygame.K_e:
                    self.check_interaction()

    def check_interaction(self):
        if self.player.rect.colliderect(self.bed):
            self.dialogue.start_sequence(
                [
                    {
                        "text":"Peter:\nCara... mal dormi essa noite.",
                        "portrait":"assets/avatars/peter.jpg" 
                    },
                    {
                        "text":"Peter:\nMas não vou negar, foi uma noite bem divertida haha!",
                        "portrait":"assets/avatars/peter.jpg"
                    }
                ]
            )
            self.decisao = True
            
        elif self.player.rect.colliderect(self.desk):
            
            self.dialogue.start_sequence(
                [
                    {
                        "text":"Peter:\nBom... vamos voltar à velha rotina de provas e livros.",
                        "portrait":"assets/avatars/peter.jpg" 
                    },
                    {
                        "text":"Peter:\nAo menos vou poder testar minha \nnova fórmula de fluido de teia na aula de química!",
                        "portrait":"assets/avatars/peter.jpg"
                    }
                ]
            )
            self.decisao = True

        elif self.player.rect.colliderect(self.door):
            # Exemplo dentro do Bedroom.py ao tocar na porta
            self.dialogue.start_sequence(
                [
                    {
                        "text":"Peter:\nAtrasar logo no primeiro dia de aula não é uma ideia muito boa...\nMelhor eu ir logo! ",
                        "choices":[
                            ("Sim, partiu escola!", lambda: None),
                            ("Não, esqueci algo.", self.ficar_no_quarto)
                        ],
                        "portrait":"assets/avatars/peter.jpg" 
                    }
                ]
            )
            self.decisao = True
            # futuramente: trocar cena

    def update(self, dt):
        if self.paused:
            return
        keys = pygame.key.get_pressed()
        if not self.show_phone and not self.decisao:
            self.player.update(dt, keys)

        if not self.dialogue.active and self.decisao:
            self.decisao = False

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        # quarto escuro
        self.player.draw(screen, is_using_phone=self.show_phone)

        if self.show_phone:
            self.phone.draw(screen)
        else:
            self.dialogue.draw(screen)
            pass
        if self.paused:
            # Desenha o fundo escuro
            screen.blit(self.overlay, (0, 0))
            
            # Desenha o Texto "PAUSADO" centralizado
            text_surf = self.font_pause.render("PAUSADO", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(960/2, 540/2))
            screen.blit(text_surf, text_rect)
            
            # (Opcional) Instrução pequena embaixo
            tip_surf = pygame.font.SysFont("arial", 20).render("Pressione ESC para voltar", True, (200, 200, 200))
            tip_rect = tip_surf.get_rect(center=(960/2, 540/2 + 40))
            screen.blit(tip_surf, tip_rect)
    
    def ficar_no_quarto(self):
        self.decisao = False
