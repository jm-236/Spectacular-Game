import pygame

class DialogueBox:
    def __init__(self):
        self.text = ""
        self.choices = []
        self.selected = 0
        self.font = pygame.font.SysFont("arial", 20)
        self.active = False
        
        # --- NOVO: Suporte a Retrato ---
        self.portrait = None 
        self.portrait_side = "left" # "left" para quem fala, "right" para quem ouve (opcional)

    def start_dialogue(self, text, choices=[], portrait_path=None):
        self.text = text
        self.choices = choices
        self.selected = 0
        self.active = True
        
        # Carrega o retrato se houver
        if portrait_path:
            try:
                img = pygame.image.load(portrait_path).convert_alpha()
                # Ajuste o tamanho para ficar bonito na caixa (ex: 100x100)
                self.portrait = pygame.transform.scale(img, (120, 120))
            except:
                self.portrait = None
        else:
            self.portrait = None

    def handle_event(self, event):
        if not self.active: return
        
        # (Sua lógica de escolhas continua igual aqui...)
        if not self.choices and event.key == pygame.K_RETURN:
            # Se não tem escolha e aperta enter, fecha o dialogo
            self.active = False
            return

        if self.choices:
            if event.key == pygame.K_UP:
                self.selected = max(0, self.selected - 1)
            elif event.key == pygame.K_DOWN:
                self.selected = min(len(self.choices)-1, self.selected + 1)
            elif event.key == pygame.K_RETURN:
                _, effect = self.choices[self.selected]
                effect()
                self.active = False # Fecha ao escolher

    def draw(self, screen):
        if not self.active: return

        BOX_HEIGHT = 180 # Aumentei um pouco para caber o retrato
        BOX_Y = 540 - BOX_HEIGHT - 10 

        # Fundo da caixa
        pygame.draw.rect(screen, (10, 10, 15), (20, BOX_Y, 920, BOX_HEIGHT), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (20, BOX_Y, 920, BOX_HEIGHT), width=2, border_radius=10)

        text_x = 40

        # --- Desenha o Retrato ---
        if self.portrait:
            # Desenha o rosto no canto esquerdo
            screen.blit(self.portrait, (30, BOX_Y + 15))
            text_x = 160 # Empurra o texto para a direita

        # Texto
        # Dica: Para texto longo não sair da tela, precisaria de uma função de quebra de linha (wrap)
        # Por enquanto, vamos assumir textos curtos ou usar \n
        lines = self.text.split('\n')
        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, (230,230,230))
            screen.blit(text_surf, (text_x, BOX_Y + 20 + (i*25)))

        # Opções
        for i, (txt, _) in enumerate(self.choices):
            color = (255,255,0) if i == self.selected else (150,150,150)
            surf = self.font.render(f"> {txt}", True, color)
            screen.blit(surf, (text_x + 20, BOX_Y + 100 + i * 25))