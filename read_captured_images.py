# from qreader import QReader
import cv2
import numpy as np
from PIL import Image

def read_captured_image(image_path: str) -> str:
  # Create a QReader instance
  qreader = QReader()

  # Get the image that contains the QR code
  image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

  # Use the detect_and_decode function to get the decoded QR data
  decoded_text = qreader.detect_and_decode(image=image)

  # Check if the QR code was successfully decoded
  if decoded_text is None:
    raise ValueError("QR code not found in the image")

  return decoded_text


def validate_image_qr(image_path: str, expected_text: str) -> bool:
  try:
    read_captured_image(image_path)
  except:
    return False
  return read_captured_image(image_path) == expected_text

def process_image(image_path):
    # Load image, resize to 256x256, and convert to numpy array
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image = image.resize((256, 256))
    image_array = np.array(image) / 255.0  # Normalize to range (0, 1)
    
    return image_array

def create_patched_image(image_array, patch_size=32):
    # Get the dimensions of the image
    height, width = image_array.shape
    
    # Initialize the result array
    patched_image = np.zeros((height, width))
    
    # Loop over each patch and calculate the average
    for i in range(0, height, patch_size):
        for j in range(0, width, patch_size):
            # Extract the patch
            patch = image_array[i:i+patch_size, j:j+patch_size]
            # Calculate the average of the patch
            patch_avg = np.mean(patch)
            # Assign the average color to the patch in the new image
            patched_image[i:i+patch_size, j:j+patch_size] = patch_avg
    
    return patched_image

def calculate_absolute_relative_difference(image1, image2):
    # Calculate the absolute relative difference
    difference = np.abs(image1 - image2) / np.maximum(image1, image2)
    difference = np.nan_to_num(difference)  # Replace NaNs with 0
    
    return difference

def save_image(image_array, output_path):
    # Convert the numpy array to a PIL image and save it
    output_image = Image.fromarray((image_array * 255).astype(np.uint8))
    output_image.save(output_path)

def validate_image_heatmap(saved_image_path, expected, out_path):
    image = process_image(image_path)
    patched_image = create_patched_image(image)
    difference_image = calculate_absolute_relative_difference(patched_image, expected)
    save_image(difference_image, out_path)

if __name__ == "__main__":
  image_path = 'example_image.png'
  expected_text = 'expected_text'
  image = process_image(image_path)
  patched_image = create_patched_image(image)
  difference_image = calculate_absolute_relative_difference(patched_image, patched_image)
  save_image(difference_image, 'new_path')
  is_match = validate_image(image_path, expected_text)
  print(f'Captured image matches?: {is_match}')
