import sys
import array
 
 
def solve(N, L, R, M, a):
    pos = []
    vals = []
    for idx in range(N):
        v = a[idx]
        if v != 0:
            pos.append(idx + 1)
            vals.append(v)
    K = len(vals)
    if K == 0:
        return 0, 0
 
    Pc = array.array('i', [0]) * (K + 1)
    for t in range(1, K + 1):
        Pc[t] = Pc[t - 1] + (1 if vals[t - 1] >= M else -1)
 
    pos_a = array.array('i', pos)
    count_i = array.array('i', [0]) * (K + 1)
    sumI = array.array('q', [0]) * (K + 1)
    for p in range(1, K + 1):
        lb = pos_a[p - 2] + 1 if p > 1 else 1
        pp = pos_a[p - 1]
        ci = pp - lb + 1
        count_i[p] = ci
        sumI[p] = (lb + pp) * ci // 2
 
    count_j = array.array('i', [0]) * (K + 1)
    sumJ = array.array('q', [0]) * (K + 1)
    for q in range(1, K + 1):
        rb = pos_a[q] - 1 if q < K else N
        pq = pos_a[q - 1]
        cj = rb - pq + 1
        count_j[q] = cj
        sumJ[q] = (pq + rb) * cj // 2
    del pos, vals, pos_a
 
    offset = K
    size = 2 * K + 1
 
    FA = [array.array('q', [0]) * size for _ in range(2)]
    FB = [array.array('q', [0]) * size for _ in range(2)]
 
    def update(fa, fb, idx, aval, bval, sign):
        x = idx + 1
        while x <= size:
            fa[x - 1] += sign * aval
            fb[x - 1] += sign * bval
            x += x & (-x)
 
    def query(fa, fb, idx):
        x = idx + 1
        sa = 0
        sb = 0
        while x > 0:
            sa += fa[x - 1]
            sb += fb[x - 1]
            x -= x & (-x)
        return sa, sb
 
    total_count = 0
    total_len = 0
    added_up_to = -1
    removed_before = 0
 
    EVEN_THR = 0  # mediana superior (confirmado por caja negra)
    ODD_THR = 1
 
    for v in range(1, K + 1):
        lo = max(v - R, 0)
        hi = v - L
        if hi < 0:
            continue
        hi = min(hi, K - 1)
 
        while added_up_to < hi:
            added_up_to += 1
            u = added_up_to
            p = u + 1
            par = u % 2
            update(FA[par], FB[par], Pc[u] + offset, count_i[p], sumI[p], 1)
 
        while removed_before < lo:
            u = removed_before
            p = u + 1
            par = u % 2
            update(FA[par], FB[par], Pc[u] + offset, count_i[p], sumI[p], -1)
            removed_before += 1
 
        if lo > hi:
            continue
 
        parv = v % 2
        cj = count_j[v]
        sj = sumJ[v]
 
        idx_even = Pc[v] - EVEN_THR + offset
        if idx_even >= 0:
            A_e, B_e = query(FA[parv], FB[parv], min(idx_even, size - 1))
        else:
            A_e, B_e = 0, 0
 
        idx_odd = Pc[v] - ODD_THR + offset
        if idx_odd >= 0:
            A_o, B_o = query(FA[1 - parv], FB[1 - parv], min(idx_odd, size - 1))
        else:
            A_o, B_o = 0, 0
 
        total_count += cj * (A_e + A_o)
        total_len += (sj + cj) * (A_e + A_o) - cj * (B_e + B_o)
 
    return total_count, total_len
 
 
def main():
    raw = sys.stdin.buffer.read()
    it = map(int, raw.split())
    N = next(it); L = next(it); R = next(it); M = next(it)
    a = array.array('i', (next(it) for _ in range(N)))
    del raw, it
    c, s = solve(N, L, R, M, a)
    sys.stdout.write(f"{c} {s}\n")
 
 
if __name__ == "__main__":
    main()