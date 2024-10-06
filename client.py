import socket
import cv2
import pickle
import struct

def client_screen_mirror(host, port=9999):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    data = b""
    payload_size = struct.calcsize("Q")  # Define the size of the packed message length

    while True:
        # Retrieve message size
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)  # Receive 4KB chunks
            if not packet: 
                break
            data += packet
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]

        msg_size = struct.unpack("Q", packed_msg_size)[0]

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize the image data
        frame = pickle.loads(frame_data)

        # Display the image in a window
        cv2.imshow("Mirrored Screen (1280x720)", frame)

        # Exit if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    client_socket.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Replace 'SERVER_IP' with the IP address of the server machine
    client_screen_mirror(host='192.168.4.62', port=9999)
