# basefind.py: per file, kind (code/data) + best load base by votes (BE words pointing into file at SH-2 prologues)
import sys, os, numpy as np
D = sys.argv[1] if len(sys.argv) > 1 else 'saturn/cd'
PRO = (0x2fe6, 0x4f22, 0x2fd6, 0x2fc6, 0x2fb6)  # mov.l r14/r13/r12/r11,@-r15 ; sts.l pr
def analyze(path):
    d = open(path, 'rb').read()
    n = len(d)
    h = np.frombuffer(d[:n & ~1], '>u2')
    rts = int((h == 0x000b).sum())
    pro = int(np.isin(h, PRO).sum())
    kind = 'code' if n >= 2000 and rts * 400 > n // 2 * 0.0 + 0 and rts >= max(8, n // 1200) and pro >= max(8, n // 1500) else 'data'
    res = None
    if kind == 'code':
        P = np.nonzero(np.isin(h, PRO))[0] * 2
        w = np.frombuffer(d[:n & ~3], '>u4').astype(np.int64)
        w = w[((w >= 0x06000000) & (w < 0x06100000)) | ((w >= 0x00200000) & (w < 0x00300000))]
        w = np.unique(w)
        best = None
        for lo, hi in ((0x06000000, 0x06100000), (0x00200000, 0x00300000)):
            ww = w[(w >= lo) & (w < hi)]
            if not len(ww): continue
            b = (ww[:, None] - P[None, :]).ravel()
            b = b[(b >= lo) & (b < hi) & (b % 4 == 0)]
            if not len(b): continue
            c = np.bincount(b - lo)
            i = int(c.argmax()); 
            if best is None or c[i] > best[1]: best = (lo + i, int(c[i]), int(np.sort(c)[-2]))
        res = best
    return n, kind, rts, pro, res
if __name__ == '__main__':
    for f in sorted(os.listdir(D)):
        if f.endswith(('.TNE', '.SEQ', '.CPK', '.DSP', '.MAP')): continue
        n, k, r, p, res = analyze(os.path.join(D, f))
        print(f, n, k, r, p, ('0x%08x votes=%d 2nd=%d' % res) if res else '-', sep='\t')
