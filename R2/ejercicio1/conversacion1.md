# Conversación completa — Problema AF: Registro de eventos de red

- Proyecto: *competenciap prompt enginerring*
- Fecha: jueves 5 de noviembre de 2026 (America/Mexico_City)
- Participantes: Usuario (adrgelbop@gmail.com) y Claude
- Entregable final: `solucion.py` (archivo único)

---

## Turno 1 — Usuario (12:31)

> # INSTRUCCIONES MAESTRAS — RESOLUCIÓN DEL PROBLEMA AF (PYTHON)
>
> Actúa como un ingeniero de software especializado en algoritmos, estructuras de datos, ingeniería inversa, análisis de complejidad y optimización de Python para jueces competitivos.
>
> Tu objetivo es desarrollar una solución **correcta, verificable y altamente optimizada en tiempo y memoria** para el problema AF: Registro de eventos de red.
>
> No busco únicamente una solución que funcione con los ejemplos. Necesito una implementación capaz de superar las restricciones máximas del juez y reproducir exactamente el comportamiento de la caja negra.
>
> ### 1. OBJETIVO Y PRIORIDADES DE EVALUACIÓN
> Funcionalidad (50 puntos), Prompting (25 puntos), Puntualidad (25 puntos). Prioriza: exactitud lógica, eficiencia algorítmica, optimización de implementación. No sacrifiques la funcionalidad para conseguir una mejora de rendimiento.
>
> ### 2. ENUNCIADO DEL PROBLEMA
> Registro de hasta 5 millones de eventos de red ordenados cronológicamente, formato `timestamp usuario accion`, acciones LOGIN/READ/WRITE/LOGOUT. Dentro del intervalo inclusivo [T1, T2], por usuario: contar eventos válidos no ignorados y calcular el promedio de brechas entre eventos consecutivos considerando solo las brechas aceptadas. El sistema puede ignorar duplicados, excluir brechas por cortes de sesión (parámetro G) y descartar líneas inválidas. Imprimir los cinco usuarios con mayor cantidad: `usuario cantidad promedio` (tres decimales o NA). Orden: mayor cantidad, luego menor identificador. Sin eventos: `SIN DATOS`.
>
> ### 3. RESTRICCIONES TÉCNICAS
> N ≤ 5,000,000; 0 ≤ timestamp ≤ 10^9; usuario < 2·10^6; eventos ordenados por tiempo; 24 segundos; 64 MB; Python. El archivo de entrada puede alcanzar ~115 MB con solo 64 MB de memoria: procesamiento en streaming y estructuras compactas.
>
> ### 4. EJEMPLOS OFICIALES
> Ejemplo 1 — Entrada:
> ```
> 2 28 20
> 11
> 6 1999999 LOGOUT
> 6 2 LOGIN
> 9 4 LOGIN
> 17 4 LOGIN
> 19 4 LOGIN
> 20 2 READ
> 22 3 WRITE
> 23 4 WRITE
> 27 2 LOGOUT
> 36 1999999 READ
> 36 1999999 READ
> ```
> Salida:
> ```
> 4 4 4.667
> 2 3 10.500
> 3 1 NA
> 1999999 1 NA
> ```
> Ejemplo 2 — Entrada:
> ```
> 8 27 20
> 8
> 7 1999999 LOGOUT
> 7 3 LOGIN
> -12 5 READ
> 11 3 READ
> 15 4 WRITE
> 15 3 WRITE
> 34 3 LOGOUT
> 35 4 WRITE
> ```
> Salida:
> ```
> 3 2 4.000
> 4 1 NA
> ```
>
> ### 5. INGENIERÍA INVERSA
> Investigar con la caja negra: A. Duplicados (qué campos, contra último evento o contra todo el historial). B. Cortes de sesión (> G o ≥ G, dependencia de acciones, reinicio del historial). C. Redondeo (half-up, half-even, truncamiento, valores intermedios). D. Líneas inválidas (negativos, fuera de rango, acción desconocida, campos faltantes/extra, malformadas, fuera de intervalo; efecto sobre el historial).
>
> ### 6. PROTOCOLO OBLIGATORIO DE EXPERIMENTACIÓN
> Experimentos pequeños y controlados con: regla, hipótesis, entrada exacta, salida obtenida, interpretación, regla confirmada/descartada. No inventar resultados. Mantener tabla de conocimiento con estados Pendiente / Hipótesis / Confirmada / Descartada. Corregir explícitamente conclusiones erróneas.
>
> ### 7. DISEÑO DEL ALGORITMO · 8. OPTIMIZACIÓN EXTREMA DE PYTHON · 9. VERIFICACIÓN Y PRUEBAS (fuerza bruta, pruebas funcionales, aleatorias y de rendimiento 100k–5M con varias distribuciones) · 10. REGLAS DE COMUNICACIÓN · 11. ENTREGABLE FINAL (reglas, algoritmo, código, complejidad, verificación, rendimiento, limitaciones).
>
> ### 12. INSTRUCCIÓN INICIAL
> No escribas todavía la solución definitiva. Analiza el enunciado separando reglas conocidas, ambiguas, dificultades algorítmicas y riesgos. Propón el primer conjunto de pruebas pequeñas para la caja negra y espera los resultados reales.

## Turno 1 — Claude

### 1. CONTRATO (lo que se sabe y lo que no)

**1.1 Reglas explícitas / confirmadas por los ejemplos**

