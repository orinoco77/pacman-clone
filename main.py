import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
FPS = 60
TILE_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Maze (1 = wall, 0 = pellet, 2 = empty/pacman start, 3 = power pellet)
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,3,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,3,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1],
    [1,0,1,1,1,1,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,0,1,1,0,1,1,0,0,0,0,1,1,0,1,1,0,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1],
    [1,1,1,0,1,1,0,1,1,1,1,1,1,2,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1],
    [1,1,1,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1],
    [1,0,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.game_over = False
        self.win = False
        
        self.pacman = Pacman()
        self.ghosts = self.spawn_ghosts()
        self.pellets = []
        self.power_pellets = []
        self.setup_maze()

    def spawn_ghosts(self):
        colors = [RED, PINK, CYAN, ORANGE]
        ghosts = []
        # Find all empty/non-wall tiles for potential spawn points
        empty_tiles = []
        for r in range(len(MAZE)):
            for c in range(len(MAZE[0])):
                if MAZE[r][c] != 1:
                    empty_tiles.append((r, c))
        
        # Randomly pick 4 distinct tiles for ghosts
        spawn_points = random.sample(empty_tiles, 4)
        for i in range(4):
            r, c = spawn_points[i]
            # Note: Ghost(c, r, color) because the class expects X(col) then Y(row)
            ghosts.append(Ghost(c, r, colors[i]))
        return ghosts

    def setup_maze(self):
        for r in range(len(MAZE)):
            for c in range(len(MAZE[0])):
                if MAZE[r][c] == 0:
                    self.pellets.append(pygame.Rect(c * TILE_SIZE + 2, r * TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4))
                elif MAZE[r][c] == 3:
                    self.power_pellets.append(pygame.Rect(c * TILE_SIZE + 2, r * TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4))

    def run(self):
        while self.running:
            self.handle_events()
            if not self.game_over and not self.win:
                self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and self.game_over:
                self.__init__() # Reset game

    def update(self):
        self.pacman.move()
        
        # Pellet collection
        pacman_rect = self.pacman.get_rect()
        for pellet in self.pellets[:]:
            if pacman_rect.colliderect(pellet):
                self.pellets.remove(pellet)
                self.score += 10
        
        for pp in self.power_pellets[:]:
            if pacman_rect.colliderect(pp):
                self.power_pellets.remove(pp)
                self.score += 50
                for g in self.ghosts:
                    g.scared = True
                    g.scared_timer = 600 # 10 seconds at 60 FPS

        # Ghost movement and collisions
        for ghost in self.ghosts:
            ghost.move()
            if ghost.get_rect().colliderect(pacman_rect):
                if ghost.scared:
                    ghost.reset()
                    self.score += 200
                else:
                    self.game_over = True

        # Check win condition
        if not self.pellets and not self.power_pellets:
            self.win = True

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw Maze
        for r in range(len(MAZE)):
            for c in range(len(MAZE[0])):
                if MAZE[r][c] == 1:
                    pygame.draw.rect(self.screen, BLUE, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
        
        # Draw Pellets
        for p in self.pellets:
            pygame.draw.circle(self.screen, WHITE, p.center, 2)
        for pp in self.power_pellets:
            pygame.draw.circle(self.screen, WHITE, pp.center, 5)
            
        # Draw Pacman
        self.pacman.draw(self.screen)
        
        # Draw Ghosts
        for g in self.ghosts:
            g.draw(self.screen)
            
        # Draw UI
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
        
        if self.game_over:
            text = font.render("GAME OVER! Press any key to restart", True, RED)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        elif self.win:
            text = font.render("YOU WIN! Press any key to restart", True, YELLOW)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            
        pygame.display.flip()

class Pacman:
    def __init__(self):
        self.x, self.y = 13 * TILE_SIZE, 13 * TILE_SIZE
        self.vel = 2
        self.dir = (0, 0)
        self.next_dir = (0, 0)
        self.radius = TILE_SIZE // 2 - 2

    def get_rect(self):
        return pygame.Rect(self.x + 2, self.y + 2, TILE_SIZE - 4, TILE_SIZE - 4)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.next_dir = (-1, 0)
        if keys[pygame.K_RIGHT]: self.next_dir = (1, 0)
        if keys[pygame.K_UP]: self.next_dir = (0, -1)
        if keys[pygame.K_DOWN]: self.next_dir = (0, 1)

        # Try to change direction
        if self.can_move(self.next_dir):
            self.dir = self.next_dir

        if self.can_move(self.dir):
            self.x += self.dir[0] * self.vel
            self.y += self.dir[1] * self.vel

        # Snap to grid for better turning
        if self.dir[0] != 0 and self.x % TILE_SIZE == 0:
            pass # Valid snap
        elif self.dir[1] != 0 and self.y % TILE_SIZE == 0:
            pass # Valid snap
        
        # Simple grid alignment to prevent drifting
        if self.dir == (0,0): return
        
        # Normalize position to grid when turning or moving
        if self.dir[0] != 0 and self.x % TILE_SIZE != 0:
            # If we are slightly off, let's not snap unless we are moving’
            pass

    def can_move(self, direction):
        nx = self.x + direction[0] * self.vel
        ny = self.y + direction[1] * self.vel
        
        # Check 4 corners of the pacman square
        for ox, oy in [(2,2), (TILE_SIZE-2, 2), (2, TILE_SIZE-2), (TILE_SIZE-2, TILE_SIZE-2)]:
            cx = (nx + ox) // TILE_SIZE
            cy = (ny + oy) // TILE_SIZE
            if cx < 0 or cx >= len(MAZE[0]) or cy < 0 or cy >= len(MAZE):
                return False
            if MAZE[cy][cx] == 1:
                return False
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, 
                           (int(self.x + TILE_SIZE//2), int(self.y + TILE_SIZE//2)), self.radius)

class Ghost:
    def __init__(self, start_x, start_y, color):
        self.x, self.y = start_x * TILE_SIZE, start_y * TILE_SIZE
        self.color = color
        self.vel = 2
        self.dir = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.scared = False
        self.scared_timer = 0

    def get_rect(self):
        return pygame.Rect(self.x + 2, self.y + 2, TILE_SIZE - 4, TILE_SIZE - 4)

    def move(self):
        if self.scared_timer > 0:
            self.scared_timer -= 1
            if self.scared_timer == 0:
                self.scared = False

        # Random move at intersections
        if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
            possible_dirs = [(1,0), (-1,0), (0,1), (0,-1)]
            # Prevent reversing immediately unless necessary
            opposite = (-self.dir[0], -self.dir[1])
            valid_dirs = [d for d in possible_dirs if self.can_move(d) and d != opposite]
            if not valid_dirs: valid_dirs = [d for d in possible_dirs if self.can_move(d)]
            
            if valid_dirs:
                self.dir = random.choice(valid_dirs)

        if self.can_move(self.dir):
            self.x += self.dir[0] * self.vel
            self.y += self.dir[1] * self.vel
        else:
            # If hit wall, pick new dir immediately
            self.dir = random.choice([(1,0), (-1,0), (0,1), (0,-1)])

    def can_move(self, direction):
        nx = self.x + direction[0] * self.vel
        ny = self.y + direction[1] * self.vel
        for ox, oy in [(2,2), (TILE_SIZE-2, 2), (2, TILE_SIZE-2), (TILE_SIZE-2, TILE_SIZE-2)]:
            cx = (nx + ox) // TILE_SIZE
            cy = (ny + oy) // TILE_SIZE
            if cx < 0 or cx >= len(MAZE[0]) or cy < 0 or cy >= len(MAZE):
                return False
            if MAZE[cy][cx] == 1:
                return False
        return True

    def reset(self):
        # Find a random non-wall tile for reset instead of a hardcoded position
        empty_tiles = []
        for r in range(len(MAZE)):
            for c in range(len(MAZE[0])):
                if MAZE[r][c] != 1:
                    empty_tiles.append((c, r)) # Store as (x, y) for consistency
        
        self.x, self.y = random.choice(empty_tiles)
        self.x *= TILE_SIZE
        self.y *= TILE_SIZE
        self.scared = False

    def draw(self, screen):
        color = (0, 0, 255) if self.scared else self.color # Blue if scared
        pygame.draw.circle(screen, color, (int(self.x + TILE_SIZE//2), int(self.y + TILE_SIZE//2)), TILE_SIZE//2 - 2)

if __name__ == "__main__":
    game = Game()
    game.run()
