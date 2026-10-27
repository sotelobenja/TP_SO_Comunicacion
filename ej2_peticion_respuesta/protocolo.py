"""
Ejercicio 2 — Protocolos petición-respuesta de 2, 3 y 4 vías.

Cada proceso usa dos sockets UDP distintos:
  - uno para RECIBIR (bind en puerto_rx)
  - uno para ENVIAR   (bind en puerto_tx)

Proceso A: rx=5100  tx=5101
Proceso B: rx=5200  tx=5201

A envía hacia el puerto_rx de B, y B hacia el puerto_rx de A.

Mensajes: TIPO|id|carga
  REQ  petición
  ACK  acuse de recibo de la petición
  RES  respuesta
  FIN  acuse de recibo de la respuesta (cierre de la transacción)
"""

import socket
from dataclasses import dataclass

BUFFER = 4096
TIMEOUT = 5.0

PUERTOS = {
    "A": {"rx": 5100, "tx": 5101},
    "B": {"rx": 5200, "tx": 5201},
}


@dataclass
class Mensaje:
    tipo: str
    id: str
    carga: str

    def serializar(self) -> bytes:
        return f"{self.tipo}|{self.id}|{self.carga}".encode("utf-8")

    @staticmethod
    def parsear(datos: bytes) -> "Mensaje":
        texto = datos.decode("utf-8", errors="replace")
        partes = texto.split("|", 2)
        if len(partes) != 3:
            raise ValueError(f"Mensaje inválido: {texto!r}")
        return Mensaje(partes[0], partes[1], partes[2])


def crear_sockets(rol: str):
    cfg = PUERTOS[rol]
    rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rx.bind(("0.0.0.0", cfg["rx"]))
    tx.bind(("0.0.0.0", cfg["tx"]))
    rx.settimeout(TIMEOUT)
    tx.settimeout(TIMEOUT)
    return rx, tx


def destino_del_par(rol: str, host: str) -> tuple[str, int]:
    otro = "B" if rol == "A" else "A"
    return host, PUERTOS[otro]["rx"]


def enviar(tx: socket.socket, msg: Mensaje, destino: tuple[str, int]) -> None:
    tx.sendto(msg.serializar(), destino)
    print(f"  -> {msg.tipo} id={msg.id}  '{msg.carga}'  a {destino}", flush=True)


def recibir(rx: socket.socket, esperado: str | None = None) -> tuple[Mensaje, tuple]:
    datos, origen = rx.recvfrom(BUFFER)
    msg = Mensaje.parsear(datos)
    print(f"  <- {msg.tipo} id={msg.id}  '{msg.carga}'  de {origen}", flush=True)
    if esperado and msg.tipo != esperado:
        raise RuntimeError(f"Se esperaba {esperado}, llegó {msg.tipo}")
    return msg, origen


def ejecutar_iniciador(rol: str, vias: int, host_par: str, carga: str) -> None:
    """El iniciador envía la petición (rol A en la demo)."""
    rx, tx = crear_sockets(rol)
    destino = destino_del_par(rol, host_par)
    transaccion = "1"
    print(f"\n[{rol}] Iniciador — protocolo de {vias} vías", flush=True)
    print(f"    rx={PUERTOS[rol]['rx']}  tx={PUERTOS[rol]['tx']}  par={destino}\n", flush=True)

    try:
        enviar(tx, Mensaje("REQ", transaccion, carga), destino)

        if vias == 2:
            recibir(rx, "RES")
        elif vias == 3:
            recibir(rx, "RES")
            enviar(tx, Mensaje("FIN", transaccion, "ok"), destino)
        elif vias == 4:
            recibir(rx, "ACK")
            recibir(rx, "RES")
            enviar(tx, Mensaje("FIN", transaccion, "ok"), destino)
        else:
            raise ValueError("vias debe ser 2, 3 o 4")

        print(f"\n[{rol}] Transacción de {vias} vías completada.", flush=True)
    finally:
        rx.close()
        tx.close()


def ejecutar_servidor(rol: str, vias: int) -> None:
    """El servidor espera la petición (rol B en la demo)."""
    rx, tx = crear_sockets(rol)
    print(f"\n[{rol}] Servidor — protocolo de {vias} vías", flush=True)
    print(f"    rx={PUERTOS[rol]['rx']}  tx={PUERTOS[rol]['tx']}", flush=True)
    print("Esperando petición...\n", flush=True)

    try:
        rx.settimeout(None)
        req, origen = recibir(rx, "REQ")
        rx.settimeout(TIMEOUT)
        host_par = origen[0]
        destino = destino_del_par(rol, host_par)
        respuesta = f"recibido:{req.carga}"

        if vias == 2:
            enviar(tx, Mensaje("RES", req.id, respuesta), destino)
        elif vias == 3:
            enviar(tx, Mensaje("RES", req.id, respuesta), destino)
            recibir(rx, "FIN")
        elif vias == 4:
            enviar(tx, Mensaje("ACK", req.id, "ack-peticion"), destino)
            enviar(tx, Mensaje("RES", req.id, respuesta), destino)
            recibir(rx, "FIN")
        else:
            raise ValueError("vias debe ser 2, 3 o 4")

        print(f"\n[{rol}] Transacción de {vias} vías completada.", flush=True)
    finally:
        rx.close()
        tx.close()
