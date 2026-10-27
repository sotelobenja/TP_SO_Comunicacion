"""
Ejercicio 3 — Servidor TCP con la interfaz confiable.

Uso:
    python servidor.py [puerto]
"""

import sys
from interfaz import aceptar

PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 9100


def main():
    canal, _ = aceptar("0.0.0.0", PUERTO)
    print("Ctrl+C para salir. Los mensajes se contestan con ECO.\n")
    try:
        while True:
            msg = canal.recibir()
            if msg is None:
                print("El cliente cerró la conexión.")
                break
            print(f"cliente> {msg}")
            canal.enviar(f"ECO: {msg}")
    except KeyboardInterrupt:
        print("\nCerrando servidor.")
    finally:
        canal.cerrar()


if __name__ == "__main__":
    main()
