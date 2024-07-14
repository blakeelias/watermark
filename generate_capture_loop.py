import read_captured_images
import generate_hashed_images
import time
import os

SSH_USER = "guest"
SSH_HOST = "rpi5.local"


def main():
  image_path = '/tmp/watermark_noise'
  image_paths, expected_texts = generate_hashed_images.generate_qr_codes(
      image_path, 16)
  os.system(f'scp -r {image_path} {SSH_USER}@{SSH_HOST}:{image_path}')

  for i, (image_path,
          expected_text) in enumerate(zip(image_paths, expected_texts)):
    # Display image_path
    display_image(image_path)
    # Sleep to ensure image is displayed
    time.sleep(1)

    # Read image from camera
    # How?
    save_path = f'/tmp/captured_images/camera_image_{i}.png'
    capture_image(save_path)

    # Validate captured image
    # is_match = read_captured_images.validate_image(save_path,
    #                                                expected_texts[i])
    # print(f'Captured image {i} matches?: {is_match}')


def display_image(image_path: str) -> None:
  # Display image_path
  print(f'Displaying {image_path}')
  cmd = f'feh {image_path}'
  os.system(f'ssh {SSH_USER}@{SSH_HOST} {cmd}')


def capture_image(image_save_path: str) -> None:
  print(f'Capturing camera image; saving to {image_save_path}')
  # Capture image from camera
  cmd = 'libcamera-vid -t 100 -o /tmp/video_capture.mp4'
  os.system(f'ssh {SSH_USER}@{SSH_HOST} {cmd}')

  # Extract a single frame from the video and save it as a PNG image
  cmd = f'ffmpeg -i /tmp/video_capture.mp4 -vframes 1 {image_save_path}'
  os.system(f'ssh {SSH_USER}@{SSH_HOST} {cmd}')
  os.system(f'scp {SSH_USER}@{SSH_HOST}:{image_save_path} {image_save_path}')


if __name__ == "__main__":
  main()
