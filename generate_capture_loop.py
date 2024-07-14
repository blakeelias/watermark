import read_captured_images
import generate_hashed_images
import time
import os


def main():
  image_paths, expected_texts = generate_hashed_images.generate_qr_codes(
      '/tmp/watermark_noise', 16)

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
    is_match = read_captured_images.validate_image(save_path,
                                                   expected_texts[i])
    print(f'Captured image {i} matches?: {is_match}')


def display_image(image_path: str) -> None:
  # Display image_path
  print(f'Displaying {image_path}')
  os.system(f'feh {image_path}')


def capture_image(image_save_path: str) -> None:
  print(f'Capturing camera image; saving to {image_save_path}')
  # Capture image from camera
  os.system('libcamera-vid -t 100 -o /tmp/video_capture.mp4')
  # Extract a single frame from the video and save it as a PNG image
  os.system('ffmpeg -i /tmp/video_capture.mp4 -vframes 1 {image_save_path}')


if __name__ == "__main__":
  main()
