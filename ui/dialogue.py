import pygame

class DialogueBox:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 20)
        self.active = False
        self.queue = []  # Lista de diálogos
        self.current_dialogue = None # Dicionário com a fala atual
        self.portrait = None
        self.text = ""
        self.choices = []
        self.selected = 0

    def start_sequence(self, dialogue_list):
        """Recebe uma lista de dicionários com as falas"""
        self.queue = dialogue_list
        self.active = True
        self.next_dialogue()

    def next_dialogue(self):
        """Avança para a próxima fala da fila"""
        if self.queue:
            # Pega o primeiro item da lista e remove
            self.current_dialogue = self.queue.pop(0)
            
            self.text = self.current_dialogue.get("text", "")
            self.choices = self.current_dialogue.get("choices", [])
            self.selected = 0
            
            # Carrega retrato
            portrait_path = self.current_dialogue.get("portrait")
            if portrait_path:
                try:
                    img = pygame.image.load(portrait_path).convert_alpha()
                    self.portrait = pygame.transform.scale(img, (120, 120))
                except:
                    self.portrait = None
            else:
                self.portrait = None
        else:
            # Se não há mais nada na fila, fecha
            self.active = False

    def handle_event(self, event):
        if not self.active or event.type != pygame.KEYDOWN: return
        
        # Se houver escolhas, a lógica de seleção continua
        if self.choices:
            if event.key == pygame.K_UP:
                self.selected = max(0, self.selected - 1)
            elif event.key == pygame.K_DOWN:
                self.selected = min(len(self.choices)-1, self.selected + 1)
            elif event.key == pygame.K_RETURN:
                _, effect = self.choices[self.selected]
                effect() # Executa a função da escolha
                self.next_dialogue() # Avança após escolher
        
        # Se NÃO houver escolhas, Enter apenas passa para o próximo
        elif event.key == pygame.K_RETURN:
            self.next_dialogue()

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