import read_captured_images
import generate_hashed_images
import time
import os
import pygame
import sys

def main():
    image_paths, expected_texts = generate_hashed_images.generate_qr_codes(
        '/tmp/watermark_noise', 16)

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("QR Code Display")

    running = True
    current_image = 0
    last_update = time.time()
    display_duration = 1  # Display each image for 1 second

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        current_time = time.time()
        if current_time - last_update >= display_duration:
            if current_image < len(image_paths):
                display_image_pygame(screen, image_paths[current_image])
                current_image += 1
                last_update = current_time
            else:
                running = False

        pygame.display.flip()
        pygame.time.wait(10)  # Small delay to reduce CPU usage

    pygame.quit()
    sys.exit()

def display_image_pygame(screen, image_path: str) -> None:
    print(f'Displaying {image_path}')
    screen.fill((0, 0, 0))  # Fill screen with black
    
    image = pygame.image.load(image_path)
    image_width, image_height = image.get_size()
    screen_width, screen_height = screen.get_size()
    
    # Calculate scaling factor to fit image within screen
    scale = min(screen_width / image_width, screen_height / image_height)
    
    # Calculate new dimensions
    new_width = int(image_width * scale)
    new_height = int(image_height * scale)
    
    # Scale image
    image = pygame.transform.scale(image, (new_width, new_height))
    
    # Calculate position to center image
    x = (screen_width - new_width) // 2
    y = (screen_height - new_height) // 2
    
    # Blit image onto screen
    screen.blit(image, (x, y))

def capture_image(image_save_path: str) -> None:
    print(f'Capturing camera image; saving to {image_save_path}')
    # Capture image from camera
    os.system('libcamera-vid -t 100 -o /tmp/video_capture.mp4')
    # Extract a single frame from the video and save it as a PNG image
    os.system(f'ffmpeg -i /tmp/video_capture.mp4 -vframes 1 {image_save_path}')

if __name__ == "__main__":
    main()