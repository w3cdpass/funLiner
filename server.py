import socket
import cv2
import numpy as np
import mss
import pickle
import struct

def server_screen_mirror(host='0.0.0.0', port=9999):
    # Get full screen dimensions
    with mss.mss() as sct:
        screen_info = sct.monitors[1]  # Monitor 1 (primary monitor)
        full_screen = {
            "top": screen_info["top"],
            "left": screen_info["left"],
            "width": screen_info["width"],
            "height": screen_info["height"]
        }

        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print("Waiting for a connection...")

        # Accept a client connection
        conn, addr = server_socket.accept()
        print(f"Connected to {addr}")

        while True:
            # Capture the entire screen
            img = sct.grab(full_screen)

            # Convert the captured image to a NumPy array
            img_np = np.array(img)

            # Convert BGRA to BGR (OpenCV uses BGR format)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

            # Resize the image to 1280x720 resolution for HD display
            img_resized = cv2.resize(img_bgr, (1280, 720))

            # Serialize the resized image data
            data = pickle.dumps(img_resized)

            # Send message size first, then the data
            message_size = struct.pack("Q", len(data))  # Pack data length as unsigned long long
            conn.sendall(message_size + data)  # Send message size followed by actual data

            # Exit if the user presses the 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Clean up
    conn.close()
    server_socket.close()

if __name__ == "__main__":
    server_screen_mirror()
