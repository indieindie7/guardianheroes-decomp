# Guardian Heroes (Sega Saturn, Treasure, 1996) reverse-engineering notes and symbols

Hand-named function map, naming prompt and tools for **Guardian Heroes** (MK-81035, Europe): the kernel `0KRNL.BIN` (SH-2, loaded at 0x06004000), the 14 mode overlays its dispatcher `main_ModeDispatch` loads into one shared slot at 0x06060000 (GAME, VS, TVS, VSTART, DEMO, OPTION, ENDING, EXP, START, TITLE, SEGA, TRE, TEST, OVER, BUP_CHK), and 62 unique stage overlays `ST*.BIN` loaded by GAME/VS at 0x06098000 (`ghidra/st_dedupe.txt`: ST191 = ST151 and ST192 = ST182 byte-identical, skipped).
Current state (after round 1 naming + one review round on the main program):

| Program | Functions | Named | Provisional |
|---|---|---|---|
| 0KRNL | 497 | 497 | 18 |
| GAME | 522 | 522 | 224 |
| VS | 1,580 | 1,580 | 712 |
| TVS | 1,581 | 1,581 | 714 |
| VSTART | 62 | 62 | 20 |
| DEMO | 111 | 111 | 27 |
| OPTION | 23 | 23 | 4 |
| ENDING | 27 | 27 | 0 |
| EXP | 21 | 21 | 0 |
| START | 8 | 8 | 0 |
| TITLE | 4 | 4 | 0 |
| SEGA | 2 | 2 | 0 |
| TRE | 2 | 2 | 0 |
| TEST | 3 | 3 | 0 |
| OVER | 4 | 4 | 0 |
| BUP_CHK | 9 | 9 | 0 |
| ST*.BIN (62 files) | 6,256 | 6,256 | 2,967 |

Stage overlays: `tools/stcluster.py` groups the 6,256 stage functions by masked byte hash; 5,166 took names from GAME/VS/TVS, the 365 remaining groups were named once on a representative and copied to every member.
0 `FUN_` placeholders left.

- Round 1 (11-01): every function Ghidra found (SH-2 `4f22`/`2fe6` prologue seeding + `CreateAt.java`) named from its decompile and strings in ~150-function slices by Sonnet agents; unsure names carry `provisional` in the comment.
- Review round 1 (11-01): the main program's provisional names re-read with callers/callees (`ghidra/review/all_*_rv.txt`: `<prog> 0x<addr> <old> CONFIRM/RENAME/UNSURE <new> <reason>`).
- Overlays: names copied from already-named programs by masked byte hashes (`tools/xmatch.py`: SH-2 literal-pool words that look like pointers are masked, a name is copied only on a unique match), the rest named like round 1.

Subsystem prefixes (most common first): chr_ (characters), vs_ (versus mode), en_ (enemies), obj_, stg_ (stages), proj_ (projectiles), gfs_/cdc_ (GFS, CD block), eft_/fx_ (effects), ai_, cpk_ (Cinepak), buf_, spell_, snd_, math_, combat_, gfx_, sys_, game_, cam_, hud_.

Same method as [deadoralive-decomp](https://github.com/indieindie7/deadoralive-decomp). Non-commercial, done for study and preservation.

**No game data is included**: no disc image, no executables, no overlays, no decompiled C, no game text,
no Ghidra database. You need your own copy of the game to use any of this.

## What is here

| Path | Content |
|---|---|
| `NOTES.md` | disc layout, load bases and how they were found, pipeline, log |
| `ghidra/hand_<prog>.txt` | hand names: `0x<addr> func <name> hand <comment>` (apply with `ghidra/scripts/ApplyNames.java`, hand mode) |
| `ghidra/funcinfo_<prog>.tsv` | per-function export: `F` address name source size, `C` callees (string rows removed) |
| `ghidra/naming/` | the naming prompt |
| `ghidra/review/` | review verdict lines |
| `ghidra/scripts/` | `FindSh2FunctionsMem.java` (prologue seeding), `CreateAt.java`, `ApplyNames.java`, `ExportFuncInfo.java`, `CsDumpAll.java` / `DumpDecomp.java` (decompile dump), `DataRefs.java`, `DeleteFunctions.java` |
| `tools/` | `slice.py` (naming slices), `pubfuncinfo.py`, `basefind.py` (overlay base vote), `stcluster.py` (stage-overlay hash groups) |

## Licence

Notes, names and tools: MIT (see `LICENSE`). Guardian Heroes belongs to its rights holders; nothing from the
game is distributed here.
