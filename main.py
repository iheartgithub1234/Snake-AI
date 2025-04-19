import pygame
import random
from collections import deque

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.length = 1
        self.score = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_head = (head[0] + x, head[1] + y)
        
        # Check for wall collision
        if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            return False
            
        # Check for self collision
        if new_head in self.positions[1:]:
            return False
            
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True
    
    def grow(self):
        self.length += 1
        self.score += 1

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

class SnakeAI:
    def __init__(self, snake):
        self.snake = snake
    
    def is_valid_position(self, pos):
        x, y = pos
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return False
        return pos not in self.snake.positions
    
    def find_path(self, food_pos):
        head = self.snake.get_head_position()
        queue = deque([(head, [])])
        visited = set()
        visited.add(head)
        
        while queue:
            (x, y), path = queue.popleft()
            
            if (x, y) == food_pos:
                return path
            
            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and self.is_valid_position((nx, ny)):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(dx, dy)]))
        
        # If no path to food, find the move that maximizes available space
        best_move = None
        max_space = -1
        
        for dx, dy in [UP, DOWN, LEFT, RIGHT]:
            nx, ny = head[0] + dx, head[1] + dy
            if self.is_valid_position((nx, ny)):
                space = self.calculate_available_space((nx, ny))
                if space > max_space:
                    max_space = space
                    best_move = (dx, dy)
        
        return [best_move] if best_move else []

    def calculate_available_space(self, start_pos):
        visited = set()
        queue = deque([start_pos])
        count = 0
        
        while queue:
            x, y = queue.popleft()
            if (x, y) in visited:
                continue
                
            visited.add((x, y))
            count += 1
            
            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and self.is_valid_position((nx, ny)):
                    queue.append((nx, ny))
        
        return count

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, BLACK, rect, 1)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake AI")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 20)
    
    snake = Snake()
    food = Food()
    ai = SnakeAI(snake)
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # AI control
        path = ai.find_path(food.position)
        if path:
            snake.direction = path[0]
        
        if not snake.move():
            print(f"Game Over! Score: {snake.score}")
            snake = Snake()
            food = Food()
            ai = SnakeAI(snake)
            continue
        
        if snake.get_head_position() == food.position:
            snake.grow()
            food.randomize_position()
            while food.position in snake.positions:
                food.randomize_position()
        
        screen.fill(BLACK)
        draw_grid(screen)
        
        for pos in snake.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
        
        food_rect = pygame.Rect(food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, food_rect)
        pygame.draw.rect(screen, BLACK, food_rect, 1)
        
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (5, 5))
        
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()