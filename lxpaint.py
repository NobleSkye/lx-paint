import pygame
import sys
import colorsys
import math
import tkinter as tk
from tkinter import filedialog
from io import BytesIO




# Initialize Pygame and Tkinter
pygame.init()
tk_root = tk.Tk()
tk_root.withdraw()  # Hide the main Tkinter window

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
TOOLBAR_HEIGHT = 50
MENU_BAR_HEIGHT = 30
DROP_DOWN_HEIGHT = 90
BRUSH_SIZE = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
TEXT_COLOR = (0, 0, 0)
MENU_COLOR = (200, 200, 200)
DROP_DOWN_COLOR = (220, 220, 220)
GRID_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (0, 255, 255), (255, 0, 255),
    (192, 192, 192), (128, 0, 0), (128, 128, 0)
]

# Set up the drawing window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Lx Paint")

# Load and set the icon
icon = pygame.image.load('icon.ico')
pygame.display.set_icon(icon)

# Initialize the canvas
canvas = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - TOOLBAR_HEIGHT - MENU_BAR_HEIGHT - DROP_DOWN_HEIGHT))
canvas.fill(WHITE)

# Initialize toolbar
toolbar = pygame.Surface((WINDOW_WIDTH, TOOLBAR_HEIGHT))
toolbar.fill(GRAY)

# Initialize menu bar
menu_bar = pygame.Surface((WINDOW_WIDTH, MENU_BAR_HEIGHT))
menu_bar.fill(MENU_COLOR)

# Initialize dropdown menu
drop_down = pygame.Surface((WINDOW_WIDTH, DROP_DOWN_HEIGHT))
drop_down.fill(DROP_DOWN_COLOR)
drop_down_visible = False

# Draw the color wheel
def draw_color_wheel(surface, center, radius):
    for y in range(center[1] - radius, center[1] + radius):
        for x in range(center[0] - radius, center[0] + radius):
            dx, dy = x - center[0], y - center[1]
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < radius:
                angle = math.atan2(dy, dx)
                hue = (angle / (2 * math.pi) + 0.5) % 1
                lightness = distance / radius
                color = colorsys.hls_to_rgb(hue, lightness, 0.5)
                surface.set_at((x, y), tuple(int(c * 255) for c in color))

# Draw toolbar buttons and color grid
def draw_toolbar():
    toolbar.fill(GRAY)
    
    # Draw color wheel
    wheel_center = (70, TOOLBAR_HEIGHT // 2)
    wheel_radius = 40
    draw_color_wheel(toolbar, wheel_center, wheel_radius)
    
    # Draw color grid
    grid_x, grid_y = 150, 10
    grid_size = 30
    for i, color in enumerate(GRID_COLORS):
        rect = pygame.Rect(grid_x + (i % 3) * (grid_size + 10), grid_y + (i // 3) * (grid_size + 10), grid_size, grid_size)
        pygame.draw.rect(toolbar, color, rect)
        pygame.draw.rect(toolbar, BLACK, rect, 1)  # Border for color buttons
    
    # Draw tool buttons
    tool_names = ["Pencil", "Brush", "Line", "Rectangle", "Ellipse", "Fill", "Text", "Eraser"]
    button_width, button_height = 80, 30
    for i, name in enumerate(tool_names):
        pygame.draw.rect(toolbar, WHITE, pygame.Rect(300 + (i * (button_width + 10)), 10, button_width, button_height))
        font = pygame.font.Font(None, 24)
        text = font.render(name, True, TEXT_COLOR)
        toolbar.blit(text, (310 + (i * (button_width + 10)), 15))

# Draw the menu bar
def draw_menu_bar():
    menu_bar.fill(MENU_COLOR)
    
    # Draw menu items
    menu_items = ["File", "Edit", "Insert", "Other"]
    item_width = WINDOW_WIDTH // len(menu_items)
    font = pygame.font.Font(None, 24)
    
    for i, item in enumerate(menu_items):
        rect = pygame.Rect(i * item_width, 0, item_width, MENU_BAR_HEIGHT)
        pygame.draw.rect(menu_bar, GRAY, rect)
        pygame.draw.rect(menu_bar, BLACK, rect, 1)  # Border
        text = font.render(item, True, TEXT_COLOR)
        text_rect = text.get_rect(center=rect.center)
        menu_bar.blit(text, text_rect)

# Draw the dropdown menu
def draw_drop_down():
    drop_down.fill(DROP_DOWN_COLOR)
    
    # Draw dropdown items
    drop_down_items = ["Open File", "Save", "Save As"]
    item_height = DROP_DOWN_HEIGHT // len(drop_down_items)
    font = pygame.font.Font(None, 24)
    
    for i, item in enumerate(drop_down_items):
        rect = pygame.Rect(0, i * item_height, WINDOW_WIDTH, item_height)
        pygame.draw.rect(drop_down, GRAY, rect)
        pygame.draw.rect(drop_down, BLACK, rect, 1)  # Border
        text = font.render(item, True, TEXT_COLOR)
        text_rect = text.get_rect(center=rect.center)
        drop_down.blit(text, text_rect)

# Handle file operations
def save_canvas_as_image():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        title="Save As"
    )
    if file_path:
        pygame.image.save(canvas, file_path)

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        title="Open File"
    )
    if file_path:
        image = pygame.image.load(file_path)
        canvas.blit(image, (0, 0))

# Call functions to draw toolbar, menu bar, and dropdown menu
draw_toolbar()
draw_menu_bar()

# Variables
drawing = False
last_pos = None
color = BLACK
brush_size = BRUSH_SIZE
tool = "Pencil"
text_input = ""
undo_stack = []
redo_stack = []

def save_to_undo_stack():
    undo_stack.append(pygame.image.tostring(canvas, 'RGB'))

def restore_from_undo_stack():
    if undo_stack:
        pixel_data = undo_stack.pop()
        new_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - TOOLBAR_HEIGHT - MENU_BAR_HEIGHT - DROP_DOWN_HEIGHT))
        new_surface.blit(pygame.image.fromstring(pixel_data, (WINDOW_WIDTH, WINDOW_HEIGHT - TOOLBAR_HEIGHT - MENU_BAR_HEIGHT - DROP_DOWN_HEIGHT), 'RGB'), (0, 0))
        canvas.blit(new_surface, (0, 0))

