"""
Ejercicio 1 — Cliente UDP (datagrama).

Envía mensajes de texto a otra computadora y muestra las respuestas.

Uso:
    python cliente.py <ip_servidor> [puerto]
    python cliente.py 127.0.0.1 9000
"""

import socket
import sys

if len(sys.argv) < 2:
    print("Uso: python cliente.py <ip_servidor> [puerto]")
    sys.exit(1)

HOST = sys.argv[1]
PUERTO = int(sys.argv[2]) if len(sys.argv) > 2 else 9000
BUFFER = 4096
TIMEOUT = 3.0


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    print(f"[UDP cliente] Destino {HOST}:{PUERTO}")
    print("Escribí un mensaje y Enter. 'salir' para terminar.\n")

    try:
        while True:
            texto = input("> ").strip()
            if not texto:
                continue
            if texto.lower() == "salir":
                break
            sock.sendto(texto.encode("utf-8"), (HOST, PUERTO))
            try:
                datos, origen = sock.recvfrom(BUFFER)
                print(f"[{origen[0]}:{origen[1]}] {datos.decode('utf-8', errors='replace')}")
            except socket.timeout:
                print("(sin respuesta: el datagrama se pudo haber perdido)")
    except KeyboardInterrupt:
        print("\nCerrando cliente.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
