# Guardian Heroes (Saturn) decomp — NOTES
## Index
1. Source + layout  2. Pipeline  3. Log
## 1. Source + layout
- User 11-01: <own disc rip> (Europe, 24 tracks: 1 data + 23 audio). Unpacked: saturn/image (bin/cue), saturn/cd (isoextract.py 2352, Scorcher/tools; 489 files, 66.5 MB).
- IP.BIN: SEGA ENTERPRISES, MK-81035 V1.000, 1996-04-23, area JT E, 1st read size 0x2000, load addr 0x06004000.
- Main exe 0KRNL.BIN (104112 B), base 0x06004000 (verified: 399 of 1515 in-range pointers hit prologues, vs 28 at 0x06000000).
- OVERLAYS (SH-2 code, NOT imported; load addresses unknown): GAME.BIN (214876 B, 546 prologues), VS.BIN (520300 B, 1436), TVS.BIN (521284 B, 1437), VSTART.BIN (80264 B, 92), ~161 stage code files ST<nn><n>.BIN (28-85 KB, ~90-180 prologues each; start 2fe6 6e53), also TITLE/OPTION/DEV/END*_D etc. to check. Data: *.TNE sprites/tiles, *.SEQ, S*CHR.BIN, BG_*.BIN, SND.DRV (68000), OPEN.CPK movie.
- Never push disc data. 
## 2. Pipeline (copied from FightingVipers 11-01)
- ghidra/run.sh <abs log> <args> (project GH), ghidra/import.sh <file in bin/> <base> = import SH-2 + FindSh2FunctionsMem + CreateAt + ExportFuncInfo + CsDumpAll. Run with HOGGATE=ok when hoggate blocks.
- tools/slice.py <decomp> ghidra/naming GH -> ~150-fn slices. Prompt ghidra/scripts/prompt_GH.txt.
- Then naming (Sonnet agents -> naming/q_<n>.txt), hand_<exe>.txt, ApplyNames, export, provisional review. No pushing yet.
## 3. Log
- 11-01: import 0KRNL.BIN @0x06004000 DONE: F=497 (funcinfo_0KRNL.tsv, decomp_0KRNL.c). Slices ghidra/naming/GH_1..4.c. No names applied.
- 11-01: round 1 named: naming/q_1..4 -> ghidra/hand_0KRNL.txt 496 (237 provisional) via Documents/Tools/decomp/mergeapply.sh (merge + ApplyNames + export + dump); F=497 FUN=0. Next: provisional review, overlays (agent basefind), publish guardianheroes-decomp.

## Overlays
- 11-01 tools/basefind.py (py -3.13 -I tools/basefind.py [dir]): per file code/data + base vote (BE words pointing into file at 2fe6/4f22-family prologues). Table below.
- Kernel main_ModeDispatch (0x0600443c) calls cd_LoadFileStart(name, 0x06060000) for BUP_CHK SEGA TRE DEMO TITLE OPTION TEST OVER ENDING EXP START VSTART GAME VS TVS, then calls 0x06060000 = entry at file offset 0. One shared slot, one overlay at a time. STIT.BIN loads to 0x00200000 (image data, not code).
- Stage overlays ST*.BIN: loaded by GAME/VS (not by kernel); basefind votes 0x06098000 for all 64 (votes 8..107, runner-up 0.4-0.6x), entry at offset 0 (prologue 2fe6 6e53). Stage slot sits above GAME.BIN (0x06060000+214876 = 0x060928dc < 0x06098000 ok). Weakest (confirm in Ghidra): ST011 ST012 ST041 ST062 ST102 ST201 (8-12 votes).
- Identical-start groups (first 64 B): ST151=ST181=ST191 (151/191 byte-identical), ST152=ST182=ST192=ST221 (182/192 identical), ST231=ST261. VS.BIN and TVS.BIN same first code bytes/size class (520300 vs 521284), same base.

