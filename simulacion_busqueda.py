import pygame
import random
import time

# --- CONFIGURACIÓN DE ESTILO ---
WIDTH, HEIGHT = 1000, 700
FPS = 60
COLOR_BG = (30, 32, 45)       # Fondo oscuro profesional
COLOR_CARD = (45, 48, 65)     # Color de los paneles
COLOR_ACCENT = (0, 200, 255)  # Azul brillante
WHITE = (240, 240, 240)
GRAY = (150, 150, 150)
RED = (255, 85, 85)
GREEN = (80, 250, 120)

class Button:
    def __init__(self, x, y, w, h, text, color, action_id):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.action_id = action_id
        self.hovered = False

    def draw(self, screen, font):
        color = (min(self.color[0]+30, 255), min(self.color[1]+30, 255), min(self.color[2]+30, 255)) if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8) # Borde
        txt_surf = font.render(self.text, True, WHITE)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, txt_rect)

class SearchApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Visualizador Maestro de Algoritmos")
        self.font_sm = pygame.font.SysFont("Segoe UI", 18)
        self.font_md = pygame.font.SysFont("Segoe UI", 22, bold=True)
        self.font_lg = pygame.font.SysFont("Segoe UI", 32, bold=True)
        
        self.buttons = [
            Button(50, 580, 160, 45, "1. Lineal", (70, 80, 120), 1),
            Button(230, 580, 160, 45, "2. Binaria", (70, 80, 120), 2),
            Button(410, 580, 160, 45, "3. Exponencial", (70, 80, 120), 3),
            Button(590, 580, 160, 45, "4. Interpolación", (70, 80, 120), 4),
            Button(800, 580, 150, 45, "Reiniciar [R]", (180, 70, 70), 'R')
        ]
        
        self.reset_data()

    def reset_data(self):
        self.n = 40
        self.data = sorted([random.randint(20, 350) for _ in range(self.n)])
        self.target_idx = random.randint(0, self.n - 1)
        self.target_val = self.data[self.target_idx]
        self.active_idx = -1
        self.lo, self.hi = -1, -1
        self.found = False
        self.steps = 0
        self.algo_name = "Seleccione un algoritmo"
        self.desc = "Los algoritmos de búsqueda permiten encontrar un dato en una estructura. Los métodos avanzados requieren orden previo."

    def draw_layout(self):
        self.screen.fill(COLOR_BG)
        
        # Panel Principal (Gráfico)
        main_panel = pygame.Rect(30, 80, 940, 400)
        pygame.draw.rect(self.screen, COLOR_CARD, main_panel, border_radius=15)
        
        # Panel de Descripción
        desc_panel = pygame.Rect(30, 495, 940, 60)
        pygame.draw.rect(self.screen, COLOR_CARD, desc_panel, border_radius=10)
        
        # Títulos
        title = self.font_lg.render("Simulador de Búsqueda Visual", True, COLOR_ACCENT)
        self.screen.blit(title, (30, 20))
        
        # Info de estado
        info_txt = self.font_md.render(f"Objetivo: {self.target_val}  |  Pasos: {self.steps}  |  Algoritmo: {self.algo_name}", True, WHITE)
        self.screen.blit(info_txt, (30, 455))
        
        # Texto de descripción dinámica
        desc_surf = self.font_sm.render(self.desc, True, GRAY)
        self.screen.blit(desc_surf, (50, 512))

        # Dibujar Barras
        bw = (main_panel.width - 100) // self.n
        for i, val in enumerate(self.data):
            color = COLOR_ACCENT
            if i == self.active_idx: color = RED
            elif self.found and i == self.target_idx: color = GREEN
            elif self.lo <= i <= self.hi and self.lo != -1: color = (80, 90, 130)
            
            x = main_panel.x + 50 + (i * bw)
            y = main_panel.bottom - val - 30
            pygame.draw.rect(self.screen, color, (x, y, bw - 4, val), border_radius=4)

        # Dibujar Botones
        for btn in self.buttons:
            btn.draw(self.screen, self.font_sm)

    def update_visuals(self, idx=-1, l=-1, r=-1):
        self.active_idx = idx
        self.lo, self.hi = l, r
        self.draw_layout()
        pygame.display.flip()
        time.sleep(0.2) # Velocidad de la animación

    # --- ALGORITMOS ---

    def run_linear(self):
        self.reset_data()
        self.algo_name = "Búsqueda Lineal"
        self.desc = "Explora secuencialmente cada elemento. Eficiencia: O(n). Útil para datos desordenados."
        for i in range(len(self.data)):
            self.steps += 1
            self.update_visuals(idx=i)
            if self.data[i] == self.target_val:
                self.found = True; break

    def run_binary(self, l=0, r=None, sub=False):
        if not sub:
            self.reset_data()
            self.algo_name = "Búsqueda Binaria"
            self.desc = "Divide el rango a la mitad en cada paso. Eficiencia: O(log n). Requiere orden."
            r = len(self.data) - 1
        
        while l <= r:
            self.steps += 1
            mid = (l + r) // 2
            self.update_visuals(idx=mid, l=l, r=r)
            if self.data[mid] == self.target_val:
                self.found = True; break
            elif self.data[mid] < self.target_val: l = mid + 1
            else: r = mid - 1

    def run_exponential(self):
        self.reset_data()
        self.algo_name = "Búsqueda Exponencial"
        self.desc = "Busca el rango saltando en potencias de 2 y luego aplica Binaria."
        self.steps = 1
        if self.data[0] == self.target_val: self.found = True
        else:
            i = 1
            while i < len(self.data) and self.data[i] <= self.target_val:
                self.update_visuals(idx=i)
                self.steps += 1
                if self.data[i] == self.target_val: self.found = True; break
                i *= 2
            if not self.found:
                self.run_binary(i // 2, min(i, len(self.data)-1), sub=True)

    def run_interpolation(self):
        self.reset_data()
        self.algo_name = "Búsqueda por Interpolación"
        self.desc = "Estima la posición basándose en los valores extremos. Eficiencia: O(log(log n))."
        l, r = 0, len(self.data) - 1
        while l <= r and self.data[l] <= self.target_val <= self.data[r]:
            self.steps += 1
            if l == r:
                if self.data[l] == self.target_val: self.found = True
                break
            pos = l + int(((r - l) / (self.data[r] - self.data[l])) * (self.target_val - self.data[l]))
            self.update_visuals(idx=pos, l=l, r=r)
            if self.data[pos] == self.target_val:
                self.found = True; break
            if self.data[pos] < self.target_val: l = pos + 1
            else: r = pos - 1

    def handle_click(self, pos):
        for btn in self.buttons:
            if btn.rect.collidepoint(pos):
                if btn.action_id == 1: self.run_linear()
                if btn.action_id == 2: self.run_binary()
                if btn.action_id == 3: self.run_exponential()
                if btn.action_id == 4: self.run_interpolation()
                if btn.action_id == 'R': self.reset_data()

    def main_loop(self):
        running = True
        while running:
            m_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.MOUSEBUTTONDOWN: self.handle_click(event.pos)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r: self.reset_data()

            for btn in self.buttons:
                btn.hovered = btn.rect.collidepoint(m_pos)

            self.draw_layout()
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    SearchApp().main_loop()