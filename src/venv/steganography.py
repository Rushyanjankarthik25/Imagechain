import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import upload_to_ipfs  # Import upload_to_ipfs from blockchain.py

def messageToBinary(message):
    """Convert a message (string, bytes, or integer) to its binary representation."""
    if isinstance(message, str):
        return ''.join(format(ord(i), "08b") for i in message)
    elif isinstance(message, (bytes, np.ndarray)):
        return [format(i, "08b") for i in message]
    elif isinstance(message, (int, np.uint8)):
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported")

def hideData(image, secret_message):
    """Hide a secret message in the image using LSB steganography."""
    # Calculate maximum bytes that can be encoded
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("Maximum bytes to encode:", n_bytes)

    # Check if the message is too large for the image
    if len(secret_message) > n_bytes:
        raise ValueError("Insufficient bytes in the image to encode the message. Use a larger image or shorter message.")

    # Add a delimiter to mark the end of the message
    delimiter = "#####"
    secret_message += delimiter

    # Convert the message to binary
    binary_secret_msg = messageToBinary(secret_message)
    data_len = len(binary_secret_msg)
    data_index = 0

    # Iterate through the image pixels
    for row in image:
        for pixel in row:
            r, g, b = messageToBinary(pixel)
            if data_index < data_len:
                pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index >= data_len:
                break
        if data_index >= data_len:
            break

    return image

def showData(image):
    """Efficiently extract the hidden message from the image."""
    binary_data = []
    delimiter = "#####"
    delimiter_binary = ''.join(format(ord(i), "08b") for i in delimiter)
    
    try:
        # Iterate through the image pixels using NumPy for faster processing
        for row in image:
            for pixel in row:
                r, g, b = pixel[:3]
                
                # Append the LSB of each channel to binary_data
                binary_data.append(format(r, "08b")[-1])
                binary_data.append(format(g, "08b")[-1])
                binary_data.append(format(b, "08b")[-1])
                
                # Check if the delimiter exists in the last few extracted bits
                if len(binary_data) >= len(delimiter_binary) * 8:
                    current_message = "".join(binary_data)
                    if delimiter_binary in current_message:
                        break
            else:
                continue
            break

        # Convert binary data to text
        binary_string = "".join(binary_data)
        all_bytes = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
        decoded_data = "".join(chr(int(byte, 2)) for byte in all_bytes)

        return decoded_data.split(delimiter)[0]  # Remove the delimiter and return the message

    except Exception as e:
        print(f"Error during decoding: {e}")
        return None


def encode_and_upload():
    """Encode a message into an image and upload it to IPFS."""
    image_name = input("Enter image name (with extension): ")
    try:
        # Read the image
        image = cv2.imread(image_name)
        if image is None:
            raise FileNotFoundError(f"Image file not found or unsupported format: {image_name}")

        # Display the original image
        print("The shape of the image is:", image.shape)
        print("The original image is as shown below:")
        resized_image = cv2.resize(image, (500, 500))
        plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

        # Get the message to encode
        data = input("Enter data to be encoded: ")
        if not data:
            raise ValueError("Data cannot be empty.")

        # Save the encoded image
        filename = input("Enter the name of the new encoded image (with extension): ")
        encoded_image = hideData(image, data)
        cv2.imwrite(filename, encoded_image)
        print(f"Message encoded successfully. Saved as {filename}")

        # Upload the encoded image to IPFS
        ipfs_hash = upload_to_ipfs(filename)
        if ipfs_hash:
            print(f"Image uploaded to IPFS with hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print("Failed to upload image to IPFS")
            return None

    except Exception as e:
        print(f"Error during encoding or uploading: {e}")
        return None