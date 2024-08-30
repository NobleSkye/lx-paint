import pygame
import sys
import colorsys
import math
import copy
import tkinter as tk
from tkinter import filedialog
from io import BytesIO

# Initialize Pygame and Tkinter
pygame.init()
tk_root = tk.Tk()
tk_root.withdraw()  # Hide the main Tkinter window

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
TOOLBAR_HEIGHT = 50
BRUSH_SIZE = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
TEXT_COLOR = (0, 0, 0)
GRID_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (0, 255, 255), (255, 0, 255),
    (192, 192, 192), (128, 0, 0), (128, 128, 0)
]

# Set up the drawing window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Lx Paint")

# Initialize the canvas
canvas = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# Initialize toolbar
toolbar = pygame.Surface((WINDOW_WIDTH, TOOLBAR_HEIGHT))
toolbar.fill(GRAY)

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

# Call function to draw toolbar
draw_toolbar()

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
    # Save the canvas state as raw pixel data
    undo_stack.append(pygame.image.tostring(canvas, 'RGB'))
    
def restore_from_undo_stack():
    if undo_stack:
        # Get the raw pixel data from the undo stack
        pixel_data = undo_stack.pop()
        # Create a new surface with the same dimensions and fill it with the pixel data
        new_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - TOOLBAR_HEIGHT))
        new_surface.blit(pygame.image.fromstring(pixel_data, (WINDOW_WIDTH, WINDOW_HEIGHT - TOOLBAR_HEIGHT), 'RGB'), (0, 0))
        canvas.blit(new_surface, (0, 0))

def save_canvas_as_image():
    # Open file dialog to choose where to save
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        title="Save As"
    )
    if file_path:
        pygame.image.save(canvas, file_path)

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
            if event.pos[1] < TOOLBAR_HEIGHT:
                if 30 <= event.pos[0] <= 110 and TOOLBAR_HEIGHT // 2 - 40 <= event.pos[1] <= TOOLBAR_HEIGHT // 2 + 40:
                    color = get_color_from_wheel(event.pos)
                    if color is None:
                        color = BLACK
                else:
                    # Check tool buttons
                    tool_names = ["Pencil", "Brush", "Line", "Rectangle", "Ellipse", "Fill", "Text", "Eraser"]
                    button_width, button_height = 80, 30
                    for i, name in enumerate(tool_names):
                        rect = pygame.Rect(300 + (i * (button_width + 10)), 10, button_width, button_height)
                        if rect.collidepoint(event.pos):
                            tool = name
                            break
                    # Check color grid buttons
                    grid_x, grid_y = 150, 10
                    grid_size = 30
                    for i, c in enumerate(GRID_COLORS):
                        rect = pygame.Rect(grid_x + (i % 3) * (grid_size + 10), grid_y + (i // 3) * (grid_size + 10), grid_size, grid_size)
                        if rect.collidepoint(event.pos):
                            color = GRID_COLORS[i]
                            break
            else:
                if tool == "Text":
                    # Start text input mode
                    text_input = ""
                else:
                    save_to_undo_stack()  # Save the current canvas state before drawing
                    drawing = True
                    last_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == "Pencil" or tool == "Brush":
                    pygame.draw.line(canvas, color, last_pos, (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT), brush_size if tool == "Brush" else 1)
                elif tool == "Line":
                    canvas.blit(pygame.image.fromstring(undo_stack[-1], (WINDOW_WIDTH, WINDOW_HEIGHT - TOOLBAR_HEIGHT), 'RGB'), (0, 0))  # Restore last canvas state
                    pygame.draw.line(canvas, color, last_pos, (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT), brush_size)
                elif tool == "Rectangle":
                    canvas.blit(pygame.image.fromstring(undo_stack[-1], (WINDOW_WIDTH, WINDOW_HEIGHT - TOOLBAR_HEIGHT), 'RGB'), (0, 0))  # Restore last canvas state
                    pygame.draw.rect(canvas, color, pygame.Rect(min(last_pos[0], event.pos[0]), min(last_pos[1], event.pos[1] - TOOLBAR_HEIGHT), abs(last_pos[0] - event.pos[0]), abs(last_pos[1] - (event.pos[1] - TOOLBAR_HEIGHT))), brush_size)
                elif tool == "Ellipse":
                    canvas.blit(pygame.image.fromstring(undo_stack[-1], (WINDOW_WIDTH, WINDOW_HEIGHT - TOOLBAR_HEIGHT), 'RGB'), (0, 0))  # Restore last canvas state
                    pygame.draw.ellipse(canvas, color, pygame.Rect(min(last_pos[0], event.pos[0]), min(last_pos[1], event.pos[1] - TOOLBAR_HEIGHT), abs(last_pos[0] - event.pos[0]), abs(last_pos[1] - (event.pos[1] - TOOLBAR_HEIGHT))), brush_size)
                last_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                save_canvas_as_image()
            if event.key == pygame.K_u and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                restore_from_undo_stack()

    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))
    screen.blit(toolbar, (0, 0))
    pygame.display.flip()

pygame.quit()
