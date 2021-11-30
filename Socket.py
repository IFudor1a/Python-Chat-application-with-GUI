import socket


class Socket:
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )