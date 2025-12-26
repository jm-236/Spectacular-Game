import pygame
from state import state

class Phone:
    def __init__(self):
        # Configurações visuais
        self.width = 280
        self.height = 450
        self.x = 620
        self.y = 50
        
        # Cores (Paleta Dark Mode)
        self.COLOR_BODY = (20, 20, 20)       # A carcaça do celular
        self.COLOR_SCREEN = (45, 45, 55)     # O fundo da tela (quase preto azulado)
        self.COLOR_MSG_BG = (70, 70, 80)     # Fundo da notificação
        self.COLOR_TEXT = (240, 240, 240)
        self.COLOR_ACCENT = (100, 200, 255)  # Azulzinho tech para nomes
        
        # Fontes
        self.font_header = pygame.font.SysFont("arial", 14, bold=True)
        self.font_name = pygame.font.SysFont("arial", 16, bold=True)
        self.font_msg = pygame.font.SysFont("arial", 15)
        
        # Dados
        self.messages = [
            {"sender": "Gwen", "text": "Vc vem cedo hoje?", "color": (255, 105, 180)}, # Rosa
            {"sender": "Harry", "text": "Prova hj 😬", "color": (50, 205, 50)},       # Verde
            {"sender": "MJ", "text": "Bom dia, Parker", "color": (255, 0, 0)},         # Vermelho
        ]

    def handle_event(self, event):
        # Mantendo a lógica de jogo que você já tinha
        if event.key == pygame.K_1:
            state["gwen_trust"] += 1
            print("Gwen Trust +1") # Debug visual no console
        if event.key == pygame.K_2:
            state["harry_trust"] += 1
            print("Harry Trust +1")

    def update(self, dt):
        pass

    def draw(self, screen):
        # 1. Desenha o Corpo do Celular (Borda preta arredondada)
        body_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.COLOR_BODY, body_rect, border_radius=30)
        
        # Borda externa fina (simulando metal/brilho)
        pygame.draw.rect(screen, (60, 60, 60), body_rect, width=2, border_radius=30)

        # 2. Desenha a Tela (Acende a tela)
        screen_margin = 12
        screen_rect = pygame.Rect(
            self.x + screen_margin, 
            self.y + screen_margin, 
            self.width - (screen_margin*2), 
            self.height - (screen_margin*2)
        )
        pygame.draw.rect(screen, self.COLOR_SCREEN, screen_rect, border_radius=20)

        # 3. Barra de Status (Topo)
        self.draw_status_bar(screen, screen_rect)

        # 4. Desenha as Notificações
        start_y = screen_rect.y + 40
        for i, msg in enumerate(self.messages):
            self.draw_notification(screen, screen_rect.x, start_y, msg)
            start_y += 70 # Espaço entre mensagens

        # 5. Botão Home / Barra de gesto (Embaixo)
        pygame.draw.rect(screen, (200, 200, 200), (self.x + self.width//2 - 40, self.y + self.height - 20, 80, 4), border_radius=2)

    def draw_status_bar(self, screen, screen_rect):
        # Hora
        time_surf = self.font_header.render("07:10", True, (200, 200, 200))
        screen.blit(time_surf, (screen_rect.x + 15, screen_rect.y + 10))
        
        # Ícone de Bateria (Simples)
        bat_rect = pygame.Rect(screen_rect.right - 35, screen_rect.y + 12, 20, 10)
        pygame.draw.rect(screen, (200, 200, 200), bat_rect, width=1)
        pygame.draw.rect(screen, (200, 200, 200), (bat_rect.x + 2, bat_rect.y + 2, 12, 6)) # Carga

    def draw_notification(self, screen, x, y, msg):
        # Fundo do Card da Mensagem
        padding = 10
        card_width = self.width - 44 # Ajuste fino para caber na tela
        card_height = 60
        
        card_rect = pygame.Rect(x + 10, y, card_width, card_height)
        
        # Desenha o fundo do card com transparência simulada (cor sólida mais clara que o fundo)
        pygame.draw.rect(screen, self.COLOR_MSG_BG, card_rect, border_radius=12)

        # Avatar (Círculo colorido com a inicial ou cor do personagem)
        pygame.draw.circle(screen, msg["color"], (x + 35, y + 30), 18)
        
        # Nome do remetente
        name_surf = self.font_name.render(msg["sender"], True, self.COLOR_TEXT)
        screen.blit(name_surf, (x + 60, y + 10))
        
        # Texto da mensagem
        txt_surf = self.font_msg.render(msg["text"], True, (180, 180, 180))
        screen.blit(txt_surf, (x + 60, y + 32))