| file | size | kind | base | evidence |
|---|---|---|---|---|
| 0KRNL.BIN | 104112 | code | 0x06004000 | IP.BIN, 216 votes |
| GAME.BIN | 214876 | code | 0x06060000 | dispatcher arg, 339 votes vs 104 |
| VS.BIN | 520300 | code | 0x06060000 | dispatcher, 860 v |
| TVS.BIN | 521284 | code | 0x06060000 | dispatcher, 861 v |
| VSTART.BIN | 80264 | code | 0x06060000 | dispatcher, 55 v |
| OPTION.BIN | 63092 | code | 0x06060000 | dispatcher, 43 v |
| ENDING.BIN | 45908 | code | 0x06060000 | dispatcher, 27 v |
| DEMO.BIN | 24972 | code | 0x06060000 | dispatcher, 61 v |
| TITLE.BIN | 23040 | code | 0x06060000 | dispatcher; starts 2fe6 prologue |
| EXP.BIN | 14292 | code | 0x06060000 | dispatcher, 15 v |
| START.BIN | 9884 | code | 0x06060000 | dispatcher (basefind weak 8 v) |
| SEGA/TRE/TEST/OVER/BUP_CHK.BIN | 20144/6864/1552/1528/5384 | code | 0x06060000 | dispatcher; start 2fe6 prologue |
| ST*.BIN (64 files, ST011..ST301 incl. ST03VS ST05VS ST12VS) | 16.7-85 KB | code | 0x06098000 | basefind votes, entry offset 0 |
| STIT.BIN | 107520 | data (image) | 0x00200000 | kernel game_LoadStitImage |
| V*.BIN, V*MAP.BIN, VVS*, S*CHR, BG_*, E1/E2*, END*_D, character .BIN (HAN GIN ...), SIM*, SND_DATA, SP_CHR etc | - | data | - | rts/prologue counts ~0, no pointer votes |
- Code overlays total: 15 named + 6 small + 64 ST = 85 (+0KRNL). Next: import GAME.BIN and one ST at their bases (ghidra/import.sh <file> <base>).
- 11-01: review r1 applied (all_GH_rv.txt, backup hand_0KRNL.r0.txt): 159 confirmed, 60 renamed, 18 provisional. Overlays imported at 0x06060000: GAME 522, VS 1580, TVS 1581, VSTART 62, OPTION 23, ENDING 27, DEMO 111, EXP 21, START 8, TITLE 4, SEGA 2, TRE 2, TEST 3, OVER 4, BUP_CHK 9 fns.
- 11-01: overlay names applied (all FUN=0): GAME 522 (224 prov), VSTART 62, DEMO 111, OPTION 23, ENDING 27, EXP 21, START 8, TITLE 4, SEGA 2, TRE 2, TEST 3, OVER 4, BUP_CHK 9. xmatch GAME->VS 494/1580; VS 1078 FUN_ sliced naming/VS_1..8.c, workflow wf_05e708c9-dd3 -> naming/o_VS_<k>.txt.
- 11-01: VS names applied (hand_VS 1572, prov 712, FUN=0). xmatch VS->TVS 1186/1581, TVS 387 FUN_ -> naming/TVS_1..3.c.
- 11-01: ST*.BIN: 62 unique imported at 0x06098000 (ghidra/st_dedupe.txt: ST192=ST182, ST191=ST151 skipped), 6256 fns. tools/stcluster.py <ghidra> stats|reps|slices|apply: masked-byte hash groups (xmatch key); 5166 fns named from GAME/VS/TVS hashes, 365 unnamed groups -> one rep each (ghidra/st_reps.txt, naming/STREP_1..3.c). Agent output naming/o_STREP_<k>.txt lines "(debug text)"; apply writes hand_ST<n>.txt for all 62. Workflow wf_c5f2eaf9-6f2 (TVS + STREP).
- 11-01: TVS applied (1573 hand, 714 prov, FUN=0). ST apply: stcluster apply wrote hand_ST<n>.txt (6256, 0 missing, 2967 prov); all 62 ST FUN=0. Gotcha: in bash loops pass "$W\hand_$s.txt", not "$W\$f" (escapes the $).
