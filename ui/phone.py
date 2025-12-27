import pygame
import os
from state import state

class Phone:
    def __init__(self):
        # --- Configurações Visuais ---
        self.width = 280
        self.height = 450
        self.x = 620
        self.y = 50
        
        # Cores
        self.colors = {
            "body": (20, 20, 20),
            "screen": (30, 30, 35),
            "header": (40, 40, 50),
            "msg_bg": (60, 60, 70),
            "user_msg": (0, 120, 215), # Azul do zap
            "text": (240, 240, 240),
            "highlight": (80, 80, 90) # Seleção
        }
        
        # Fontes
        self.font_header = pygame.font.SysFont("arial", 16, bold=True)
        self.font_msg = pygame.font.SysFont("arial", 14)
        self.font_small = pygame.font.SysFont("arial", 12)

        # --- Estado Interno do Celular ---
        self.current_screen = "LIST" # Pode ser "LIST" ou "CHAT"
        self.selected_index = 0      # Qual item está selecionado (na lista ou nas respostas)
        self.active_chat_id = None   # Qual chat está aberto
        
        # --- Dados das Conversas ---
        # Aqui definimos: Caminho da foto, Cor (caso falte foto), Histórico e Opções
        self.chats = {
            "Gwen": {
                "color": (255, 105, 180),
                "image": self.load_avatar("assets/avatars/gwen.jpg"),
                "history": [
                    {"sender": "Gwen", "text": "Vc vem cedo hoje?"}
                ],
                "options": [
                    {"text": "Tô saindo!", "effect": self.increase_gwen_trust},
                    {"text": "Vou atrasar...", "effect": lambda: print("Gwen chateada")}
                ]
            },
            "Harry": {
                "color": (50, 205, 50),
                "image": self.load_avatar("assets/avatars/harry.jpg"),
                "history": [
                    {"sender": "Harry", "text": "Prova hj 😬"},
                    {"sender": "Harry", "text": "Estudou algo?"}
                ],
                "options": [
                    {"text": "Claro (mentira)", "effect": self.increase_harry_trust},
                    {"text": "Ferrou.", "effect": lambda: None}
                ]
            }
        }
        
        # Lista ordenada de chaves para navegação
        self.contact_list = list(self.chats.keys())

    def load_avatar(self, path):
        """ Tenta carregar imagem, retorna None se falhar """
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (36, 36)) # Tamanho do avatar
        except:
            return None

    # --- Efeitos (Callbacks) ---
    def increase_gwen_trust(self):
        state["gwen_trust"] += 1
        # Adiciona a resposta ao histórico visualmente
        self.chats["Gwen"]["history"].append({"sender": "Eu", "text": "Tô saindo!"})
        self.chats["Gwen"]["options"] = [] # Remove opções após responder

    def increase_harry_trust(self):
        state["harry_trust"] += 1
        self.chats["Harry"]["history"].append({"sender": "Eu", "text": "Claro que estudei."})
        self.chats["Harry"]["options"] = []

    # --- Lógica de Input ---
    def handle_event(self, event):
        if event.key == pygame.K_UP:
            self.selected_index = max(0, self.selected_index - 1)
            
        elif event.key == pygame.K_DOWN:
            limit = len(self.contact_list) - 1 if self.current_screen == "LIST" else len(self.get_active_options()) - 1
            if limit >= 0:
                self.selected_index = min(limit, self.selected_index + 1)
        
        elif event.key == pygame.K_RETURN:
            if self.current_screen == "LIST":
                # Entra no chat
                self.open_chat(self.contact_list[self.selected_index])
            elif self.current_screen == "CHAT":
                # Seleciona resposta
                options = self.get_active_options()
                if options:
                    choice = options[self.selected_index]
                    choice["effect"]() # Executa o efeito
                    # Reseta seleção para evitar crash se as opções sumirem
                    self.selected_index = 0 
        
        elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_LEFT:
            # Voltar para lista
            if self.current_screen == "CHAT":
                self.current_screen = "LIST"
                self.active_chat_id = None
                self.selected_index = 0

    def open_chat(self, contact_name):
        self.active_chat_id = contact_name
        self.current_screen = "CHAT"
        self.selected_index = 0 # Reinicia seleção para as opções de resposta

    def get_active_options(self):
        if not self.active_chat_id: return []
        return self.chats[self.active_chat_id]["options"]

    def update(self, dt):
        pass

    # --- Desenho ---
    def draw(self, screen):
        # 1. Carcaça e Tela Base
        body_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.colors["body"], body_rect, border_radius=30)
        pygame.draw.rect(screen, (60,60,60), body_rect, width=2, border_radius=30) # Brilho
        
        screen_rect = pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)
        pygame.draw.rect(screen, self.colors["screen"], screen_rect, border_radius=20)
        
        # Barra de Status
        self.draw_status_bar(screen, screen_rect)

        # 2. Conteúdo da Tela
        content_area = pygame.Rect(screen_rect.x, screen_rect.y + 30, screen_rect.width, screen_rect.height - 50)
        # Clip para nada vazar da tela
        old_clip = screen.get_clip()
        screen.set_clip(screen_rect) 

        if self.current_screen == "LIST":
            self.draw_list_screen(screen, content_area)
        elif self.current_screen == "CHAT":
            self.draw_chat_screen(screen, content_area)

        screen.set_clip(old_clip)

        # 3. Botão Home
        pygame.draw.rect(screen, (200, 200, 200), (self.x + self.width//2 - 40, self.y + self.height - 15, 80, 3), border_radius=2)

    def draw_status_bar(self, screen, rect):
        time_surf = self.font_small.render("07:15", True, (200, 200, 200))
        screen.blit(time_surf, (rect.x + 15, rect.y + 8))
        # Bateria
        bat_rect = pygame.Rect(rect.right - 25, rect.y + 10, 18, 8)
        pygame.draw.rect(screen, (200,200,200), bat_rect, 1)
        pygame.draw.rect(screen, (200,200,200), (bat_rect.x+2, bat_rect.y+2, 10, 4))

    def draw_list_screen(self, screen, area):
        start_y = area.y + 10
        
        title = self.font_header.render("Mensagens", True, self.colors["text"])
        screen.blit(title, (area.x + 15, start_y))
        start_y += 30

        for i, name in enumerate(self.contact_list):
            chat_data = self.chats[name]
            last_msg = chat_data["history"][-1]["text"] if chat_data["history"] else "..."
            
            # Fundo do item (Highlight se selecionado)
            item_rect = pygame.Rect(area.x + 5, start_y, area.width - 10, 60)
            if i == self.selected_index:
                pygame.draw.rect(screen, self.colors["highlight"], item_rect, border_radius=10)
            
            # Avatar
            avatar_x, avatar_y = item_rect.x + 10, item_rect.y + 12
            if chat_data["image"]:
                screen.blit(chat_data["image"], (avatar_x, avatar_y))
            else:
                pygame.draw.circle(screen, chat_data["color"], (avatar_x + 18, avatar_y + 18), 18)
                # Inicial do nome
                initial = self.font_header.render(name[0], True, (255,255,255))
                screen.blit(initial, (avatar_x + 12, avatar_y + 8))

            # Texto
            name_surf = self.font_header.render(name, True, self.colors["text"])
            msg_surf = self.font_msg.render(last_msg, True, (180, 180, 180))
            
            screen.blit(name_surf, (avatar_x + 50, item_rect.y + 10))
            screen.blit(msg_surf, (avatar_x + 50, item_rect.y + 30))
            
            start_y += 65

    def draw_chat_screen(self, screen, area):
        data = self.chats[self.active_chat_id]
        
        # Header do Chat (Nome + Voltar)
        pygame.draw.rect(screen, self.colors["header"], (area.x, area.y, area.width, 40))
        back_arrow = self.font_header.render("<", True, self.colors["text"])
        name_surf = self.font_header.render(self.active_chat_id, True, self.colors["text"])
        screen.blit(back_arrow, (area.x + 10, area.y + 10))
        screen.blit(name_surf, (area.x + 35, area.y + 10))
        
        # Histórico de Mensagens
        msg_y = area.y + 50
        for msg in data["history"]:
            is_me = msg["sender"] == "Eu"
            bg_color = self.colors["user_msg"] if is_me else self.colors["msg_bg"]
            align_x = area.x + 60 if is_me else area.x + 10
            
            # Balão simples
            surf = self.font_msg.render(msg["text"], True, self.colors["text"])
            padding = 10
            bubble_rect = pygame.Rect(align_x, msg_y, surf.get_width() + padding*2, surf.get_height() + padding*2)
            
            # Ajuste para alinhar à direita se for Eu
            if is_me:
                bubble_rect.right = area.right - 10
            
            pygame.draw.rect(screen, bg_color, bubble_rect, border_radius=10)
            screen.blit(surf, (bubble_rect.x + padding, bubble_rect.y + padding))
            
            msg_y += bubble_rect.height + 10

        # Opções de Resposta (Ficam no rodapé)
        options = data["options"]
        if options:
            opt_start_y = area.bottom - (len(options) * 35) - 10
            for i, opt in enumerate(options):
                color = self.colors["user_msg"] if i == self.selected_index else (100,100,100)
                
                # Botão de resposta
                btn_rect = pygame.Rect(area.x + 10, opt_start_y + (i*35), area.width - 20, 30)
                pygame.draw.rect(screen, color, btn_rect, border_radius=15)
                
                txt_surf = self.font_msg.render(opt["text"], True, (255,255,255))
                # Centralizar texto no botão
                txt_rect = txt_surf.get_rect(center=btn_rect.center)
                screen.blit(txt_surf, txt_rect)