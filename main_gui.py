import pygame
import sys
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
PURPLE = (178, 0, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 100, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Input box dimensions
INPUT_WIDTH = 500
INPUT_HEIGHT = 40
INPUT_LEFT_MARGIN = 350
LABEL_LEFT_MARGIN = 100
VERTICAL_SPACING = 100

# Button dimensions
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 50
BUTTON_SPACING = 60

# Create the window and set up display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Twitch Cooker")

# Load mascot image and laugh sound
try:
    mascot_image = pygame.image.load('mascot.png')
    mascot_rect = mascot_image.get_rect()
    mascot_rect.topleft = (50, 50)  # Position the mascot in the top-left corner
except:
    mascot_image = None
    mascot_rect = None

try:
    laugh_sound = pygame.mixer.Sound('laugh.mp3')
except:
    laugh_sound = None

# Set custom icon if available
try:
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
except:
    pass  # Use default icon if custom icon is not found

# Center the window on screen
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Font
try:
    # Try to use a font that supports emojis (Segoe UI Emoji is available on Windows)
    font = pygame.font.SysFont('Segoe UI Emoji', 32)
except:
    font = pygame.font.Font(None, 32)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = WHITE if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, PURPLE, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = DARK_GRAY
        self.txt_surface = font.render(text, True, WHITE)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)

def run_viewer_bot(proxy_choice, channel_name, viewer_count, repeat=False):
    proxy_servers = {
        1: "https://www.blockaway.net",
        2: "https://www.croxyproxy.com",
        3: "https://www.croxyproxy.rocks",
        4: "https://www.croxy.network",
        5: "https://www.croxy.org",
        6: "https://www.youtubeunblocked.live",
        7: "https://www.croxyproxy.net",
    }
    
    proxy_url = proxy_servers.get(int(proxy_choice))
    if not proxy_url:
        return

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Add adblock extension
    extension_path = 'adblock.crx'
    chrome_options.add_extension(extension_path)
    
    while True:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(proxy_url)

        for i in range(int(viewer_count)):
            driver.execute_script("window.open('" + proxy_url + "')")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(proxy_url)

            text_box = driver.find_element(By.ID, 'url')
            text_box.send_keys(f'www.twitch.tv/{channel_name}')
            text_box.send_keys(Keys.RETURN)

        if not repeat:
            break
        
        # Wait for 1 hour before refreshing viewers if in repeat mode
        pygame.time.wait(3600000)  # 1 hour in milliseconds
        driver.quit()

def main():
    # Create input boxes with updated positions
    proxy_box = InputBox(INPUT_LEFT_MARGIN, VERTICAL_SPACING, INPUT_WIDTH, INPUT_HEIGHT)
    channel_box = InputBox(INPUT_LEFT_MARGIN, VERTICAL_SPACING * 2, INPUT_WIDTH, INPUT_HEIGHT)
    viewer_box = InputBox(INPUT_LEFT_MARGIN, VERTICAL_SPACING * 3, INPUT_WIDTH, INPUT_HEIGHT)
    
    # Create buttons with centered positions
    button_y = VERTICAL_SPACING * 4
    run_once_btn = Button(
        (WINDOW_WIDTH - (BUTTON_WIDTH * 2 + BUTTON_SPACING)) // 2,
        button_y,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Run Once"
    )
    run_repeat_btn = Button(
        (WINDOW_WIDTH - (BUTTON_WIDTH * 2 + BUTTON_SPACING)) // 2 + BUTTON_WIDTH + BUTTON_SPACING,
        button_y,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Run Repeat"
    )
    
    # Load mascot image
    try:
        mascot = pygame.image.load('mascot.png')
        # Scale the image to fit nicely at the bottom (adjust size as needed)
        mascot = pygame.transform.scale(mascot, (200, 200))
        mascot_rect = mascot.get_rect(centerx=WINDOW_WIDTH // 2, bottom=WINDOW_HEIGHT - 20)
    except:
        mascot = None
    
    # Labels with updated positions
    labels = [
        ("Proxy (1-7):", (LABEL_LEFT_MARGIN, VERTICAL_SPACING + INPUT_HEIGHT//2 - 10)),
        ("Channel Name:", (LABEL_LEFT_MARGIN, VERTICAL_SPACING * 2 + INPUT_HEIGHT//2 - 10)),
        ("Viewer Count:", (LABEL_LEFT_MARGIN, VERTICAL_SPACING * 3 + INPUT_HEIGHT//2 - 10))
    ]
    
    # Add title
    title = font.render("🇨🇿 FROM CZECHOSLOVAKIA WITH LOVE! 🇸🇰", True, WHITE)
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, VERTICAL_SPACING // 2))
    
    bot_thread = None
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                if bot_thread and bot_thread.is_alive():
                    sys.exit()
            
            # Handle mascot click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mascot_rect and mascot_rect.collidepoint(event.pos):
                    if laugh_sound:
                        laugh_sound.play()
            
            proxy_box.handle_event(event)
            channel_box.handle_event(event)
            viewer_box.handle_event(event)
            
            if run_once_btn.handle_event(event):
                if not bot_thread or not bot_thread.is_alive():
                    bot_thread = threading.Thread(
                        target=run_viewer_bot,
                        args=(proxy_box.text, channel_box.text, viewer_box.text, False)
                    )
                    bot_thread.start()
            
            if run_repeat_btn.handle_event(event):
                if not bot_thread or not bot_thread.is_alive():
                    bot_thread = threading.Thread(
                        target=run_viewer_bot,
                        args=(proxy_box.text, channel_box.text, viewer_box.text, True)
                    )
                    bot_thread.start()
        
        screen.fill(PURPLE)
        
        # Draw title
        screen.blit(title, title_rect)
        
        # Draw labels
        for text, pos in labels:
            label = font.render(text, True, WHITE)
            screen.blit(label, pos)
        
        # Draw input boxes
        proxy_box.draw(screen)
        channel_box.draw(screen)
        viewer_box.draw(screen)
        
        # Draw buttons
        run_once_btn.draw(screen)
        run_repeat_btn.draw(screen)
        
        # Draw mascot if loaded successfully
        if mascot:
            screen.blit(mascot, mascot_rect)
        
        # Draw mascot image
        if mascot_image:
            screen.blit(mascot_image, mascot_rect)
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()