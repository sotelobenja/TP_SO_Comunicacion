"""
Ejercicio 1 — Servidor UDP (datagrama).

Escucha mensajes de texto y responde con un eco.
Se puede usar entre dos computadoras indicando la IP del servidor.

Uso:
    python servidor.py [puerto]
"""

import socket
import sys

HOST = "0.0.0.0"
PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 9000
BUFFER = 4096


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PUERTO))
    print(f"[UDP servidor] Escuchando en {HOST}:{PUERTO}", flush=True)
    print("Ctrl+C para salir.\n", flush=True)

    try:
        while True:
            datos, origen = sock.recvfrom(BUFFER)
            texto = datos.decode("utf-8", errors="replace")
            print(f"[{origen[0]}:{origen[1]}] {texto}", flush=True)
            respuesta = f"ECO: {texto}"
            sock.sendto(respuesta.encode("utf-8"), origen)
    except KeyboardInterrupt:
        print("\nCerrando servidor.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
