import pygame, sys, random      #paketleri kullanabilmek için sisteme dahil ediyorum

# Ekran boyutlarý ve renk tanýmlarý
screen_width = 600  
screen_height = 600  
gridsize = 20
grid_width = int(screen_width / gridsize)
grid_height = int(screen_height / gridsize)

# Renkler
light_green = (0, 170, 140)
dark_green = (0, 140, 120)
food_color = (250, 200, 0)
snake_color = (34, 34, 34)
button_color = (200, 50, 50)
text_color = (0, 0, 0)          #sdfsdf

# Yönler
up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)

# Yýlan sýnýfý
class SNAKE:
    def __init__(self):
        self.positions = [(screen_width / 2, screen_height / 2)]
        self.length = 1
        self.direction = random.choice([up, down, left, right])
        self.color = snake_color
        self.score = 0

    def move(self):
        current = self.positions[0]
        x, y = self.direction
        new = ((current[0] + (x * gridsize)), (current[1] + (y * gridsize)))

        if new[0] in range(0, screen_width) and new[1] in range(0, screen_height) and not new in self.positions[2:]:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        else:
            self.reset()

    def reset(self):
        global game_over
        self.length = 1
        self.positions = [(screen_width / 2, screen_height / 2)]
        self.direction = random.choice([up, down, left, right])
        self.score = 0
        game_over = True  # Oyunun sonlandýðýný belirtiyoruz

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)

    def turn(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def draw(self, surface):
        for p in self.positions:
            rect = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, rect)

# Yemek sýnýfý
class FOOD:
    def __init__(self):
        self.position = (0, 0)
        self.color = food_color
        self.random_position()

    def random_position(self):
        self.position = (random.randint(0, grid_width - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)

    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, rect)

# Oyun alanýný çizen fonksiyon
def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x + y) % 2 == 0:
                light = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, light_green, light)
            else:
                dark = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, dark_green, dark)

# Ana oyun fonksiyonu
def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.Font(pygame.font.match_font('arial', bold=True), 20)
    game_over_font = pygame.font.Font(pygame.font.get_default_font(), 40)  # Piksel tarzý kalýn font
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    food = FOOD()
    snake = SNAKE()

    global game_over
    game_over = False

    while True:
        snake.handle_keys()
        if not game_over:
            snake.move()
        
        surface.fill((0, 0, 0))  # Temizleme
        drawGrid(surface)
        
        # Yemek yendiðinde skoru arttýrma ve yýlaný büyütme
        if snake.positions[0] == food.position:
            snake.length += 1
            snake.score += 1
            food.random_position()
        
        food.draw(surface)
        snake.draw(surface)
        screen.blit(surface, (0, 0))
        
        # Skor gösterimi
        score_text = font.render(f"Score: {snake.score}", True, text_color)
        screen.blit(score_text, (10, 10))

        if game_over:
            # "Kaybettiniz" yazýsý
            game_over_text = game_over_font.render("Kaybettiniz", True, text_color)
            screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, screen_height / 2 - 60))
            
            # Skor yazýsý
            final_score_text = font.render(f"Skorunuz: {snake.score}", True, text_color)
            screen.blit(final_score_text, (screen_width / 2 - final_score_text.get_width() / 2, screen_height / 2))
            
            # "Yeniden Oyna" butonu
            button_rect = pygame.Rect(screen_width / 2 - 75, screen_height / 2 + 40, 150, 50)
            pygame.draw.rect(screen, button_color, button_rect)
            button_text = font.render("Yeniden Oyna", True, text_color)
            screen.blit(button_text, (screen_width / 2 - button_text.get_width() / 2, screen_height / 2 + 50))
            
            # Fare ile butona týklama kontrolü
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:  # Sol fare tuþuna týklama
                    game_over = False
                    snake.reset()  # Yýlaný sýfýrla
                    food.random_position()  # Yeni yemek pozisyonu

        pygame.display.update()     #Güncellemerlin ekranda yenilenmesini saðlýyor
        clock.tick(10)  # Yýlanýn ilerleme hýzý

main()
