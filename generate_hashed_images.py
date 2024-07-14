import qrcode
from PIL import ImageOps, Image
import os
import time
import hashlib
from typing import List, Tuple
import numpy as np


def generate_qr_codes(image_path: str,
                      num_images: int) -> Tuple[List[str], List[str]]:
    '''
    Create a folder to store the images.
    Returns:
        A list of the image paths.
    '''
    os.makedirs(image_path, exist_ok=True)
    filenames = []
    expected_texts = []

    for i in range(num_images):
        # Get the current timestamp and hash it
        timestamp = str(time.time()).encode('utf-8')
        print(timestamp)
        hashed_timestamp = hashlib.sha256(timestamp).hexdigest()

        # Create the QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(hashed_timestamp)
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")

        # Invert the colors
        inverted_img = ImageOps.invert(img)

        # Save the inverted image
        filename = f"{image_path}/inverted_qr_code_{i+1}.png"
        inverted_img.save(filename)

        filenames.append(filename)
        expected_texts.append(hashed_timestamp)

        print(f"Generated QR code {i+1}/{num_images}")

    return filenames, expected_texts


def generate_checkerboards(
    image_path: str,
    num_images: int,
    checkerboard_dims: Tuple[int, int] = (4, 4)
) -> Tuple[List[str], List[np.array]]:
    '''
    Generate a list of random checkerboard patterns.
    Returns:
        A list of the image paths.
    '''
    os.makedirs(image_path, exist_ok=True)
    filenames = []
    expected_checkerboards = []

    for i in range(num_images):
        # Get the current timestamp and hash it
        timestamp = str(time.time()).encode('utf-8')
        print(timestamp)
        hashed_timestamp = hashlib.sha256(timestamp).hexdigest()
        np.radom.seed(hashed_timestamp)

        # Create random checkerboard pattern using datetime as a seed
        checkerboard = np.random.randint(0, 2, size=checkerboard_dims)

        # Convert checkerboard pattern to an image
        img = Image.fromarray(checkerboard)

        # Save the image
        filename = f"{image_path}/checkerboard_{i+1}.png"
        img.save(filename)

        filenames.append(filename)
        expected_checkerboards.append(checkerboard)

        print(f"Generated QR code {i+1}/{num_images}")

    return filenames, expected_checkerboards


if __name__ == "__main__":
    num_images = 50  # Change this to the desired number of images
    generate_qr_codes(num_images)
    print(f"Generated {num_images} QR codes in the 'images' folder.")
