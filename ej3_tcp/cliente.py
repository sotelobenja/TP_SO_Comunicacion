"""
Ejercicio 3 — Cliente TCP con la interfaz confiable.

Uso:
    python cliente.py <ip_servidor> [puerto]
"""

import sys
from interfaz import conectar

if len(sys.argv) < 2:
    print("Uso: python cliente.py <ip_servidor> [puerto]")
    sys.exit(1)

HOST = sys.argv[1]
PUERTO = int(sys.argv[2]) if len(sys.argv) > 2 else 9100


def main():
    canal = conectar(HOST, PUERTO)
    print(f"[TCP cliente] Conectado a {HOST}:{PUERTO}")
    print("Escribí un mensaje y Enter. 'salir' para terminar.\n")
    try:
        while True:
            texto = input("> ").strip()
            if not texto:
                continue
            if texto.lower() == "salir":
                break
            canal.enviar(texto)
            respuesta = canal.recibir()
            if respuesta is None:
                print("El servidor cerró la conexión.")
                break
            print(f"servidor> {respuesta}")
    except KeyboardInterrupt:
        print("\nCerrando cliente.")
    finally:
        canal.cerrar()


if __name__ == "__main__":
    main()
