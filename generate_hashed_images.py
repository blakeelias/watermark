import qrcode
from PIL import ImageOps
import os
import time
import hashlib

def generate_qr_codes(num_images):
    # Create a folder to store the images
    folder_name = "images"
    os.makedirs(folder_name, exist_ok=True)

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
        filename = f"{folder_name}/inverted_qr_code_{i+1}.png"
        inverted_img.save(filename)

        print(f"Generated QR code {i+1}/{num_images}")

if __name__ == "__main__":
    num_images = 50  # Change this to the desired number of images
    generate_qr_codes(num_images)
    print(f"Generated {num_images} QR codes in the 'images' folder.")