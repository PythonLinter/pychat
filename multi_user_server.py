import socket
import selectors

HOST = '127.0.0.1'
PORT = 65432

selector = selectors.DefaultSelector()
lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lock_socket.bind((HOST, PORT))
lock_socket.listen()
print('listening on', (HOST, PORT))
lock_socket.setblocking(False)

selector.register(lock_socket, selectors.EVENT_READ, data=None)
while True:
    event = selector.select(timeout=None)
    for key, mask in event:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)

def accept_wrapper(socket):
    connection, address = socket.accept()
    print('accept connection from', address)
    connection.setblocking(False)
    data = types.SimpleNamespace(addr=address, inb=b'', outb=b'')
    event = selectors.EVENT_READ | selectors.EVENT_WRITE

    selector.register(connection, event, data=data)
