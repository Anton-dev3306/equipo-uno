import sys
from array import array
from heapq import heappush, heappop
 
CHOOSE_BEST_PATH = True   # S1
BOTH_DIRECTIONS = True    # S2
 
# Centinela de "inalcanzable" que cabe en int64 (array 'q'):
#   distancia real maxima = (N-1)*w_max = 199999*4e13 < 8e18 < 2^63-1.
# Las sumas intermedias (dS+w+dT, bestU+dV) se hacen en int de Python, que
# no desborda; en los arrays solo se guardan distancias reales o INF.
INF = (1 << 63) - 1
 
 
def dijkstra(n, head, nxt, to, wt, src, want_par=False):
    dist = array('q', [INF]) * (n + 1)
    par = array('q', [-1]) * (n + 1) if want_par else None
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heappop(pq)
        if d > dist[u]:
            continue
        e = head[u]
        while e != -1:
            v = to[e]
            nd = d + wt[e]
            if nd < dist[v]:
                dist[v] = nd
                if want_par:
                    par[v] = e
                heappush(pq, (nd, v))
            e = nxt[e]
    return dist, par
 
 
def build_graph(n, m, ea, eb, ew):
    """Forward-star con arrays: la via i genera las aristas dirigidas
    2i (a->b) y 2i+1 (b->a)."""
    head = array('q', [-1]) * (n + 1)
    nxt = array('q', [0]) * (2 * m)
    to = array('q', [0]) * (2 * m)
    wt = array('q', [0]) * (2 * m)
    k = 0
    for i in range(m):
        a = ea[i]; b = eb[i]; w = ew[i]
        to[k] = b; wt[k] = w; nxt[k] = head[a]; head[a] = k; k += 1
        to[k] = a; wt[k] = w; nxt[k] = head[b]; head[b] = k; k += 1
    return head, nxt, to, wt
 
 
def solve(n, edges, s, t, u, v,
          choose_best=CHOOSE_BEST_PATH, both_dirs=BOTH_DIRECTIONS):
    """edges: lista de tuplas (a,b,w) o tripleta de arrays (ea, eb, ew)."""
    if isinstance(edges, tuple):
        ea, eb, ew = edges
    else:
        ea = array('q', [a for a, _, _ in edges])
        eb = array('q', [b for _, b, _ in edges])
        ew = array('q', [w for _, _, w in edges])
    m = len(ea)
    head, nxt, to, wt = build_graph(n, m, ea, eb, ew)
 
    dS, parS = dijkstra(n, head, nxt, to, wt, s, want_par=not choose_best)
    dU, _ = dijkstra(n, head, nxt, to, wt, u)
    ans = dU[v]
    D = dS[t]
    if D == INF:                                  # S3
        return -1 if ans == INF else ans
    dT, _ = dijkstra(n, head, nxt, to, wt, t)
    dV, _ = dijkstra(n, head, nxt, to, wt, v)
 
    dag_in = [None] * (n + 1)                     # y -> [x] (vias x->y del DAG)
    if choose_best:
        verts = []
        for x in range(1, n + 1):
            if dS[x] + dT[x] == D:
                verts.append(x)
                dag_in[x] = []
        for i in range(m):
            a = ea[i]; b = eb[i]
            if a == b or dag_in[a] is None or dag_in[b] is None:
                continue
            w = ew[i]
            if dS[a] + w + dT[b] == D:
                dag_in[b].append(a)
            if dS[b] + w + dT[a] == D:
                dag_in[a].append(b)
    else:
        verts = [t]
        dag_in[t] = []
        x = t
        while x != s:
            e = parS[x]
            p = to[e ^ 1]
            dag_in[x].append(p)
            if dag_in[p] is None:
                dag_in[p] = []
            verts.append(p)
            x = p
    verts.sort(key=dS.__getitem__)                # orden topologico
 
    bestU = array('q', [INF]) * (n + 1)
    bestV = array('q', [INF]) * (n + 1)
    for y in verts:
        bu = dU[y]
        bv = dV[y]
        for x in dag_in[y]:
            if bestU[x] < bu:
                bu = bestU[x]
            if bestV[x] < bv:
                bv = bestV[x]
        bestU[y] = bu
        bestV[y] = bv
        c = bu + dV[y]                            # ida
        if c < ans:
            ans = c
        if both_dirs:
            c = bv + dU[y]                        # vuelta
            if c < ans:
                ans = c
    return -1 if ans == INF else ans
 
 
def main():
    # Parseo directo a un array de int64: evita la lista de tuplas y libera
    # los tokens en cuanto se consumen (memoria ~ 8 bytes por numero).
    vals = array('q', map(int, sys.stdin.buffer.read().split()))
    n = vals[0]; m = vals[1]
    s = vals[2]; t = vals[3]; u = vals[4]; v = vals[5]
    ea = vals[6::3]
    eb = vals[7::3]
    ew = vals[8::3]
    del vals
    sys.stdout.write(str(solve(n, (ea, eb, ew), s, t, u, v)) + "\n")
 
 
if __name__ == "__main__":
    main()