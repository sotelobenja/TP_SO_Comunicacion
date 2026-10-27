# TP Comunicaciones — Sockets

Implementación de los tres ejercicios con Python (biblioteca estándar `socket`).
Funciona en una sola máquina (`127.0.0.1`) o entre dos PCs de la misma red.

Requisito: Python 3.10 o superior. En Windows, si `python` no está en el PATH, usá `py`.

---

## 1. Datagramas UDP — mensajes de texto

El servidor espera datagramas y responde un eco. El cliente envía texto.

**Terminal 1 (servidor)**

```bash
python ej1_udp/servidor.py 9000
```

**Terminal 2 (cliente)** — en la otra computadora usá la IP del servidor:

```bash
python ej1_udp/cliente.py 127.0.0.1 9000
```

UDP no garantiza entrega: si no hay respuesta en 3 s el cliente lo informa.

---

## 2. Petición-respuesta de 2, 3 y 4 vías

Cada proceso tiene **dos puertos**: uno para recibir y otro para enviar.

| Proceso | Puerto RX | Puerto TX |
|---------|-----------|-----------|
| A       | 5100      | 5101      |
| B       | 5200      | 5201      |

Siempre hay que **arrancar B primero**. A inicia la petición.

```bash
# Terminal 1
python ej2_peticion_respuesta/proceso.py B --vias 2

# Terminal 2
python ej2_peticion_respuesta/proceso.py A --vias 2 --host 127.0.0.1 --msg "hola"
```

Cambiá `--vias` a `3` o `4` (el mismo valor en ambos procesos).

Secuencia:

| Vías | A                         | B                         |
|------|---------------------------|---------------------------|
| 2    | REQ →                     | → RES                     |
| 3    | REQ → … → FIN             | → RES                     |
| 4    | REQ → … → FIN             | → ACK → RES               |

---

## 3. Comunicación confiable con TCP

`ej3_tcp/interfaz.py` define `CanalTCP`: envío y recepción de **mensajes completos**
(longitud de 4 bytes + payload). TCP se encarga del orden y de no perder datos;
el framing evita cortar un mensaje a la mitad.

```bash
python ej3_tcp/servidor.py 9100
python ej3_tcp/cliente.py 127.0.0.1 9100
```

---

## Entre dos computadoras

1. Averiguá la IP local (`ipconfig` en Windows, `ip addr` en Linux).
2. Si hay firewall, abrí los puertos UDP/TCP que uses (9000, 5100-5201, 9100).
3. En el cliente / proceso A, pasá `--host` o el primer argumento con esa IP.
