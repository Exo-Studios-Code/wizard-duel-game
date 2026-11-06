import pygame

# Inicializace Pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wizard Maze")

# Barvy pro kouzelnickou atmosféru
WHITE = (255, 255, 255)
MAGIC_BLUE = (0, 102, 204)
MAGIC_YELLOW = (255, 255, 128)
MAGIC_GREEN = (34, 139, 34)
RED = (255, 0, 0)
MAGIC_PURPLE = (128, 0, 128)

# Velikost políček mapy
TILE_SIZE = 20

# Velikost mapy
MAP_SIZE = 40  # Pro větší mapu s Hogwarts uprostřed (40x40)
MAP_CENTER = MAP_SIZE // 2

# Vytvoření mapy
import random

def generate_maze():
    maze = [['#' for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]

    def carve(x, y):
        dirs = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 1 <= nx < MAP_SIZE-1 and 1 <= ny < MAP_SIZE-1 and maze[ny][nx] == '#':
                maze[ny][nx] = '.'
                maze[y + dy // 2][x + dx // 2] = '.'
                carve(nx, ny)

    # Začínáme u [1,1]
    maze[1][1] = '.'
    carve(1, 1)

    return maze

def generate_map():
    """Vytvoří mapu s bludištěm a Hogwarts uprostřed"""
    map = generate_maze()

    # Vytvoření Hogwarts jako uzavřený blok
    hogwarts_width = 12
    hogwarts_height = 10
    start_x = MAP_CENTER - hogwarts_width // 2
    start_y = MAP_CENTER - hogwarts_height // 2

    # Stěny Hogwarts
    for y in range(start_y, start_y + hogwarts_height):
        for x in range(start_x, start_x + hogwarts_width):
            if x == start_x or x == start_x + hogwarts_width - 1 or y == start_y or y == start_y + hogwarts_height - 1:
                map[y][x] = '#'
            else:
                map[y][x] = '.'

    # Nápis "Hogwarts" uprostřed
    word = "Hogwarts"
    word_start_x = MAP_CENTER - len(word) // 2
    for i, letter in enumerate(word):
        map[start_y + hogwarts_height // 2][word_start_x + i] = letter

    return map


# Inicializace mapy
hogwarts_map = generate_map()

# Pozice hráče a nepřátel
player_pos = [1, 1]  # výchozí pozice hráče
enemy_positions = [[MAP_SIZE - 5, MAP_SIZE - 5], [MAP_CENTER + 5, MAP_CENTER + 5], [MAP_SIZE - 10, MAP_SIZE - 10]]

# Nastavení fontu pro vykreslení textu
font = pygame.font.SysFont('Arial', 24)

def draw_map():
    """Vykreslí mapu na obrazovku"""
    window.fill(WHITE)  # Vyplní obrazovku bílou barvou

    # Ověříme, že se pohybujeme v mezích mapy
    for y in range(len(hogwarts_map)):
        for x in range(len(hogwarts_map[y])):
            # Kreslení stěn (modrá pro kouzelnickou atmosféru)
            if hogwarts_map[y][x] == '#':
                pygame.draw.rect(window, MAGIC_BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            # Kreslení volného prostoru (žlutá pro magický prostor)
            elif hogwarts_map[y][x] == '.':
                pygame.draw.rect(window, MAGIC_YELLOW, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            # Kreslení nápisu Hogwarts
            elif isinstance(hogwarts_map[y][x], str):
                text = font.render(hogwarts_map[y][x], True, MAGIC_PURPLE)
                window.blit(text, (x * TILE_SIZE, y * TILE_SIZE))

    # Kreslení hráče (magická zelená)
    pygame.draw.rect(window, MAGIC_GREEN, (player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Kreslení nepřátel (červený)
    for enemy in enemy_positions:
        pygame.draw.rect(window, RED, (enemy[1] * TILE_SIZE, enemy[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    pygame.display.update()  # Aktualizace obrazovky

def move_player(dy, dx):
    """Funkce pro pohyb hráče"""
    new_y = player_pos[0] + dy
    new_x = player_pos[1] + dx

    # Ověření, že hráč není mimo hranice mapy a nenarazí na stěnu
    if 0 <= new_y < len(hogwarts_map) and 0 <= new_x < len(hogwarts_map[0]) and hogwarts_map[new_y][new_x] != '#':
        player_pos[0] = new_y
        player_pos[1] = new_x

from collections import deque

def bfs(start, goal, map_data):
    """Najde nejkratší cestu z start do goal pomocí BFS"""
    queue = deque()
    queue.append((start, []))
    visited = set()
    visited.add(tuple(start))

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path

        y, x = current
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < len(map_data) and 0 <= nx < len(map_data[0]):
                if map_data[ny][nx] != '#' and (ny, nx) not in visited:
                    visited.add((ny, nx))
                    queue.append(((ny, nx), path + [(ny, nx)]))
    return []

def move_enemies():
    """Chytřejší pohyb nepřátel - sledují hráče cestou přes bludiště"""
    global enemy_positions
    for i, enemy in enumerate(enemy_positions):
        path = bfs(enemy, player_pos, hogwarts_map)
        if path and len(path) > 0:
            next_step = path[0]  # vezme první krok směrem k hráči
            enemy_positions[i] = list(next_step)  # posune nepřítele


def game_loop():
    """Hlavní herní smyčka"""
    running = True
    while running:
        # Zpracování událostí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Pohyb hráče na základě kláves
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            move_player(-1, 0)
        elif keys[pygame.K_s]:
            move_player(1, 0)
        elif keys[pygame.K_a]:
            move_player(0, -1)
        elif keys[pygame.K_d]:
            move_player(0, 1)

        # Pohyb nepřátel
        move_enemies()

        # Kontrola, jestli nepřítel zasáhl hráče
        if player_pos in enemy_positions:
            print("\n👹 Nepřítel tě zasáhl! Konec hry!")
            running = False

        draw_map()  # Vykreslení mapy s novými pozicemi

        pygame.time.Clock().tick(30)  # Ovládání FPS (30 FPS)

    pygame.quit()

# Spuštění
if __name__ == "__main__":
    try:
        game_loop()
    except Exception as e:
        print(f"Chyba: {e}")
        pygame.quit()
