import cv2
import os
import numpy as np

def encode_message(image_path, message, password, output_path="encryptedImage.png"):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found!")
        return
    
    rows, cols, _ = img.shape
    max_length = (rows * cols * 3) // 8 
    
    if len(message) > max_length:
        print("Error: Message too long for this image!")
        return
    
    message += "|||" 
    encoded_msg = ''.join(format(ord(char), '08b') for char in message)
    
    idx = 0
    for i in range(rows):
        for j in range(cols):
            for k in range(3):
                if idx < len(encoded_msg):
                    img[i, j, k] = (img[i, j, k] & 0b11111110) | int(encoded_msg[idx])
                    idx += 1
    
    cv2.imwrite(output_path, img)
    print(f"Message encoded successfully in {output_path}")
    os.system(f"start {output_path}")

def decode_message(image_path, password):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found!")
        return
    
    binary_data = ""
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                binary_data += str(img[i, j, k] & 1)
    
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = "".join([chr(int(char, 2)) for char in chars])
    message = message.split("|||")[0]
    
    print("Decrypted Message:", message)

image_file = "D:/New folder/pyhton/mypic.jpg" 
secret_message = input("Enter secret message: ")
passcode = input("Enter passcode: ")
encode_message(image_file, secret_message, passcode)

decode_passcode = input("Enter passcode for decryption: ")
if decode_passcode == passcode:
    decode_message("encryptedImage.png", passcode)
else:
    print("Authentication failed! Access denied.")
