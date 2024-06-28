import pygame
from pygame.locals import *
import random

pygame.init()

from pygame import mixer

mixer.init()
mixer.music.load('level-ix-211054.wav')

# Create the window
width = 700
height = 700
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# Colors
gray = (100, 100, 100)
sand = (237, 215, 201)
red = (200, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 182, 1)

# Road and marker sizes
road_width = 300
marker_width = 10
marker_height = 50

# Lane coordinates
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# Road and edge markers
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# For animating movement of the lane markers
lane_marker_move_y = 0

# Player's starting coordinates
player_x = 250
player_y = 400

# Frame settings
clock = pygame.time.Clock()
fps = 120

# Game settings
gameover = False
speed = 2
score = 0

# Define game states
MAIN_MENU = 0
OPTIONS = 1
PLAYING = 2
PAUSED = 3
GAME_OVER = 4
state = MAIN_MENU

class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # Scale the image down so it's not wider than the lane
        image_scale = 45 / image.get_rect().width
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)

# Sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Create the player's car
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Load the vehicle images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)
    
# Load the crash image
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

def main_menu():
    global state
    screen.fill(black)
    font = pygame.font.Font(None, 74)
    text = font.render("CAR GAME", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 50))
    
    font = pygame.font.Font(None, 36)
    text = font.render("Press S to Start", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 20))
    
    text = font.render("Press O for Options", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 60))
    
    text = font.render("Press E to Exit", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 100))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_s:
                mixer.music.play(-1)
                state = PLAYING
            if event.key == K_o:
                state = OPTIONS
            if event.key == K_e:
                pygame.quit()
                exit()

def options():
    global state
    screen.fill(black)
    font = pygame.font.Font(None, 74)
    text = font.render("OPTIONS", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, 50))
    
    font = pygame.font.Font(None, 36)
    text = font.render("Kelompok: 5", True, white)
    screen.blit(text, (50, 150))
    
    members = ["1. Rizka Amalia Muchtar (23.82.1751)", "2. Mulyati (23.82.1713)", "3. Febriana Rahmawati", "4. Syahmia (23.82.1750)", "5. Ilham Hikmai Hakim (23.82.1717)", "6. Muh Fadhil Raffi B Lapuka (23.82.1755)"]
    for i, member in enumerate(members):
        text = font.render(member, True, white)
        screen.blit(text, (50, 200 + i * 30))
    
    text = font.render("Press B to go Back", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, height - 100))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_b:
                state = MAIN_MENU

def game_over():
    global state
    screen.fill(red)
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 50))
    
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 20))
    
    text = font.render("Press Y to play again", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 60))
    text = font.render("Press N to quit", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 100))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_y:
                reset_game()
                state = MAIN_MENU
            if event.key == K_n:
                pygame.quit()
                exit()

def reset_game():
    global gameover, speed, score, vehicle_group, player
    gameover = False
    speed = 2
    score = 0
    vehicle_group.empty()
    player.rect.center = [player_x, player_y]

def game_loop():
    global state, lane_marker_move_y, gameover, speed, score
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
            
        # Move the player's car using the left/right arrow keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
            elif event.key == K_SPACE:
                state = PAUSED
                
            # Check if there's a side swipe collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    gameover = True
                    # Place the player's car next to other vehicle
                    # And determine where to position the crash image
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
    
    # Draw the grass
    screen.fill(sand)
    
    # Draw the road
    pygame.draw.rect(screen, gray, road)
    
    # Draw the edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)
    
    # Draw the lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, yellow, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, yellow, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        
    # Draw the player's car
    player_group.draw(screen)
    
    # Add a vehicle
    if len(vehicle_group) < 2:
        # Ensure there's enough gap between vehicles
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
                
        if add_vehicle:
            # Select a random lane
            lane = random.choice(lanes)
            # Select a random vehicle image
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)
    
    # Make the vehicles move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        
        # Remove vehicle once it goes off screen
        if vehicle.rect.top >= height:
            vehicle.kill()
            # Add to score
            score += 1
            # Speed up the game after passing 5 vehicles
            if score > 0 and score % 5 == 0:
                speed += 1
    
    # Draw the vehicles
    vehicle_group.draw(screen)
    
    # Display the score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 400)
    screen.blit(text, text_rect)
    
    # Check if there's a head on collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
            
    # Display game over
    if gameover:
        state = GAME_OVER
        mixer.music.stop()
            
    pygame.display.update()

def pause_menu():
    global state
    font = pygame.font.Font(None, 74)
    text = font.render("PAUSED", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    
    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to resume", True, white)
    screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 50))
    
    pygame.display.flip()
    
    while state == PAUSED:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    state = PLAYING

# Main loop
running = True
while running:
    if state == MAIN_MENU:
        main_menu()
    elif state == OPTIONS:
        options()
    elif state == PLAYING:
        game_loop()
    elif state == PAUSED:
        pause_menu()
    elif state == GAME_OVER:
        game_over()

pygame.quit()
