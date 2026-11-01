"""Split ghidra/decomp_<n>.c into naming slices ghidra/naming/<P>_<k>.c (~150 fns each, split at '// ====' lines).
usage: py -3.13 -I slice.py <decomp.c> <outdir> <prefix> [fns_per_slice=150]"""
import sys,os
src,out,pre=sys.argv[1:4]; per=int(sys.argv[4]) if len(sys.argv)>4 else 150
L=open(src,encoding='utf-8',errors='replace').read().split('\n')
starts=[i for i,l in enumerate(L) if l.startswith('// ====')]
head=L[:starts[0]] if starts else []
os.makedirs(out,exist_ok=True)
k=0
for s in range(0,len(starts),per):
    k+=1; a=starts[s]; b=starts[s+per] if s+per<len(starts) else len(L)
    open(os.path.join(out,f'{pre}_{k}.c'),'w',encoding='utf-8',newline='\n').write('\n'.join(L[a:b])+'\n')
print(len(starts),'functions',k,'slices')
