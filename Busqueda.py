import pygame
import random
import time

WIDTH, HEIGHT = 900, 500
FPS = 60
WHITE = (240, 240, 240)
BLUE = (50, 150, 255)
RED = (255, 80, 80)
GREEN = (80, 255, 80)
GRAY = (100, 100, 100)
BLACK = (30, 30, 30)

class SearchVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Simulador de Algoritmos de Búsqueda")
        self.font = pygame.font.SysFont("Arial", 18)
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.reset_data()

    def reset_data(self):
        self.n = 50 
        self.data = sorted([random.randint(10, 490) for _ in range(self.n)])
        self.target_idx = random.randint(0, self.n - 1)
        self.target_value = self.data[self.target_idx]
        self.current_idx = -1
        self.low = -1
        self.high = -1
        self.found = False
        self.steps = 0
        self.algo_name = "Presiona 1-4 para iniciar"

    def draw(self, special_idx=-1, range_lo=-1, range_hi=-1):
        self.screen.fill(WHITE)
        
        # titulo, info
        title = self.title_font.render(f"Algoritmo: {self.algo_name}", True, BLACK)
        info = self.font.render(f"Buscando el valor: {self.target_value} | Pasos: {self.steps}", True, BLACK)
        controls = self.font.render("[1] Lineal  [2] Binaria  [3] Exponencial  [4] Interpolación  [R] Reiniciar", True, GRAY)
        
        self.screen.blit(title, (20, 20))
        self.screen.blit(info, (20, 55))
        self.screen.blit(controls, (20, HEIGHT - 40))

        # Dibujar barras
        bar_width = (WIDTH - 100) // self.n
        for i in range(self.n):
            color = BLUE
            if i == special_idx: color = RED # Puntero actual
            elif i == self.target_idx and self.found: color = GREEN # Encontrado
            elif range_lo <= i <= range_hi and range_lo != -1: color = (200, 200, 255) # Rango activo
            
            height = self.data[i]
            pygame.draw.rect(self.screen, color, (50 + i * bar_width, HEIGHT - height - 60, bar_width - 2, height))
            
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: self.reset_data()
                if event.key == pygame.K_1: self.linear_search()
                if event.key == pygame.K_2: self.binary_search()
                if event.key == pygame.K_3: self.exponential_search()
                if event.key == pygame.K_4: self.interpolation_search()


    def linear_search(self):
        self.reset_data()
        self.algo_name = "Búsqueda Lineal"
        for i in range(len(self.data)):
            self.steps += 1
            self.draw(special_idx=i)
            time.sleep(0.1)
            if self.data[i] == self.target_value:
                self.found = True
                break
        self.draw()

    def binary_search(self, lo=0, hi=None, is_sub=False):
        if not is_sub:
            self.reset_data()
            self.algo_name = "Búsqueda Binaria"
            hi = len(self.data) - 1
        
        while lo <= hi:
            self.steps += 1
            mid = (lo + hi) // 2
            self.draw(special_idx=mid, range_lo=lo, range_hi=hi)
            time.sleep(0.5)
            
            if self.data[mid] == self.target_value:
                self.found = True; break
            elif self.data[mid] < self.target_value: lo = mid + 1
            else: hi = mid - 1
        self.draw()

    def exponential_search(self):
        self.reset_data()
        self.algo_name = "Búsqueda Exponencial"
        self.steps = 1
        if self.data[0] == self.target_value:
            self.found = True
        else:
            i = 1
            while i < len(self.data) and self.data[i] <= self.target_value:
                self.draw(special_idx=i)
                time.sleep(0.5)
                self.steps += 1
                if self.data[i] == self.target_value:
                    self.found = True
                    break
                i *= 2
            
            if not self.found:
                # Hace binaria en el rango encontrado
                lo, hi = i // 2, min(i, len(self.data) - 1)
                self.binary_search(lo, hi, is_sub=True)
        self.draw()

    def interpolation_search(self):
        self.reset_data()
        self.algo_name = "Búsqueda por Interpolación"
        lo, hi = 0, len(self.data) - 1
        
        while lo <= hi and self.data[lo] <= self.target_value <= self.data[hi]:
            self.steps += 1
            if lo == hi:
                if self.data[lo] == self.target_value: self.found = True
                break
            
            # Fórmula de posición estimada
            pos = lo + int(((float(hi - lo) / (self.data[hi] - self.data[lo])) * (self.target_value - self.data[lo])))
            
            self.draw(special_idx=pos, range_lo=lo, range_hi=hi)
            time.sleep(0.8)
            
            if self.data[pos] == self.target_value:
                self.found = True; break
            if self.data[pos] < self.target_value: lo = pos + 1
            else: hi = pos - 1
        self.draw()

    def run(self):
        while True:
            self.draw()
            self.check_events()

if __name__ == "__main__":
    SearchVisualizer().run()