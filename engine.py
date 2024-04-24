import pygame
import json
import sys
import os
import tkinter.simpledialog as tsd

# Initialize Pygame
pygame.init()

def Song_Info():
    Song_name = tsd.askstring("Input", "What song do you want?")
    has_voices = tsd.askstring("Input", "Are there voices? (yes/no)")
    Song_json = tsd.askstring("Input", "What is the JSON file name?")
    return Song_name, has_voices, Song_json

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Render Engine v1")

Song_name, has_voices, Song_json = Song_Info()

# Set frame rate and start time
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

# Initialize counters and flags
notes_hit = 0

# Load sounds
background_music = pygame.mixer.Sound(f'{Song_name}.ogg') if Song_name != 'Chart' else ""
background_music2 = pygame.mixer.Sound(f'{Song_name}.mp3') if has_voices.lower() == 'yes' else None
pygame.mixer.Sound.play(background_music, 0)
pygame.mixer.Sound.play(background_music2, 0) if has_voices.lower() == 'yes' else None


# Initialize font
font = pygame.font.Font(None, 36)
if Song_name == "Chart":
    import Chart_Editor
# Load note data
try:
    with open(f'{Song_json}.json', 'r') as file:
        data = json.load(file)
        notes = data['song']['notes']
except Exception as e:
    print(f"Failed to load or parse JSON: {e}")
    sys.exit()

# Load total notes from Amount.re file
total_notes = 0
amount_file = f'{Song_name}.re'
if os.path.exists(amount_file):
    with open(amount_file, 'r') as f:
        line = f.readline().strip()
        if line.startswith("Amount:"):
            try:
                total_notes = int(line.split(":")[1])
            except ValueError:
                print("Invalid value in Amount.re")
else:
    print(".re file not found.")

# Text surfaces
score_text = font.render(f"Notes Hit: {notes_hit}", True, (255, 255, 255))
total_notes_text = font.render(f"Total Notes: {total_notes}", True, (255, 255, 255))

# Main game loop
running = True
while running:
    current_time = pygame.time.get_ticks() - start_time

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check note timings
    for note_info in notes:
        section_notes = note_info['sectionNotes']
        for note_data in section_notes:
            note_time = note_data[0]
            if abs(note_time - current_time) < 1000:
                key_index = note_data[1]
                if 'hit' not in note_data:
                    notes_hit += 1
                    note_data.append('hit')

    # Clear the screen
    screen.fill((0, 0, 0))

    # Display text
    screen.blit(total_notes_text, (10, 40))
    screen.blit(font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255)), (10, 70))
    screen.blit(font.render(f"Notes Hit: {notes_hit}", True, (255, 255, 255)), (10, 10))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(6000)

# Quit Pygame
pygame.quit()
sys.exit()
