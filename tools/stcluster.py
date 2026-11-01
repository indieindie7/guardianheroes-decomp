# stcluster.py <ghidra dir> stats|reps|apply: group ST*.BIN functions by masked byte hash (xmatch key);
# names come from GAME/VS/TVS hand files on unique hash match; one representative per unnamed group.
# reps: writes st_reps.txt (ST addr key size). apply: reads naming/o_STREP_*.txt (rep names) and writes hand_ST<n>.txt for all.
import sys, os, hashlib, glob
G, mode = sys.argv[1], sys.argv[2]; os.chdir(G)
def funcs(f):
    return [(int(p[1],16), p[2], int(p[4])) for p in (l.split() for l in open(f,encoding='utf-8',errors='replace')) if p and p[0]=='F']
def key(d, base, a, n):
    b = bytearray(d[a-base:a-base+n])
    for i in range(0, len(b)-3, 2):
        w = int.from_bytes(b[i:i+4],'big')
        if 0x06000000 <= w < 0x06100000 or 0x00200000 <= w < 0x00300000: b[i:i+4] = b'PPPP'
    return hashlib.md5(bytes(b)).hexdigest()+str(n)
def hand(f):
    r = {}
    if os.path.exists(f):
        for l in open(f,encoding='utf-8',errors='replace'):
            p = l.split(None,2)
            if len(p)>=3 and p[1]=='func': r[int(p[0],16)] = p[2].rstrip('\n')
    return r
src = {}
for s in ('GAME','VS','TVS'):
    d = open(f'bin/{s}.BIN','rb').read(); h = hand(f'hand_{s}.txt'); seen = {}
    for a,nm,n in funcs(f'funcinfo_{s}.tsv'):
        if n>8 and a in h: seen.setdefault(key(d,0x06060000,a,n),set()).add(h[a])
    for k,v in seen.items():
        if len(v)==1: src.setdefault(k,set()).update(v)
src = {k:next(iter(v)) for k,v in src.items() if len(v)==1}
sts = sorted(os.path.basename(f)[9:-4] for f in glob.glob('funcinfo_ST[0-9]*.tsv'))
groups = {}; members = []
for s in sts:
    d = open(f'bin/{s}.BIN','rb').read()
    for a,nm,n in funcs(f'funcinfo_{s}.tsv'):
        k = key(d,0x06098000,a,n) if n>8 else f'{s}:{a:x}'
        groups.setdefault(k,[]).append((s,a,n)); members.append((s,a,k))
named = {k for k in groups if k in src}
print('sts',len(sts),'fns',len(members),'groups',len(groups),'named-from-src',sum(len(groups[k]) for k in named),'unnamed groups',len(groups)-len(named))
if mode=='reps':
    with open('st_reps.txt','w') as w:
        for k,v in groups.items():
            if k not in named: s,a,n = v[0]; w.write(f'{s} 0x{a:08x} {k} {n} {len(v)}\n')
if mode=='apply':
    rk = {}
    for l in open('st_reps.txt'):
        s_,a_,k_,n_,c_ = l.split(); rk[k_] = (s_,a_)
    repn = {}
    for f in glob.glob('naming/o_STREP_*.txt'):
        for l in open(f,encoding='utf-8',errors='replace'):
            p = l.strip().split(None,3)
            if len(p)==4 and p[0].startswith('ST') and p[2]=='func': repn[(p[0],p[1].lower())] = p[3]
    out = {s:[] for s in sts}; miss = 0
    for s,a,k in members:
        if k in src: rest = src[k]
        elif k in rk and (rk[k][0], rk[k][1]) in repn: rest = repn[rk[k]]
        else: miss += 1; continue
        out[s].append(f'0x{a:08x} func {rest}')
    for s,v in out.items(): open(f'hand_{s}.txt','w',encoding='utf-8').write('\n'.join(v)+'\n')
    print('written', sum(len(v) for v in out.values()), 'missing', miss)
if mode=='slices':
    import re
    byst = {}
    for l in open('st_reps.txt'):
        s_,a_,k_,n_,c_ = l.split(); byst.setdefault(s_,set()).add(a_[2:])
    blocks = []
    for s_ in sorted(byst):
        for b in re.split(r'(?m)^(?=// ==== )', open(f'decomp_{s_}.c',encoding='utf-8',errors='replace').read()):
            m = re.match(r'// ==== \S+ @ ([0-9a-f]{8})', b)
            if m and m.group(1) in byst[s_]: blocks.append(f'// ######## PROGRAM {s_}\n'+b)
    per = 130
    for k in range(0,len(blocks),per): open(f'naming/STREP_{k//per+1}.c','w',encoding='utf-8').write(''.join(blocks[k:k+per]))
    print('rep blocks',len(blocks),'slices',(len(blocks)+per-1)//per)
