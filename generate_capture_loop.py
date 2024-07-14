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
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption("QR Code Display")

    running = True
    current_image = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_image += 1

        if current_image < len(image_paths):
            display_image_pygame(screen, image_paths[current_image])
        else:
            running = False

        pygame.display.flip()
        pygame.time.wait(100)  # Small delay to reduce CPU usage

    pygame.quit()
    sys.exit()

def display_image_pygame(screen, image_path: str) -> None:
    print(f'Displaying {image_path}')
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (300, 300))
    screen.blit(image, (0, 0))
    pygame.display.flip()

def capture_image(image_save_path: str) -> None:
    print(f'Capturing camera image; saving to {image_save_path}')
    # Capture image from camera
    os.system('libcamera-vid -t 100 -o /tmp/video_capture.mp4')
    # Extract a single frame from the video and save it as a PNG image
    os.system(f'ffmpeg -i /tmp/video_capture.mp4 -vframes 1 {image_save_path}')

if __name__ == "__main__":
    main()