| Aspecto | Dato | Fuente |
|---|---|---|
| Línea 1 | `T1 T2 G` (ej1: T1=2, T2=28, G=20) | Deducido de ejemplos; pido confirmación |
| Línea 2 | `N` = número de líneas de evento | Ejemplos |
| Evento | `timestamp usuario accion` | Enunciado |
| Eventos fuera de [T1,T2] no se cuentan | Ej2: user 3 tiene LOGIN en t=7 (<8) y LOGOUT en t=34 (>27) → cantidad 2 | Ejemplo 2 |
| Un usuario sin brecha válida → `NA` | Ej1 users 3 y 1999999 | Ejemplos |
| Orden: cantidad desc, luego id **numérico** asc | Ej1: `3` antes que `1999999` | Ejemplo 1 |
| Si hay <5 usuarios, se imprimen los que hay | Ej1 imprime 4, ej2 imprime 2 | Ejemplos |
| Promedio con 3 decimales | `4.667`, `10.500` | Ejemplos |
| `SIN DATOS` si no hay eventos | Enunciado | Enunciado |

Traza del ejemplo 1 (usuario 4): eventos 9,17,19,23 → brechas 8,2,4 → 14/3 = 4.667 ✔. Usuario 2: 6,20,27 → 14,7 → 10.500 ✔. Ninguna brecha de los ejemplos supera G=20, así que los ejemplos no dicen nada sobre cortes de sesión.

**1.2 Reglas ambiguas (requieren caja negra):** A. Duplicados: ¿clave (ts,user,acción), (ts,user) o solo ts? ¿contra el último evento del usuario, la última línea global o todo el historial? B. Cortes: ¿`> G` o `>= G`? ¿afecta a la cantidad? ¿depende de LOGIN/LOGOUT? ¿reinicia el historial? C. Redondeo: half-up, half-even o truncamiento. D. Líneas inválidas: criterios y si rompen la cadena de brechas. E. Intervalo: inclusividad (ej2 es ambiguo: user 3 da 4.000 tanto si la brecha 7→11 cuenta como si no).

**1.3 Dificultades algorítmicas:** estado por usuario con hasta 2·10⁶ ids; top-5 con desempate numérico; todo es un pase lineal si las reglas no miran más de un evento atrás por usuario.

**1.4 Riesgos:** entrada ~115 MB > 64 MB ⇒ descartado `read().split()`; iterar `sys.stdin.buffer`. Estado por usuario con `array` int32 (`count`, `last_ts`, `gap_sum`, `gap_cnt`) = 32 MB + `bytearray` 2 MB ≈ 34 MB + intérprete ≈ 44 MB. Un dict con 2·10⁶ claves costaría >200 MB. Tiempo estimado 6–12 s (estimación, no medición).

### 2. COMPLEJIDAD OBJETIVO
O(N) tiempo, O(U_max = 2·10⁶) memoria compacta.

### 3. TABLA DE CONOCIMIENTO (inicial)

| Característica | Regla | Estado |
|---|---|---|
| Formato entrada | Deducida de ejemplos | Hipótesis |
| Orden salida | Ej1 | Confirmada |
| <5 usuarios → imprimir los existentes | Ej1, Ej2 | Confirmada |
| Eventos fuera de intervalo no cuentan | Ej2 | Confirmada |
| Inclusividad T1/T2 | — | Pendiente |
| Duplicados | — | Pendiente |
| Cortes de sesión | — | Pendiente |
| Redondeo | — | Pendiente |
| Líneas inválidas | — | Pendiente |

### 4. PRIMER LOTE DE EXPERIMENTOS
Se propusieron E1 (duplicados, 6 hipótesis con predicciones distintas), E2 (umbral y reinicio del corte), E3 (dependencia de la acción), E4 (redondeo con 16 brechas), E5 (líneas inválidas y efecto en historial), E6 (inclusividad del intervalo y efecto de eventos externos), E7 (rangos numéricos). Las entradas exactas y salidas están en el anexo de experimentos.

### 5. Lo que necesito
1. Confirmar que la primera línea es `T1 T2 G` y que se leen exactamente `N` líneas. 2. Ejecutar E1–E7 y pegar la salida exacta.

---

## Turno 2 — Usuario (12:36)

> INSTRUCCIONES DE RESOLUCIÓN — PROBLEMA AF. Entregable obligatorio: UN ÚNICO ARCHIVO PYTHON con lectura, validación, duplicados, historial, cálculo, cortes, top-5, formateo y función principal; ejecutable con `python solucion.py` por stdin/stdout, sin módulos propios ni dependencias. Proceso: analizar reglas explícitas y ambiguas, usar E1–E7 con resultados reales, diferenciar hipótesis de reglas confirmadas, no inventar resultados. Rendimiento: 5,000,000 eventos, 2,000,000 usuarios, 24 s, 64 MB, entrada ~115 MB; O(N) tiempo, O(U) memoria.

## Turno 2 — Claude

**ESTADO: BLOQUEADO A LA ESPERA DE DATOS.** Acepté el entregable (un único `solucion.py`). No pasé al diseño porque ninguna regla ambigua tenía evidencia; implementar obligaría a elegir hipótesis, lo que prohíben las reglas 2 y 10 del protocolo. Reiteré la tabla de conocimiento y pedí: (1) confirmar el formato de cabecera y la lectura de N líneas; (2) las salidas exactas de E1–E7.

---

## Turno 3 — Usuario (12:40)

> *(adjunto: `Ronda2_Avanzada.zip`)*
> 1. Confirmación del formato: Sí. Primera línea `T1 T2 G`, segunda `N`, luego exactamente `N` registros `timestamp usuario accion`.
> 2. Te paso el ejecutable de la caja negra y todos los archivos requeridos y me das la guía de cómo ejecutarlo.

## Turno 3 — Claude (trabajo con herramientas)

**Contenido del zip:** `Ronda2_Avanzada.pdf`, `LEEME_caja_negra.txt`, `AF/enunciado.md`, `AF/ejemplo{1,2}.{in,out}`, `AF/caja_linux` (ELF estático x86-64), `caja_mac_arm`, `caja_mac_intel`, `caja_windows.exe`.

