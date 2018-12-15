import socket
import selectors

HOST = '127.0.0.1'
PORT = 65432


selector = selectors.DefaultSelector()

lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lock_socket.bind((HOST,PORT))
lock_socket.listen()
lock_socket.setblocking(False)
selector.register(lock_socket, selectors.EVENT_READ, data=None)

while True:
    events = selector.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            serve_connection(key, mask)

def accept_wrapper(socket):
    connection, address = socket.accept()
    connection.setblocking(False)
    data = types.SimpleNameSpace(address=address, inb='', outb='')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(connection, events, data=data)


