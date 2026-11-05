# Problema AF - Registro de eventos de red
# Solucion en streaming: O(N) tiempo, O(U_max) memoria con arrays compactos.
#
# Reglas (descubiertas con la caja negra, ver documentacion):
#  - Se leen exactamente N lineas (o hasta EOF). Una linea vacia consume una.
#  - Linea valida: "ts usuario accion" con exactamente un espacio entre tokens,
#    sin espacios extra; ts y usuario solo digitos ASCII de longitud 1..12;
#    accion in {LOGIN, READ, WRITE, LOGOUT}; se tolera un unico '\r' final.
#  - usuario < 2_000_000 ; T1 <= ts <= T2 (inclusivo). Lo demas se ignora sin
#    tocar el estado del usuario.
#  - Duplicado: misma (ts, usuario, accion) que el ultimo evento contabilizado
#    del mismo usuario -> se ignora.
#  - Brecha g = ts - last_ts; se acumula solo si g <= G. El evento cuenta
#    siempre y actualiza last_ts.
#  - Promedio = suma/gcnt redondeado half-up sobre el valor exacto, 3 decimales.
#  - Salida: top 5 por conteo desc, id asc. Sin eventos: SIN DATOS.
import sys
from array import array
 
UMAX = 2_000_000
ACTIONS = {b"LOGIN": 1, b"READ": 2, b"WRITE": 3, b"LOGOUT": 4}
 
 
def _read_header(stdin):
    hdr = stdin.readline()
    while hdr and not hdr.strip():
        hdr = stdin.readline()
    p = hdr.split()
    if len(p) < 3:
        return None
    T1, T2, G = int(p[0]), int(p[1]), int(p[2])
    nl = stdin.readline()
    while nl and not nl.strip():
        nl = stdin.readline()
    N = int(nl.strip()) if nl.strip() else 0
    return T1, T2, G, N
 
 
def main():
    stdin = sys.stdin.buffer
    hdr = _read_header(stdin)
    if hdr is None:
        sys.stdout.write("SIN DATOS\n")
        return
    T1, T2, G, N = hdr
 
    # int32 basta si todo ts contabilizado cabe (ts <= T2); si no, int64.
    code = "i" if (-2147483648 <= T1 and T2 <= 2147483647) else "q"
    cnt = array("i", [0]) * UMAX        # eventos contabilizados      (8 MB)
    last_ts = array(code, [0]) * UMAX   # ultimo ts contabilizado     (8 MB)
    gap_sum = array(code, [0]) * UMAX   # suma de brechas aceptadas   (8 MB)
    gap_cnt = array("i", [0]) * UMAX    # numero de brechas aceptadas (8 MB)
    last_act = bytearray(UMAX)          # ultima accion (1..4)        (2 MB)
    actions = ACTIONS
    umax = -1
 
    readline = stdin.readline
    remaining = N
    while remaining > 0:
        line = readline()
        if not line:
            break
        remaining -= 1
        # quitar '\n' y, opcionalmente, un unico '\r'
        if line[-1] == 10:
            line = line[:-2] if (len(line) >= 2 and line[-2] == 13) else line[:-1]
        parts = line.split(b" ")
        if len(parts) != 3:
            continue
        a, b, c = parts
        act = actions.get(c)
        if act is None or not a.isdigit() or not b.isdigit() \
                or len(a) > 12 or len(b) > 12:
            continue
        u = int(b)
        if u >= UMAX:
            continue
        t = int(a)
        if t < T1 or t > T2:
            continue
        if cnt[u]:
            lt = last_ts[u]
            if lt == t and last_act[u] == act:
                continue  # duplicado
            g = t - lt
            if g <= G:
                gap_sum[u] += g
                gap_cnt[u] += 1
            cnt[u] += 1
        else:
            cnt[u] = 1
            if u > umax:
                umax = u
        last_ts[u] = t
        last_act[u] = act
 
    # Top 5: barrido ascendente; con '>' estricto los empates quedan en el id menor.
    top = []  # lista de (cnt, u) ordenada desc por cnt, asc por u
    fifth = 0
    for u in range(umax + 1):
        c = cnt[u]
        if c > fifth:
            i = len(top)
            while i > 0 and top[i - 1][0] < c:
                i -= 1
            top.insert(i, (c, u))
            if len(top) > 5:
                top.pop()
            if len(top) == 5:
                fifth = top[4][0]
 
    if not top:
        sys.stdout.write("SIN DATOS\n")
        return
    out = []
    for c, u in top:
        k = gap_cnt[u]
        if k == 0:
            out.append("%d %d NA" % (u, c))
        else:
            s = gap_sum[u]
            num = 2000 * s + k
            den = 2 * k
            # q = trunc(num/den) (division entera estilo C, hacia cero).
            # Para s >= 0 es exactamente half-up a milesimas.
            q = num // den if num >= 0 else -((-num) // den)
            ip = q // 1000 if q >= 0 else -((-q) // 1000)
            fp = q - ip * 1000
            out.append("%d %d %d.%03d" % (u, c, ip, fp))
    sys.stdout.write("\n".join(out) + "\n")
 
 
if __name__ == "__main__":
    main()