**Guía de uso (del LEEME):**
```
Linux:    chmod +x caja_linux && ./caja_linux < ejemplo1.in
Windows:  caja_windows.exe < ejemplo1.in   (PowerShell: Get-Content ejemplo1.in | .\caja_windows.exe)
Mac ARM:  chmod +x caja_mac_arm && ./caja_mac_arm < ejemplo1.in
Mac Intel: chmod +x caja_mac_intel && ./caja_mac_intel < ejemplo1.in
Si macOS la bloquea: xattr -d com.apple.quarantine caja_mac_arm
```
La caja solo acepta **N ≤ 300** (`ERROR: la caja negra solo acepta N <= 300`).

**Enunciado oficial (`enunciado.md`):** "Transmisiones masivas". Rango [T1, T2] inclusive. Lo que debes descubrir con la caja negra: qué es un duplicado, cuándo una brecha es un corte de sesión, cómo redondea el sistema y qué hace inválida una línea. Límites: N ≤ 5 000 000 (≈116 MB); 0 ≤ timestamp ≤ 10^9; 24 s / 64 MB.

Como el binario Linux corría en mi entorno, ejecuté la caja negra directamente. Los ejemplos oficiales reprodujeron `ejemplo1.out` y `ejemplo2.out` (`diff` vacío).

### Lote 1 (E1–E7) — interpretación
- **E1 → `1 7 5.000` / `2 1 NA`**: coincide solo con H1: duplicado = misma terna `(ts, usuario, acción)` que el **último evento contabilizado del mismo usuario**. Descartadas H1b, H2, H3, H3b, H4. Las brechas de 0 s cuentan.
- **E2 → `6.000`** = (5+10+3)/3: se descarta la brecha **> G** (la igual a G cuenta), sin reinicio, el conteo no cambia, `last_ts` se actualiza.
- **E3 → 4.667**: las acciones no influyen.
- **E4 → `1000.625` / `1000.188`**: corrección de mi aritmética (16010/16 = 1000.625, sin empate). `1000.1875 → .188` descarta truncamiento pero no distingue half-up de half-even.
- **E5**: líneas inválidas (acción desconocida, campo extra, campo faltante) se ignoran sin romper la cadena de brechas.
- **E6**: intervalo inclusivo en ambos extremos; un evento fuera del intervalo no alimenta brechas.
- **E7**: `-5` inválido aunque T1=−100; `1000000001` válido (no hay tope en 10⁹ aparte de T2); usuario `2000000` y `-1` inválidos, `1999999` válido.

### Lote 2 — redondeo (R1, R2a, R2b)
- R1 usuario 1: 1000.0625 → `1000.063` ⇒ descartado `%.3f`/half-even; es half-up. (Usuario 2 mal diseñado: 3×10/80 = 0.375.)
- R2a/R2b: 1000.0375→`.038`, 1000.0625→`.063`, 1000.0875→`.088`, 1000.0125→`.013`, 1000.1875→`.188`, 1000.3125→`.313`, 1000.4375→`.438`. Coinciden con `(2000·suma + n) // (2n)`; el caso 1000.0875 difiere de `%.3f` sobre float (`.087`).

### Lote 3 — robustez (F1–F11)
- **F1**: una línea inválida no se registra como último evento (no genera duplicados).
- **F2** (desordenada) 10,30,20,40 → `4 10.000` = (20−10+20)/3: brecha con signo, aceptada si `≤ G`.
- **F3**: solo sobreviven `05 1 READ` y `12 01 READ` ⇒ ceros iniciales OK; `+6`, `7.0`, `1e1`, `read`, tabulador, doble espacio y espacio final inválidos. **F11**: espacio inicial y `READX` inválidos.
- **F4a/F4b**: se leen como máximo N líneas; si hay menos, se procesa lo que hay.
- **F5a/F5b**: CRLF aceptado.
- **F6a**: desempate numérico ascendente, máximo 5 líneas. **F6b/F6c**: `SIN DATOS`.
- **F7a/F7b**: G=0 → brecha 0 cuenta, 1 no; G=−1 → nada cuenta.
- **F8a**: T1>T2 → `SIN DATOS`. **F8b**: usuario 0 válido; brecha 10⁹ válida.
- **F10**: comparación siempre con el último evento contabilizado.

### Lote 4 — bordes de parseo (H1–H11, sondeos U/TS)
- **H1**: la línea vacía consume una de las N. **H2**: solo se tolera un `\r` final.
- **H3**: usuario `9999999` inválido (límite numérico `< 2·10⁶`). **H4**: duplicados comparados numéricamente (`010` ≡ `10`).
- **H5/H6/H7**: tokens numéricos largos inválidos. Sondeo por longitud (una ejecución por caso): **≤ 12 dígitos** válidos tanto para `ts` como para `usuario`; 13+ inválidos. Con T2 de 12 dígitos, `999999999999` válido y `1000000000000` inválido (13 dígitos).
- **H8**: `N` con espacios alrededor OK. **H9**: sin salto final OK. **H11**: `LOGIN, LOGIN(dup), LOGOUT, LOGIN` a mismo ts → 3 eventos, 0.000.
- `strings` del binario: compilado con GCC 13.3 (Ubuntu 24.04), libstdc++ ⇒ C++.

### Tabla de conocimiento consolidada

