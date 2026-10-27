"""
Ejercicio 2 — Proceso A o B.

Uso (en dos terminales, mismo o distinto host):
    python proceso.py B --vias 2
    python proceso.py A --vias 2 --host 127.0.0.1 --msg "hola"

Roles:
    A  inicia la petición
    B  espera y responde

--vias  2 | 3 | 4
"""

import argparse
from protocolo import ejecutar_iniciador, ejecutar_servidor


def main():
    parser = argparse.ArgumentParser(description="Protocolo petición-respuesta")
    parser.add_argument("rol", choices=["A", "B"])
    parser.add_argument("--vias", type=int, choices=[2, 3, 4], required=True)
    parser.add_argument("--host", default="127.0.0.1", help="IP del otro proceso")
    parser.add_argument("--msg", default="ping", help="Carga de la petición (rol A)")
    args = parser.parse_args()

    if args.rol == "A":
        ejecutar_iniciador(args.rol, args.vias, args.host, args.msg)
    else:
        ejecutar_servidor(args.rol, args.vias)


if __name__ == "__main__":
    main()
