import pygame
import sys
import engine
# Initialize Pygame
pygame.init()

# Set up display
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chart Editor")

# Set frame rate
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define note attributes
NOTE_WIDTH, NOTE_HEIGHT = 20, 20
note_color = RED

# Initialize empty list to store notes
notes = []

# Load song
song_file = f'{engine.Song_name}.ogg'
pygame.mixer.music.load(song_file)
pygame.mixer.music.play(-1)  # Play the song indefinitely

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Add a note at the current position
                current_time = pygame.time.get_ticks()
                notes.append(current_time)
            elif event.key == pygame.K_LEFT:
                # Move selected note left
                pass
            elif event.key == pygame.K_RIGHT:
                # Move selected note right
                pass
            elif event.key == pygame.K_DELETE:
                # Delete selected note
                pass

    # Clear the screen
    screen.fill(WHITE)

    # Draw the timeline
    pygame.draw.line(screen, BLACK, (0, WINDOW_HEIGHT // 2), (WINDOW_WIDTH, WINDOW_HEIGHT // 2))

    # Draw notes
    for note in notes:
        pygame.draw.rect(screen, note_color, (note - NOTE_WIDTH // 2, WINDOW_HEIGHT // 2 - NOTE_HEIGHT // 2, NOTE_WIDTH, NOTE_HEIGHT))

    # Display notes count
    font = pygame.font.Font(None, 24)
    notes_count_text = font.render(f"Notes Placed: {len(notes)}", True, BLACK)
    screen.blit(notes_count_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Save notes data
with open('chart_data.json', 'w') as file:
    for note in notes:
        file.write(f"{note}\n")

# Stop the song and quit Pygame
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