| Característica | Regla | Estado |
|---|---|---|
| Formato / N líneas | exactamente N (o EOF); línea vacía consume una | Confirmada |
| Línea válida | un espacio exacto, 3 tokens, dígitos 1–12, acción exacta, un `\r` tolerado | Confirmada |
| Rango usuario | 0 ≤ u < 2 000 000 | Confirmada |
| Rango ts | solo T1 ≤ ts ≤ T2 inclusivo | Confirmada |
| Inválida / fuera de intervalo | se ignora sin alterar estado | Confirmada |
| Duplicado | misma (ts,u,acción) que último contabilizado del usuario | Confirmada |
| Brecha | g = ts − last_ts; acumula si g ≤ G; sin reinicio | Confirmada |
| Acciones | no influyen | Confirmada |
| Promedio | half-up (ver corrección posterior) | Confirmada → luego revisada |
| Salida | ≤5, conteo desc, id asc; SIN DATOS | Confirmada |

### Diseño
Candidatos: (1) dict usuario→estado: ~250 MB, descartado. (2) leer todo y ordenar: O(N log N) y >115 MB, descartado. (3) **streaming + 4 `array('i')` + `bytearray` = 34 MB**, top-5 por barrido ascendente. Elegido. Traza del ejemplo 1 verificada a mano.

### Implementación y verificación
Escribí `solucion.py`, `brute.py` (implementación independiente con dict/listas/Decimal), `stress.py` (casos aleatorios ≤300 líneas con 14 tipos de línea inválida, entradas desordenadas, N≠líneas), `gen_big.py` y `measure.py`.

**Stress — primer mismatch (iteración 8, seed 1):** entrada desordenada con G=−1 produjo promedio negativo; la caja imprimió `1 11 -26.-749` y mi solución `-26.750`. Diagnóstico: la caja calcula `q = trunc(avg·1000 + 0.5)` en aritmética C (−26749.5 → −26749) e imprime `q/1000 "." q%1000`. **Corrección explícita:** el redondeo no es "half-up sobre el valor exacto" como declaré tras R2, sino `trunc(x·1000+0.5)`; mis casos R2 coincidieron numéricamente.

Busqué (k<300, s<2·10⁶) casos donde `s/k·1000`, `s·1000/k` y la fórmula entera exacta difieren: solo `s/k·1000` difiere. **R3** (s=323, k=80, avg 4.0375): caja → `4.038` ⇒ descartado `s/k·1000`. Para el dominio del juez (brechas ≥ 0, suma ≤ 10⁹ ≪ 2⁵³) `trunc(s·1000/k + 0.5)` en double coincide con `(2000s+k)//(2k)`: los empates exactos x.5 son representables y la división IEEE es correctamente redondeada; los no-empates distan ≥ 1/(2k) del .5, mucho más que el ulp. Implementé la fórmula entera con truncamiento hacia cero y formato C para negativos; actualicé `brute.py` igual.

**Resultados:** ejemplos OK; todos los experimentos caja = solución = brute; stress 1500 (seed 1) + 1500 (seed 2) + 700 (seed 3) + 300 (seed 7) = **4000 casos OK**; brute = solución en 300k–1M líneas en 6 distribuciones.

**Memoria:** inicialización `array('i', bytes(8 MB))` creaba un temporal; sustituida por `array('i',[0]) * UMAX`. Pico de 50 MB → 44 MB.

**Rendimiento medido (Python 3.13, RSS pico):**

| Distribución (5M líneas) | Tamaño | Tiempo | Memoria |
|---|---|---|---|
| few (50 usuarios) | 93 MB | 4.69 s | 44.2 MB |
| many (2·10⁶ usuarios) | 117 MB | 6.20 s | 44.2 MB |
| dup | 99 MB | 4.85 s | 44.2 MB |
| invalid (50 %) | 115 MB | 4.01 s | 44.2 MB |
| cuts (G=10) | 117 MB | 5.13 s | 44.3 MB |
| maxstate (todos los ids) | 116 MB | 4.41 s | 44.2 MB |

Escalado: 100k 0.22 s, 500k 0.66 s, 1M 1.18 s, 2M 2.56 s.

**Bordes manuales:** N=1, N=0, T1=T2, T2 > 2³¹ (paso automático a int64). La entrada totalmente vacía lanzaba excepción → corregido a `SIN DATOS`.

### Entregable final (resumen del turno)
1. Reglas definitivas (tabla anterior, con redondeo corregido a `trunc(1000·s/k+0.5)` ≡ half-up exacto para s ≥ 0).
2. Algoritmo: un pase en streaming con arrays compactos indexados por id; invariantes: (1) `cnt[u]>0 ⇔ (last_ts[u], last_act[u])` es el último evento contabilizado; (2) `gap_sum`/`gap_cnt` solo acumulan brechas ≤ G, `gap_cnt ≤ cnt−1`; (3) `top` siempre contiene los 5 mejores por `(−cnt, u)`.
3. Complejidad: O(N + U_max) tiempo; O(U_max) memoria (34 MB + intérprete).
4. Limitaciones: velocidad del CPU del juez desconocida (margen ≈ 4×); baseline del intérprete variable; redondeo de promedios negativos solo reproducido en los casos observados; cabeceras malformadas no exploradas.

Archivos entregados: `solucion.py`, `brute.py`, `stress.py`, `gen_big.py`, `measure.py`.

---

## Turno 4 — Usuario (12:55)

> Bien, ahora la solución es solo un archivo .py, por lo que fusiona las funcionalidades de cada uno de esos 5 archivos en uno solo.

## Turno 4 — Claude

Fusioné los cinco en un único `solucion.py`. Sin argumentos se comporta exactamente como la solución del juez; las herramientas quedan como subcomandos:

| Modo | Comando |
|---|---|
| Solución (juez) | `python solucion.py < entrada.in` |
| Fuerza bruta | `python solucion.py --brute < entrada.in` |
| Stress vs caja negra | `python solucion.py --stress ./caja_linux 500 [seed]` |
| Generador grande | `python solucion.py --gen 5000000 many salida.in` (few, many, dup, invalid, cuts, maxstate) |
| Medición | `python solucion.py --measure salida.in` |

