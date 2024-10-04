import socket
import cv2
import numpy as np

# Client setup
# HOST = 'your-windows-ip'  # Replace with your actual Windows IP
HOST = '192.168.143.200'  # Replace with your actual Windows IP
PORT = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

try:
    while True:
        # Receive the length of the image
        img_size = int.from_bytes(client_socket.recv(4), 'big')

        # Receive the image data
        img_data = b""
        while len(img_data) < img_size:
            packet = client_socket.recv(4096)
            if not packet:
                print("Connection closed by the server.")
                break
            img_data += packet

        if not img_data:
            break  # Exit if no data received

        # Convert the received bytes into an image
        img_array = np.asarray(bytearray(img_data), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Display the image using OpenCV
        cv2.imshow('Screen Mirror', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    client_socket.close()
    cv2.destroyAllWindows()
