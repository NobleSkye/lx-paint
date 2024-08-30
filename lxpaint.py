import pygame
import sys
import colorsys
import math
import copy

# Initialize Pygame
pygame.init()

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
    undo_stack.append(copy.deepcopy(canvas.get_at((0, 0))))


def restore_from_undo_stack():
    if undo_stack:
        canvas.blit(undo_stack.pop(), (0, 0))


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
                    canvas.blit(undo_stack[-1], (0, 0))  # Restore last canvas state
                    pygame.draw.line(canvas, color, last_pos, (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT), brush_size)
                elif tool == "Rectangle":
                    canvas.blit(undo_stack[-1], (0, 0))  # Restore last canvas state
                    pygame.draw.rect(canvas, color, pygame.Rect(min(last_pos[0], event.pos[0]), min(last_pos[1], event.pos[1] - TOOLBAR_HEIGHT), abs(last_pos[0] - event.pos[0]), abs(last_pos[1] - (event.pos[1] - TOOLBAR_HEIGHT))), brush_size)
                elif tool == "Ellipse":
                    canvas.blit(undo_stack[-1], (0, 0))  # Restore last canvas state
                    pygame.draw.ellipse(canvas, color, pygame.Rect(min(last_pos[0], event.pos[0]), min(last_pos[1], event.pos[1] - TOOLBAR_HEIGHT), abs(last_pos[0] - event.pos[0]), abs(last_pos[1] - (event.pos[1] - TOOLBAR_HEIGHT))), brush_size)
                elif tool == "Fill":
                    # Use a flood fill algorithm for the fill tool
                    start_color = canvas.get_at(last_pos)
                    fill_color = color
                    if start_color != fill_color:
                        stack = [last_pos]
                        while stack:
                            x, y = stack.pop()
                            if canvas.get_at((x, y)) == start_color:
                                canvas.set_at((x, y), fill_color)
                                if x > 0:
                                    stack.append((x - 1, y))
                                if x < WINDOW_WIDTH:
                                    stack.append((x + 1, y))
                                if y > 0:
                                    stack.append((x, y - 1))
                                if y < WINDOW_HEIGHT - TOOLBAR_HEIGHT:
                                    stack.append((x, y + 1))
                elif tool == "Eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT), brush_size)

                last_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                restore_from_undo_stack()  # Undo
            elif event.key == pygame.K_r:
                # Redo (not implemented yet)
                pass
            elif event.key == pygame.K_s:
                # Save the drawing as an image
                pygame.image.save(canvas, "drawing.png")
            elif event.key == pygame.K_UP:
                brush_size = min(100, brush_size + 1)
            elif event.key == pygame.K_DOWN:
                brush_size = max(1, brush_size - 1)
            elif event.key == pygame.K_BACKSPACE:
                # Clear canvas
                canvas.fill(WHITE)
            elif event.key == pygame.K_RETURN:
                if tool == "Text":
                    # Render text on canvas
                    font = pygame.font.Font(None, 36)
                    text_surface = font.render(text_input, True, color)
                    canvas.blit(text_surface, (last_pos[0], last_pos[1] - TOOLBAR_HEIGHT))
                    text_input = ""

    # Blit the canvas and toolbar onto the screen
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))
    screen.blit(toolbar, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