Regresión sobre el archivo fusionado: ambos ejemplos OK; experimentos caja = solución = brute; 400 casos aleatorios nuevos OK (seed 11); brute = solución en 300k líneas; 5M líneas en **6.18 s / 45.0 MB**; entrada vacía → `SIN DATOS`.

---

## Turno 5 — Usuario (13:01)

> ¿Puedes exportar la conversación completa en .md?

## Turno 5 — Claude

Este documento.

---

# ANEXO A — Código final `solucion.py`

```python
#!/usr/bin/env python3
# =============================================================================
# Problema AF - Registro de eventos de red
# Archivo unico. Uso:
#   python solucion.py < entrada.in                 -> SOLUCION (modo juez)
#   python solucion.py --brute < entrada.in         -> fuerza bruta de referencia
#   python solucion.py --stress <caja> <iters> [seed]
#                                                   -> casos aleatorios: caja vs solucion vs brute
#   python solucion.py --gen <N> <modo> <salida>    -> generador de entradas grandes
#        modos: few | many | dup | invalid | cuts | maxstate
#   python solucion.py --measure <entrada> [salida] -> tiempo de pared y RSS maximo
#
# Reglas (descubiertas con la caja negra):
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
#  - Promedio = trunc(1000*s/k + 0.5) (half-up exacto para s >= 0), 3 decimales.
#  - Salida: top 5 por conteo desc, id asc. Sin eventos: SIN DATOS.
# =============================================================================
import sys
from array import array

UMAX = 2_000_000
ACTIONS = {b"LOGIN": 1, b"READ": 2, b"WRITE": 3, b"LOGOUT": 4}


# -----------------------------------------------------------------------------
# 1. SOLUCION OPTIMIZADA (modo juez)
# -----------------------------------------------------------------------------
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


def _fmt_avg(s, k):
    # q = trunc((2000*s + k) / (2*k)) con division entera estilo C (hacia cero).
    # Para s >= 0 es exactamente half-up a milesimas. Se imprime q/1000 "." q%1000
    # con semantica C (relevante solo para promedios negativos, entrada desordenada).
    num = 2000 * s + k
    den = 2 * k
    q = num // den if num >= 0 else -((-num) // den)
    ip = q // 1000 if q >= 0 else -((-q) // 1000)
    return "%d.%03d" % (ip, q - ip * 1000)


def solve_main():
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
            out.append("%d %d %s" % (u, c, _fmt_avg(gap_sum[u], k)))
    sys.stdout.write("\n".join(out) + "\n")


# -----------------------------------------------------------------------------
# 2. FUERZA BRUTA DE REFERENCIA (implementacion independiente, sin optimizar)
# -----------------------------------------------------------------------------
def brute_solve(text):
    from decimal import Decimal, ROUND_DOWN
    lines = text.split(b"\n")
    if len(lines) < 2 or len(lines[0].split()) < 3:
        return "SIN DATOS\n"
    T1, T2, G = map(int, lines[0].split())
    N = int(lines[1].strip()) if lines[1].strip() else 0
    body = lines[2:2 + N]
    events = {}  # user -> lista de (ts, accion) contabilizados
    for raw in body:
        if raw.endswith(b"\r"):
            raw = raw[:-1]
        p = raw.split(b" ")
        if len(p) != 3:
            continue
        ts_s, u_s, act = p
        if not (ts_s.isdigit() and u_s.isdigit()):
            continue
        if len(ts_s) > 12 or len(u_s) > 12:
            continue
        if act not in (b"LOGIN", b"READ", b"WRITE", b"LOGOUT"):
            continue
        ts, u = int(ts_s), int(u_s)
        if u >= 2_000_000 or ts < T1 or ts > T2:
            continue
        lst = events.setdefault(u, [])
        if lst and lst[-1] == (ts, act):
            continue
        lst.append((ts, act))
    rows = []
    for u, lst in events.items():
        gaps = [lst[i][0] - lst[i - 1][0] for i in range(1, len(lst))]
        gaps = [g for g in gaps if g <= G]
        if gaps:
            k = len(gaps)
            # emula la caja: q = trunc(1000*s/k + 0.5), impreso como q/1000 "." q%1000 (C)
            q = int((Decimal(sum(gaps)) * 1000 / Decimal(k) + Decimal("0.5"))
                    .to_integral_value(rounding=ROUND_DOWN))
            ip = abs(q) // 1000 * (1 if q >= 0 else -1)
            s = "%d.%03d" % (ip, q - ip * 1000)
        else:
            s = "NA"
        rows.append((-len(lst), u, s))
    rows.sort()
    if not rows:
        return "SIN DATOS\n"
    return "".join(f"{u} {-c} {s}\n" for c, u, s in rows[:5])


def brute_main():
    sys.stdout.write(brute_solve(sys.stdin.buffer.read()))


# -----------------------------------------------------------------------------
# 3. GENERADOR DE CASOS PEQUENOS + STRESS TEST (caja vs solucion vs brute)
# -----------------------------------------------------------------------------
_ACTS = ["LOGIN", "READ", "WRITE", "LOGOUT"]


def _gen_small(rng):
    mode = rng.randrange(6)
    T1 = rng.randrange(0, 50)
    T2 = T1 + rng.randrange(0, 80)
    G = rng.choice([0, 1, 2, 3, 5, 10, 20, 1000, -1])
    n = rng.randrange(0, 40) if mode != 5 else rng.randrange(200, 301)
    users = [rng.randrange(0, 6) for _ in range(rng.randrange(1, 6))]
    lines = []
    t = rng.randrange(-5, 10)
    for _ in range(n):
        t += rng.choice([0, 0, 0, 1, 1, 2, 3, 5, 11, 25])
        u = rng.choice(users)
        a = rng.choice(_ACTS)
        r = rng.random()
        if mode == 0 or r < 0.75:
            lines.append(f"{t} {u} {a}")
        else:
            k = rng.randrange(14)
            if k == 0:
                lines.append(f"{t} {u} {a.lower()}")
            elif k == 1:
                lines.append(f"{t}  {u} {a}")
            elif k == 2:
                lines.append(f"{t} {u} {a} ")
            elif k == 3:
                lines.append(f"{t} {u}")
            elif k == 4:
                lines.append(f"{t} {u} {a} x")
            elif k == 5:
                lines.append(f"0{t} {u} {a}")          # cero inicial (valido)
            elif k == 6:
                lines.append(f"{t} {rng.choice([1999999, 2000000, 2500000])} {a}")
            elif k == 7:
                lines.append(f"-{t} {u} {a}")
            elif k == 8:
                lines.append(f"{t} {u} {a}\r")
            elif k == 9:
                lines.append("")
            elif k == 10:
                lines.append(f"{t}\t{u} {a}")
            elif k == 11:
                lines.append(f"{'0' * 12}{t} {u} {a}")   # >12 digitos
            elif k == 12:
                lines.append(f"{t} {'0' * 6}{u} {a}")     # ceros iniciales en usuario
            else:
                lines.append(f"+{t} {u} {a}")
    if mode == 4:
        rng.shuffle(lines)  # desordenado
    N = len(lines) + rng.choice([0, 0, 0, 1, -1]) if lines else 0
    N = max(N, 0)
    return f"{T1} {T2} {G}\n{N}\n" + "\n".join(lines) + "\n"


def _run(cmd, data):
    import subprocess
    return subprocess.run(cmd, input=data.encode(), capture_output=True).stdout.decode()


def stress_main(argv):
    import random
    if len(argv) < 2:
        print("uso: --stress <caja> <iters> [seed]"); return
    box, iters = argv[0], int(argv[1])
    seed = int(argv[2]) if len(argv) > 2 else 1
    rng = random.Random(seed)
    me = [sys.executable, __file__]
    for i in range(iters):
        data = _gen_small(rng)
        exp = _run([box], data)
        got = _run(me, data)
        bru = _run(me + ["--brute"], data)
        if exp != got or exp != bru:
            print("MISMATCH en iteracion", i)
            print("--- input"); print(data)
            print("--- caja"); print(exp)
            print("--- solucion"); print(got)
            print("--- brute"); print(bru)
            sys.exit(1)
    print(f"OK {iters} casos (seed {seed})")


# -----------------------------------------------------------------------------
# 4. GENERADOR DE ENTRADAS GRANDES (rendimiento)
# -----------------------------------------------------------------------------
def gen_big_main(argv):
    import random
    if len(argv) < 3:
        print("uso: --gen <N> <few|many|dup|invalid|cuts|maxstate> <salida>"); return
    N, mode, out = int(argv[0]), argv[1], argv[2]
    rng = random.Random(42)
    ACTS = ("LOGIN", "READ", "WRITE", "LOGOUT")
    T1, T2 = 0, 1_000_000_000
    G = 10 if mode == "cuts" else 1_000_000_000
    step = max(T2 // max(N, 1), 1)
    with open(out, "w") as f:
        f.write(f"{T1} {T2} {G}\n{N}\n")
        t = 0
        buf = []
        for i in range(N):
            if mode == "dup":
                if i % 3 == 0:
                    t += step * 3
                u = rng.randrange(0, 1000)
                a = ACTS[(i // 2) % 4]
            else:
                t += step
                if mode == "few":
                    u = rng.randrange(0, 50)
                elif mode == "maxstate":
                    u = i % 2_000_000
                else:
                    u = rng.randrange(0, 2_000_000)
                a = ACTS[i & 3]
            if mode == "invalid" and i % 2:
                k = i % 5
                line = (f"{t} {u} {a} ", f"{t}  {u} {a}", f"{t} {u} read",
                        f"{t} {u}", f"-{t} {u} {a}")[k]
            else:
                line = f"{t} {u} {a}"
            buf.append(line)
            if len(buf) >= 100000:
                f.write("\n".join(buf) + "\n"); buf = []
        if buf:
            f.write("\n".join(buf) + "\n")


# -----------------------------------------------------------------------------
# 5. MEDICION DE TIEMPO Y MEMORIA (ejecuta este mismo archivo en modo juez)
# -----------------------------------------------------------------------------
def measure_main(argv):
    import resource
    import subprocess
    import time
    if len(argv) < 1:
        print("uso: --measure <entrada> [salida]"); return
    inp = argv[0]
    outp = argv[1] if len(argv) > 1 else "/dev/null"
    t0 = time.perf_counter()
    with open(inp, "rb") as fi, open(outp, "wb") as fo:
        r = subprocess.run([sys.executable, __file__], stdin=fi, stdout=fo)
    t1 = time.perf_counter()
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    print(f"{inp}: {t1 - t0:.2f}s  maxrss={ru.ru_maxrss / 1024:.1f} MB  exit={r.returncode}")


# -----------------------------------------------------------------------------
# PUNTO DE ENTRADA: sin argumentos = modo juez
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        solve_main()
    elif args[0] == "--brute":
        brute_main()
    elif args[0] == "--stress":
        stress_main(args[1:])
    elif args[0] == "--gen":
        gen_big_main(args[1:])
    elif args[0] == "--measure":
        measure_main(args[1:])
    else:
        solve_main()
```

