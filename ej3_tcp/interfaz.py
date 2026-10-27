"""
Ejercicio 3 — Interfaz de comunicación confiable sobre TCP.

TCP ya garantiza entrega ordenada y sin pérdidas. Esta capa agrega
delimitación de mensajes (framing) para que send/recv trabajen con
mensajes completos y no con un flujo de bytes cortado al medio.

Formato en el cable:  4 bytes big-endian con la longitud + payload UTF-8.
"""

import socket
import struct

_HEADER = struct.Struct("!I")
_MAX = 1024 * 1024


class CanalTCP:
    def __init__(self, sock: socket.socket):
        self._sock = sock

    def enviar(self, texto: str) -> None:
        payload = texto.encode("utf-8")
        self._sock.sendall(_HEADER.pack(len(payload)) + payload)

    def recibir(self) -> str | None:
        header = self._leer_exacto(_HEADER.size)
        if header is None:
            return None
        (n,) = _HEADER.unpack(header)
        if n > _MAX:
            raise ValueError(f"Mensaje demasiado grande: {n} bytes")
        payload = self._leer_exacto(n)
        if payload is None:
            raise ConnectionError("Conexión cerrada a mitad de un mensaje")
        return payload.decode("utf-8")

    def cerrar(self) -> None:
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self._sock.close()

    def _leer_exacto(self, n: int) -> bytes | None:
        buf = bytearray()
        while len(buf) < n:
            chunk = self._sock.recv(n - len(buf))
            if not chunk:
                return None if not buf else bytes(buf)
            buf.extend(chunk)
        return bytes(buf)


def conectar(host: str, puerto: int) -> CanalTCP:
    sock = socket.create_connection((host, puerto))
    return CanalTCP(sock)


def aceptar(host: str, puerto: int) -> tuple[CanalTCP, tuple]:
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host, puerto))
    listener.listen(1)
    print(f"[TCP] Esperando conexión en {host}:{puerto}...", flush=True)
    conn, addr = listener.accept()
    listener.close()
    print(f"[TCP] Conectado desde {addr[0]}:{addr[1]}", flush=True)
    return CanalTCP(conn), addr
