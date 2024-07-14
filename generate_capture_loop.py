import read_captured_images
import generate_hashed_images
import time


def main():
  image_paths, expected_texts = generate_hashed_images.generate_qr_codes('/tmp/watermark_noise', 16)
  
  for i, image_path in image_paths:
    # Display image_path
    # How?
    print(f'Displaying {image_path}')
    # Sleep to ensure image is displayed
    time.sleep(1)
    
    # Read image from camera
    # How?
    image = None # capture this from camera
    save_path = f'/tmp/captured_images/camera_image_{i}.png
    f = open(save_path, 'wb')
    f.write(image)
    print('Capturing camera image; saving to {save_path}')
    f.close()
    
    # Validate captured image
    match = read_captured_images.validate_image(save_path, expected_texts[i])
    print(f'Captured image {i} matches?: {match}')
  

if __name__ == "__main__":
  main()