# ANEXO B — Experimentos ejecutados en la caja negra

Notación: las entradas se muestran con `cat -A` (`^I` = tabulador, `^M` = retorno de carro `\r`). Los experimentos marcados R2a/R2b/R3 se generaron por script (se listan las primeras 40 líneas).

### E1

Entrada:
```
0 1000 1000
10
10 1 LOGIN
10 1 LOGIN
20 1 READ
20 1 WRITE
30 1 READ
30 2 READ
30 1 READ
30 1 WRITE
30 1 READ
40 1 READ
```
Salida de la caja negra:
```
1 7 5.000
2 1 NA
```

### E2

Entrada:
```
0 1000 10
5
0 1 READ
5 1 READ
15 1 READ
30 1 READ
33 1 READ
```
Salida de la caja negra:
```
1 5 6.000
```

### E3

Entrada:
```
0 1000 1000
7
0 1 LOGIN
5 1 READ
9 1 LOGOUT
11 1 READ
19 1 LOGIN
22 1 READ
28 1 LOGOUT
```
Salida de la caja negra:
```
1 7 4.667
```

### E4

Entrada:
```
0 100000 100000
34
0 1 READ
0 2 READ
1000 1 READ
1000 2 READ
2000 1 READ
2000 2 READ
3000 1 READ
3000 2 READ
4000 1 READ
4000 2 READ
5000 1 READ
5000 2 READ
6000 1 READ
6000 2 READ
7000 1 READ
7000 2 READ
8000 1 READ
8000 2 READ
9000 1 READ
9000 2 READ
10000 1 READ
10000 2 READ
11000 1 READ
11000 2 READ
12000 1 READ
12000 2 READ
13000 1 READ
13000 2 READ
14000 1 READ
14000 2 READ
15000 1 READ
15000 2 READ
16003 2 READ
16010 1 READ
```
Salida de la caja negra:
```
1 17 1000.625
2 17 1000.188
```

