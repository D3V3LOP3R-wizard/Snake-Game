import pygame
import random
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    HIGH_SCORES = 4

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4

class SnakeGame:
    def __init__(self):
        # Window settings
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.GRID_SIZE = 20
        self.GRID_WIDTH = self.WINDOW_WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.WINDOW_HEIGHT // self.GRID_SIZE
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (128, 0, 128)
        self.ORANGE = (255, 165, 0)
        self.GRAY = (128, 128, 128)
        self.DARK_GREEN = (0, 150, 0)
        self.LIGHT_GREEN = (144, 238, 144)
        self.BACKGROUND = (20, 20, 30)
        
        # Game settings
        self.difficulty_speeds = {
            Difficulty.EASY: 10,
            Difficulty.MEDIUM: 15,
            Difficulty.HARD: 20,
            Difficulty.EXPERT: 25
        }
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 Snake Game")
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Game variables
        self.state = GameState.MENU
        self.difficulty = Difficulty.MEDIUM
        self.score = 0
        self.high_scores = self.load_high_scores()
        self.snake = []
        self.food = None
        self.direction = Direction.RIGHT
        self.game_speed = self.difficulty_speeds[self.difficulty]
        
    def load_high_scores(self):
        """Load high scores from file"""
        try:
            with open("snake_highscores.txt", "r") as f:
                scores = [int(line.strip()) for line in f.readlines()]
                return sorted(scores, reverse=True)[:5]
        except:
            return [0, 0, 0, 0, 0]
    
    def save_high_scores(self):
        """Save high scores to file"""
        with open("snake_highscores.txt", "w") as f:
            for score in self.high_scores:
                f.write(f"{score}\n")
    
    def update_high_scores(self):
        """Update high scores with current score"""
        self.high_scores.append(self.score)
        self.high_scores = sorted(self.high_scores, reverse=True)[:5]
        self.save_high_scores()
    
    def reset_game(self):
        """Reset game state"""
        self.snake = [(self.GRID_WIDTH // 2, self.GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.score = 0
        self.spawn_food()
        self.game_speed = self.difficulty_speeds[self.difficulty]
    
    def spawn_food(self):
        """Spawn food at random location"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def handle_input(self):
        """Handle keyboard input"""
        keys = pygame.key.get_pressed()
        
        if self.state == GameState.PLAYING:
            if keys[pygame.K_UP] and self.direction != Direction.DOWN:
                self.direction = Direction.UP
            elif keys[pygame.K_DOWN] and self.direction != Direction.UP:
                self.direction = Direction.DOWN
            elif keys[pygame.K_LEFT] and self.direction != Direction.RIGHT:
                self.direction = Direction.LEFT
            elif keys[pygame.K_RIGHT] and self.direction != Direction.LEFT:
                self.direction = Direction.RIGHT
    
    def move_snake(self):
        """Move the snake"""
        head = self.snake[0]
        
        if self.direction == Direction.UP:
            new_head = (head[0], head[1] - 1)
        elif self.direction == Direction.DOWN:
            new_head = (head[0], head[1] + 1)
        elif self.direction == Direction.LEFT:
            new_head = (head[0] - 1, head[1])
        elif self.direction == Direction.RIGHT:
            new_head = (head[0] + 1, head[1])
        
        # Check for food collision
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.score += 10
            self.spawn_food()
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()
    
    def check_collisions(self):
        """Check for collisions"""
        head = self.snake[0]
        
        # Check wall collision
        if (head[0] < 0 or head[0] >= self.GRID_WIDTH or
            head[1] < 0 or head[1] >= self.GRID_HEIGHT):
            return True
        
        # Check self collision
        if head in self.snake[1:]:
            return True
        
        return False
    
    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(self.BACKGROUND)
        
        # Title
        title_text = self.font_large.render("🐍 SNAKE GAME", True, self.GREEN)
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Menu options
        options = [
            ("Press SPACE to Start", self.WHITE),
            ("Press D for Difficulty", self.YELLOW),
            ("Press H for High Scores", self.BLUE),
            ("Press ESC to Quit", self.RED)
        ]
        
        for i, (text, color) in enumerate(options):
            option_text = self.font_medium.render(text, True, color)
            option_rect = option_text.get_rect(center=(self.WINDOW_WIDTH // 2, 250 + i * 60))
            self.screen.blit(option_text, option_rect)
        
        # Current difficulty
        diff_text = self.font_small.render(
            f"Current Difficulty: {self.difficulty.name}",
            True,
            self.ORANGE
        )
        diff_rect = diff_text.get_rect(center=(self.WINDOW_WIDTH // 2, 500))
        self.screen.blit(diff_text, diff_rect)
        
        pygame.display.flip()
    
    def draw_game(self):
        """Draw game screen"""
        self.screen.fill(self.BACKGROUND)
        
        # Draw grid (optional, for visual effect)
        for x in range(0, self.WINDOW_WIDTH, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.GRAY, (x, 0), (x, self.WINDOW_HEIGHT), 1)
        for y in range(0, self.WINDOW_HEIGHT, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.GRAY, (0, y), (self.WINDOW_WIDTH, y), 1)
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            x = segment[0] * self.GRID_SIZE
            y = segment[1] * self.GRID_SIZE
            
            # Gradient color for snake (head is brighter)
            if i == 0:
                color = self.LIGHT_GREEN
            else:
                color = self.DARK_GREEN
            
            pygame.draw.rect(
                self.screen,
                color,
                (x + 2, y + 2, self.GRID_SIZE - 4, self.GRID_SIZE - 4)
            )
            pygame.draw.rect(
                self.screen,
                self.WHITE,
                (x + 2, y + 2, self.GRID_SIZE - 4, self.GRID_SIZE - 4),
                1
            )
        
        # Draw food
        if self.food:
            x = self.food[0] * self.GRID_SIZE
            y = self.food[1] * self.GRID_SIZE
            pygame.draw.circle(
                self.screen,
                self.RED,
                (x + self.GRID_SIZE // 2, y + self.GRID_SIZE // 2),
                self.GRID_SIZE // 2 - 2
            )
        
        # Draw score
        score_text = self.font_small.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw difficulty
        diff_text = self.font_small.render(
            f"Difficulty: {self.difficulty.name}",
            True,
            self.YELLOW
        )
        self.screen.blit(diff_text, (self.WINDOW_WIDTH - 200, 10))
        
        pygame.display.flip()
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(self.BACKGROUND)
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER!", True, self.RED)
        game_over_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, 150))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, self.WHITE)
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, 250))
        self.screen.blit(score_text, score_rect)
        
        # High score message if achieved
        if self.score >= self.high_scores[0]:
            high_score_text = self.font_medium.render("NEW HIGH SCORE! 🏆", True, self.YELLOW)
            high_score_rect = high_score_text.get_rect(center=(self.WINDOW_WIDTH // 2, 320))
            self.screen.blit(high_score_text, high_score_rect)
        
        # Options
        options = [
            ("Press SPACE to Play Again", self.GREEN),
            ("Press M for Menu", self.BLUE),
            ("Press ESC to Quit", self.RED)
        ]
        
        for i, (text, color) in enumerate(options):
            option_text = self.font_small.render(text, True, color)
            option_rect = option_text.get_rect(center=(self.WINDOW_WIDTH // 2, 400 + i * 50))
            self.screen.blit(option_text, option_rect)
        
        pygame.display.flip()
    
    def draw_high_scores(self):
        """Draw high scores screen"""
        self.screen.fill(self.BACKGROUND)
        
        # Title
        title_text = self.font_large.render("🏆 HIGH SCORES", True, self.YELLOW)
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Display high scores
        for i, score in enumerate(self.high_scores):
            if score > 0:
                medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
                score_text = self.font_medium.render(
                    f"{medal} {score}",
                    True,
                    self.WHITE if i > 2 else [self.YELLOW, self.GRAY, self.ORANGE][i]
                )
                score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, 200 + i * 60))
                self.screen.blit(score_text, score_rect)
        
        # Back instruction
        back_text = self.font_small.render("Press B to go Back", True, self.BLUE)
        back_rect = back_text.get_rect(center=(self.WINDOW_WIDTH // 2, 550))
        self.screen.blit(back_text, back_rect)
        
        pygame.display.flip()
    
    def change_difficulty(self):
        """Cycle through difficulties"""
        difficulties = list(Difficulty)
        current_index = difficulties.index(self.difficulty)
        self.difficulty = difficulties[(current_index + 1) % len(difficulties)]
        self.game_speed = self.difficulty_speeds[self.difficulty]
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == GameState.PLAYING:
                            self.state = GameState.MENU
                        else:
                            running = False
                    elif event.key == pygame.K_SPACE:
                        if self.state == GameState.MENU:
                            self.reset_game()
                            self.state = GameState.PLAYING
                        elif self.state == GameState.GAME_OVER:
                            self.reset_game()
                            self.state = GameState.PLAYING
                    elif event.key == pygame.K_d and self.state == GameState.MENU:
                        self.change_difficulty()
                    elif event.key == pygame.K_h and self.state == GameState.MENU:
                        self.state = GameState.HIGH_SCORES
                    elif event.key == pygame.K_b and self.state == GameState.HIGH_SCORES:
                        self.state = GameState.MENU
                    elif event.key == pygame.K_m and self.state == GameState.GAME_OVER:
                        self.state = GameState.MENU
            
            # Handle continuous input
            self.handle_input()
            
            # Update game state
            if self.state == GameState.PLAYING:
                self.move_snake()
                
                if self.check_collisions():
                    self.update_high_scores()
                    self.state = GameState.GAME_OVER
            
            # Draw based on state
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_game()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            elif self.state == GameState.HIGH_SCORES:
                self.draw_high_scores()
            
            # Control game speed
            self.clock.tick(self.game_speed)
        
        pygame.quit()
        sys.exit()

class SnakeGameWithPowerUps(SnakeGame):
    """Extended version with power-ups and obstacles"""
    
    def __init__(self):
        super().__init__()
        self.power_up = None
        self.power_up_timer = 0
        self.obstacles = []
        self.speed_boost = False
        self.invincible = False
        
    def reset_game(self):
        """Reset game with additional features"""
        super().reset_game()
        self.power_up = None
        self.power_up_timer = 0
        self.obstacles = []
        self.speed_boost = False
        self.invincible = False
        
        # Add obstacles for harder difficulties
        if self.difficulty in [Difficulty.HARD, Difficulty.EXPERT]:
            self.generate_obstacles()
    
    def generate_obstacles(self):
        """Generate obstacles on the grid"""
        num_obstacles = 5 if self.difficulty == Difficulty.HARD else 10
        
        for _ in range(num_obstacles):
            while True:
                x = random.randint(0, self.GRID_WIDTH - 1)
                y = random.randint(0, self.GRID_HEIGHT - 1)
                if (x, y) not in self.snake and (x, y) != self.food:
                    self.obstacles.append((x, y))
                    break
    
    def spawn_power_up(self):
        """Spawn a power-up at random location"""
        if random.random() < 0.01 and not self.power_up:  # 1% chance per frame
            while True:
                x = random.randint(0, self.GRID_WIDTH - 1)
                y = random.randint(0, self.GRID_HEIGHT - 1)
                if (x, y) not in self.snake and (x, y) != self.food and (x, y) not in self.obstacles:
                    power_up_type = random.choice(['speed', 'invincible', 'points'])
                    self.power_up = {'pos': (x, y), 'type': power_up_type}
                    break
    
    def move_snake(self):
        """Move snake with power-up effects"""
        head = self.snake[0]
        
        if self.direction == Direction.UP:
            new_head = (head[0], head[1] - 1)
        elif self.direction == Direction.DOWN:
            new_head = (head[0], head[1] + 1)
        elif self.direction == Direction.LEFT:
            new_head = (head[0] - 1, head[1])
        elif self.direction == Direction.RIGHT:
            new_head = (head[0] + 1, head[1])
        
        # Check for power-up collision
        if self.power_up and new_head == self.power_up['pos']:
            self.activate_power_up(self.power_up['type'])
            self.power_up = None
        
        # Check for food collision
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.score += 10
            self.spawn_food()
            self.spawn_power_up()
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()
    
    def activate_power_up(self, power_type):
        """Activate power-up effects"""
        if power_type == 'speed':
            self.speed_boost = True
            self.power_up_timer = 100
            self.game_speed = int(self.game_speed * 1.5)
        elif power_type == 'invincible':
            self.invincible = True
            self.power_up_timer = 150
        elif power_type == 'points':
            self.score += 50
        
    def update_power_up_timer(self):
        """Update power-up duration"""
        if self.power_up_timer > 0:
            self.power_up_timer -= 1
            if self.power_up_timer == 0:
                if self.speed_boost:
                    self.speed_boost = False
                    self.game_speed = self.difficulty_speeds[self.difficulty]
                if self.invincible:
                    self.invincible = False
    
    def check_collisions(self):
        """Check collisions with power-up considerations"""
        head = self.snake[0]
        
        # Check wall collision
        if (head[0] < 0 or head[0] >= self.GRID_WIDTH or
            head[1] < 0 or head[1] >= self.GRID_HEIGHT):
            return not self.invincible
        
        # Check self collision
        if head in self.snake[1:]:
            return not self.invincible
        
        # Check obstacle collision
        if head in self.obstacles:
            return not self.invincible
        
        return False
    
    def draw_game(self):
        """Draw game with additional features"""
        self.screen.fill(self.BACKGROUND)
        
        # Draw grid
        for x in range(0, self.WINDOW_WIDTH, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.GRAY, (x, 0), (x, self.WINDOW_HEIGHT), 1)
        for y in range(0, self.WINDOW_HEIGHT, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.GRAY, (0, y), (self.WINDOW_WIDTH, y), 1)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            x = obstacle[0] * self.GRID_SIZE
            y = obstacle[1] * self.GRID_SIZE
            pygame.draw.rect(
                self.screen,
                self.GRAY,
                (x + 2, y + 2, self.GRID_SIZE - 4, self.GRID_SIZE - 4)
            )
        
        # Draw snake with power-up effects
        for i, segment in enumerate(self.snake):
            x = segment[0] * self.GRID_SIZE
            y = segment[1] * self.GRID_SIZE
            
            if i == 0 and self.invincible:
                color = self.PURPLE
            elif i == 0:
                color = self.LIGHT_GREEN
            else:
                color = self.DARK_GREEN
            
            pygame.draw.rect(
                self.screen,
                color,
                (x + 2, y + 2, self.GRID_SIZE - 4, self.GRID_SIZE - 4)
            )
        
        # Draw food
        if self.food:
            x = self.food[0] * self.GRID_SIZE
            y = self.food[1] * self.GRID_SIZE
            pygame.draw.circle(
                self.screen,
                self.RED,
                (x + self.GRID_SIZE // 2, y + self.GRID_SIZE // 2),
                self.GRID_SIZE // 2 - 2
            )
        
        # Draw power-up
        if self.power_up:
            x = self.power_up['pos'][0] * self.GRID_SIZE
            y = self.power_up['pos'][1] * self.GRID_SIZE
            
            color = {
                'speed': self.YELLOW,
                'invincible': self.PURPLE,
                'points': self.BLUE
            }[self.power_up['type']]
            
            pygame.draw.rect(
                self.screen,
                color,
                (x + 4, y + 4, self.GRID_SIZE - 8, self.GRID_SIZE - 8)
            )
        
        # Draw score and power-up status
        score_text = self.font_small.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        if self.power_up_timer > 0:
            if self.speed_boost:
                status = "SPEED BOOST!"
            elif self.invincible:
                status = "INVINCIBLE!"
            status_text = self.font_small.render(status, True, self.YELLOW)
            self.screen.blit(status_text, (self.WINDOW_WIDTH // 2 - 50, 10))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop with power-up updates"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == GameState.PLAYING:
                            self.state = GameState.MENU
                        else:
                            running = False
                    elif event.key == pygame.K_SPACE:
                        if self.state == GameState.MENU:
                            self.reset_game()
                            self.state = GameState.PLAYING
                        elif self.state == GameState.GAME_OVER:
                            self.reset_game()
                            self.state = GameState.PLAYING
                    elif event.key == pygame.K_d and self.state == GameState.MENU:
                        self.change_difficulty()
                    elif event.key == pygame.K_h and self.state == GameState.MENU:
                        self.state = GameState.HIGH_SCORES
                    elif event.key == pygame.K_b and self.state == GameState.HIGH_SCORES:
                        self.state = GameState.MENU
                    elif event.key == pygame.K_m and self.state == GameState.GAME_OVER:
                        self.state = GameState.MENU
            
            self.handle_input()
            
            if self.state == GameState.PLAYING:
                self.move_snake()
                self.update_power_up_timer()
                
                if self.check_collisions():
                    self.update_high_scores()
                    self.state = GameState.GAME_OVER
            
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_game()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            elif self.state == GameState.HIGH_SCORES:
                self.draw_high_scores()
            
            self.clock.tick(self.game_speed)
        
        pygame.quit()
        sys.exit()

def main():
    """Main function to run the game"""
    print("🎮 Snake Game")
    print("=" * 40)
    print("1. Classic Snake")
    print("2. Snake with Power-ups")
    print("=" * 40)
    
    choice = input("Choose game mode (1 or 2): ").strip()
    
    if choice == "2":
        game = SnakeGameWithPowerUps()
    else:
        game = SnakeGame()
    
    game.run()

if __name__ == "__main__":
    main()