def get_color_from_wheel(pos):
    wheel_center = (70, TOOLBAR_HEIGHT // 2)
    wheel_radius = 40
    dx, dy = pos[0] - wheel_center[0], pos[1] - wheel_center[1]
    distance = math.sqrt(dx * dx + dy * dy)
    if distance <= wheel_radius:
        angle = math.atan2(dy, dx)
        hue = (angle / (2 * math.pi) + 0.5) % 1
        lightness = distance / wheel_radius
        color = colorsys.hls_to_rgb(hue, lightness, 0.5)
        return tuple(int(c * 255) for c in color)
    return None

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < MENU_BAR_HEIGHT:
                item_width = WINDOW_WIDTH // 4
                item_index = event.pos[0] // item_width
                if item_index == 0:
                    drop_down_visible = not drop_down_visible
                # Other menu options can be handled here

            elif drop_down_visible and event.pos[1] >= MENU_BAR_HEIGHT and event.pos[1] < MENU_BAR_HEIGHT + DROP_DOWN_HEIGHT:
                drop_down_item_index = (event.pos[1] - MENU_BAR_HEIGHT) // (DROP_DOWN_HEIGHT // 3)
                if drop_down_item_index == 0:
                    open_file()
                elif drop_down_item_index == 1:
                    save_canvas_as_image()
                drop_down_visible = False

            else:
                if event.pos[1] < TOOLBAR_HEIGHT:
                    # Handle color wheel click
                    color = get_color_from_wheel(event.pos)
                    if color is not None:
                        print(f"Color selected: {color}")
                else:
                    tool_names = ["Pencil", "Brush", "Line", "Rectangle", "Ellipse", "Fill", "Text", "Eraser"]
                    button_width, button_height = 80, 30
                    for i, name in enumerate(tool_names):
                        rect = pygame.Rect(300 + (i * (button_width + 10)), 10, button_width, button_height)
                        if rect.collidepoint(event.pos):
                            tool = name
                            print(f"{tool} selected")
                            break

                    # Handle color grid click
                    grid_x, grid_y = 150, 10
                    grid_size = 30
                    for i, c in enumerate(GRID_COLORS):
                        rect = pygame.Rect(grid_x + (i % 3) * (grid_size + 10), grid_y + (i // 3) * (grid_size + 10), grid_size, grid_size)
                        if rect.collidepoint(event.pos):
                            color = GRID_COLORS[i]
                            print(f"Grid color selected: {color}")
                            break

        # Example for logging brush size changes
        # You can add similar checks for mousewheel up/down if you have those events to change brush size
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                set_brush_size(brush_size + 1)
            elif event.key == pygame.K_DOWN:
                set_brush_size(brush_size - 1)

        # Continue handling other events like drawing, etc.

    # Draw everything
    screen.fill(WHITE)
    screen.blit(canvas, (0, MENU_BAR_HEIGHT + TOOLBAR_HEIGHT + (DROP_DOWN_HEIGHT if drop_down_visible else 0)))
    screen.blit(toolbar, (0, MENU_BAR_HEIGHT + (DROP_DOWN_HEIGHT if drop_down_visible else 0)))
    screen.blit(menu_bar, (0, 0))
    if drop_down_visible:
        draw_drop_down()
        screen.blit(drop_down, (0, MENU_BAR_HEIGHT))
    
    pygame.display.flip()

pygame.quit()