### E5

Entrada:
```
0 100 1000
9
10 1 READ
20 1 FOO
30 1 READ
40 2 READ
50 2 READ extra
60 2 READ
70 3 READ
80 3
90 3 READ
```
Salida de la caja negra:
```
1 2 20.000
2 2 20.000
3 2 20.000
```

### E6

Entrada:
```
10 50 1000
6
10 1 READ
50 1 READ
5 2 READ
20 2 READ
60 2 READ
30 3 READ
```
Salida de la caja negra:
```
1 2 40.000
2 1 NA
3 1 NA
```

### E7

Entrada:
```
-100 2000000000 100000000000
7
-5 1 READ
10 1 READ
999999999 2 READ
1000000001 2 READ
20 2000000 READ
30 1999999 READ
40 -1 READ
```
Salida de la caja negra:
```
2 2 2.000
1 1 NA
1999999 1 NA
```

### R1

Entrada:
```
0 1000000 1000000
98
0 1 READ
0 2 READ
1000 1 READ
1010 2 READ
2000 1 READ
2020 2 READ
3000 1 READ
3030 2 READ
4000 1 READ
4030 2 READ
5000 1 READ
5030 2 READ
6000 1 READ
6030 2 READ
7000 1 READ
7030 2 READ
8000 1 READ
8030 2 READ
9000 1 READ
9030 2 READ
10000 1 READ
10030 2 READ
11000 1 READ
11030 2 READ
12000 1 READ
12030 2 READ
13000 1 READ
13030 2 READ
14000 1 READ
14030 2 READ
15000 1 READ
15030 2 READ
16001 1 READ
16030 2 READ
17030 2 READ
18030 2 READ
19030 2 READ
20030 2 READ
... (100 líneas en total)
```
Salida de la caja negra:
```
2 81 1000.375
1 17 1000.063
```

### R2a

Entrada:
```
0 1000000 1000000
243
0 1 READ
0 3 READ
0 4 READ
1001 1 READ
1001 3 READ
1001 4 READ
2002 1 READ
2002 3 READ
2002 4 READ
3003 1 READ
3003 3 READ
3003 4 READ
4003 1 READ
4004 3 READ
4004 4 READ
5003 1 READ
5005 3 READ
5005 4 READ
6003 1 READ
6005 3 READ
6006 4 READ
7003 1 READ
7005 3 READ
7007 4 READ
8003 1 READ
8005 3 READ
8007 4 READ
9003 1 READ
9005 3 READ
9007 4 READ
10003 1 READ
10005 3 READ
10007 4 READ
11003 1 READ
11005 3 READ
11007 4 READ
12003 1 READ
12005 3 READ
... (245 líneas en total)
```
Salida de la caja negra:
```
1 81 1000.038
3 81 1000.063
4 81 1000.088
```

### R2b

Entrada:
```
0 1000000 1000000
149
0 2 READ
0 5 READ
0 6 READ
0 7 READ
0 8 READ
1001 2 READ
1001 5 READ
1001 6 READ
1001 7 READ
1001 8 READ
2001 2 READ
2001 5 READ
2002 6 READ
2002 7 READ
2002 8 READ
3001 2 READ
3001 5 READ
3003 6 READ
3003 7 READ
3003 8 READ
4001 2 READ
4001 5 READ
4003 6 READ
4004 7 READ
4004 8 READ
5001 2 READ
5001 5 READ
5003 6 READ
5005 7 READ
5005 8 READ
6001 2 READ
6001 5 READ
6003 6 READ
6005 7 READ
6006 8 READ
7001 2 READ
7001 5 READ
7003 6 READ
... (151 líneas en total)
```
Salida de la caja negra:
```
2 81 1000.013
5 17 1000.063
6 17 1000.188
7 17 1000.313
8 17 1000.438
```

### R3

