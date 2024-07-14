from qreader import QReader
import cv2


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


def validate_image(image_path: str, expected_text: str) -> bool:
  try:
    read_captured_image(image_path)
  except:
    return False
  return read_captured_image(image_path) == expected_text