Entrada:
```
0 100000 100000
81
0 1 READ
5 1 READ
10 1 READ
15 1 READ
19 1 READ
23 1 READ
27 1 READ
31 1 READ
35 1 READ
39 1 READ
43 1 READ
47 1 READ
51 1 READ
55 1 READ
59 1 READ
63 1 READ
67 1 READ
71 1 READ
75 1 READ
79 1 READ
83 1 READ
87 1 READ
91 1 READ
95 1 READ
99 1 READ
103 1 READ
107 1 READ
111 1 READ
115 1 READ
119 1 READ
123 1 READ
127 1 READ
131 1 READ
135 1 READ
139 1 READ
143 1 READ
147 1 READ
151 1 READ
... (83 líneas en total)
```
Salida de la caja negra:
```
1 81 4.038
```

### F1

Entrada:
```
0 100 1000
4
10 1 READ
20 1 READ extra
20 1 READ
30 1 READ
```
Salida de la caja negra:
```
1 3 10.000
```

### F2

Entrada:
```
0 100 1000
4
10 1 READ
30 1 READ
20 1 READ
40 1 READ
```
Salida de la caja negra:
```
1 4 10.000
```

### F3

Entrada:
```
0 100 1000
9
05 1 READ
+6 1 READ
7.0 1 READ
8 1 read
9^I1^IREAD
10  1  READ
11 1 READ 
12 01 READ
1e1 1 READ
```
Salida de la caja negra:
```
1 2 7.000
```

### F4a

Entrada:
```
0 100 1000
5
10 1 READ
20 1 READ
```
Salida de la caja negra:
```
1 2 10.000
```

### F4b

Entrada:
```
0 100 1000
2
10 1 READ
20 1 READ
30 1 READ
40 1 READ
```
Salida de la caja negra:
```
1 2 10.000
```

### F5a

Entrada:
```
0 100 1000
4
10 1 READ

20 1 READ
30 1 READ
```
Salida de la caja negra:
```
1 3 10.000
```

### F5b

Entrada:
```
0 100 1000^M
3^M
10 1 READ^M
20 1 READ^M
30 1 READ^M
```
Salida de la caja negra:
```
1 3 10.000
```

### F6a

Entrada:
```
0 100 1000
8
1 9 READ
2 8 READ
3 7 READ
4 10 READ
5 11 READ
6 100 READ
7 100 READ
8 5 READ
```
Salida de la caja negra:
```
100 2 1.000
5 1 NA
7 1 NA
8 1 NA
9 1 NA
```

### F6b

Entrada:
```
0 100 1000
2
200 1 READ
300 2 READ
```
Salida de la caja negra:
```
SIN DATOS
```

### F6c

Entrada:
```
0 100 1000
0
```
Salida de la caja negra:
```
SIN DATOS
```

### F7a

Entrada:
```
0 100 0
4
10 1 READ
10 1 WRITE
11 1 READ
11 1 WRITE
```
Salida de la caja negra:
```
1 4 0.000
```

### F7b

Entrada:
```
0 100 -1
3
10 1 READ
10 1 WRITE
11 1 READ
```
Salida de la caja negra:
```
1 3 NA
```

### F8a

Entrada:
```
50 10 1000
2
20 1 READ
30 1 READ
```
Salida de la caja negra:
```
SIN DATOS
```

### F8b

Entrada:
```
0 1000000000 1000000000
3
0 0 READ
1000000000 0 READ
1000000000 0 READ
```
Salida de la caja negra:
```
0 2 1000000000.000
```

### F10

Entrada:
```
0 100 1000
7
10 1 READ
10 1 READ
10 1 READ
20 1 READ
20 1 WRITE
20 1 READ
20 1 WRITE
```
Salida de la caja negra:
```
1 5 2.500
```

### F11

Entrada:
```
0 100 1000
4
 10 1 READ
20 1 READX
30 1 READ
40 1 LOGIN
```
Salida de la caja negra:
```
1 2 10.000
```

### H1

Entrada:
```
0 100 1000
3
10 1 READ

20 1 READ
30 1 READ
```
Salida de la caja negra:
```
1 2 10.000
```

### H2

Entrada:
```
0 100 1000
4
10 1 READ
20 1 READ ^M
30 1 READ^M^M
40 1 READ^M
```
Salida de la caja negra:
```
1 2 30.000
```

### H3

Entrada:
```
0 100 1000
4
10 9999999 READ
20 9999999 READ
30 2000000 READ
40 1999999 READ
```
Salida de la caja negra:
```
1999999 1 NA
```

### H4

Entrada:
```
0 100 1000
4
010 1 READ
10 1 READ
20 01 READ
20 1 READ
```
Salida de la caja negra:
```
1 2 10.000
```

### H5

Entrada:
```
0 100 1000
3
10 00000000000000000001 READ
20 1 READ
30 000001 READ
```
Salida de la caja negra:
```
1 2 10.000
```

### H6

Entrada:
```
0 100 1000
3
10 1 READ
20 1 READ
00000000000000000000000030 1 READ
```
Salida de la caja negra:
```
1 2 10.000
```

### H7

Entrada:
```
0 100 1000
2
10 1 READ
99999999999999999999999 1 READ
```
Salida de la caja negra:
```
1 1 NA
```

### H8

Entrada:
```
0 100 1000
 3 
10 1 READ
20 1 READ
30 1 READ
```
Salida de la caja negra:
```
1 3 10.000
```

### H9

Entrada:
```
0 100 1000
3
10 1 READ
20 1 READ
30 1 READ```
Salida de la caja negra:
```
1 3 10.000
```

### H10

Entrada:
```
0 100 1000
3
10 1 READ
20 2 READ
30 1 READ
```
Salida de la caja negra:
```
1 2 20.000
2 1 NA
```

### H11

Entrada:
```
0 100 1000
4
10 1 LOGIN
10 1 LOGIN
10 1 LOGOUT
10 1 LOGIN
```
Salida de la caja negra:
```
1 3 0.000
```