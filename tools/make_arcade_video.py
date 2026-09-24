# Generates media/arcade-explainer.mp4 frame by frame (PIL + ffmpeg).
# Explains the Blockz10 Arcade game in the game's own aesthetic:
# black background, gold tiles, green kills, blinking next target.
import os
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
BG = (6, 8, 6)
GREEN = (0, 230, 118)
DIM = (110, 200, 150)
WHITE = (235, 235, 235)
GREY = (150, 150, 150)
GOLD = (255, 213, 79)
BLUE = (129, 212, 250)
RED = (244, 67, 54)
DARKCELL = (10, 14, 8)

FONTS = r"C:\Windows\Fonts"
MONO_B = lambda s: ImageFont.truetype(os.path.join(FONTS, "consolab.ttf"), s)
MONO = lambda s: ImageFont.truetype(os.path.join(FONTS, "consola.ttf"), s)
SANS = lambda s: ImageFont.truetype(os.path.join(FONTS, "segoeui.ttf"), s)
SANS_B = lambda s: ImageFont.truetype(os.path.join(FONTS, "segoeuib.ttf"), s)

OUT = Path(__file__).resolve().parents[1] / "media"
FRAMES = OUT / "_aframes"
FRAMES.mkdir(parents=True, exist_ok=True)

frames: list[tuple[str, float]] = []
_n = 0
rng = random.Random(10)


def canvas():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def save(img, dur):
    global _n
    name = f"a{_n:04d}.png"
    img.save(FRAMES / name)
    frames.append((name, dur))
    _n += 1


def center(d, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)


def footer(d):
    center(d, H - 44, "Joaquim Pedro de Morais Filho  \u00b7  j360074@hotmail.com", MONO(20), DIM)


def tile(d, x, y, ch, size=72, color=GOLD, dead=False):
    if dead:
        return
    d.rounded_rectangle([x, y, x + size, y + size], radius=8,
                        outline=color, width=4, fill=DARKCELL)
    f = MONO_B(int(size * 0.55))
    w = d.textlength(ch, font=f)
    d.text((x + (size - w) / 2, y + size * 0.18), ch, font=f, fill=color)


def board(d, grid, x0, y0, size=72, gap=12, dead=set(), hint=set(), colors={}):
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch is None:
                continue
            idx = (r, c)
            if idx in dead:
                continue
            col = colors.get(idx, GREEN if idx in hint else GOLD)
            tile(d, x0 + c * (size + gap), y0 + r * (size + gap), ch, size, col)


def seq_line(d, y, chars, pos, x0=None, fs=44, spacing=None):
    spacing = spacing or fs + 26
    total = len(chars) * spacing
    x = (W - total) / 2 if x0 is None else x0
    for i, ch in enumerate(chars):
        col = GREEN if i < pos else (GOLD if i == pos else GREY)
        f = MONO_B(fs)
        w = d.textlength(ch, font=f)
        d.text((x + i * spacing + (spacing - w) / 2, y), ch, font=f, fill=col)
    return x


# ---- Scene 1: title ---------------------------------------------------------
img, d = canvas()
center(d, 140, "\u00abBlockz10 Arcade\u00bb", MONO_B(74), GOLD)
center(d, 275, "Treino de QI cripto \u2014 mate as letras na ordem certa", SANS(32), WHITE)
center(d, 328, "Crypto IQ training \u2014 kill the letters in the right order", SANS(24), GREY)
gx = (W - 5 * 84) / 2
for i, ch in enumerate("e13h1"):
    tile(d, gx + i * 84, 420, ch, 72, GOLD if i != 1 else GREEN)
center(d, 560, "por Joaquim Pedro de Morais Filho", SANS(24), DIM)
save(img, 5.0)

# ---- Scene 2: the board & controls ------------------------------------------
GRID = [
    ["e", "7", "w", "1", "h", "j"],
    ["2", "q", "e", "4", "3", "y"],
    ["u", "1", "b", "x", "d", "g"],
]
img, d = canvas()
center(d, 54, "O tabuleiro / The board", SANS_B(38), GOLD)
board(d, GRID, 320, 140)
d.text((880, 170), "\u00bb digite a letra", font=SANS_B(26), fill=WHITE)
d.text((880, 208), "type the letter", font=SANS(20), fill=GREY)
d.text((880, 270), "\u00bb ou clique no tile", font=SANS_B(26), fill=WHITE)
d.text((880, 308), "or click the tile", font=SANS(20), fill=GREY)
d.text((880, 370), "tile morto some \u00b7", font=SANS(24), fill=GREEN)
d.text((880, 404), "novos nascem", font=SANS(24), fill=GREEN)
d.text((880, 442), "dead tiles vanish \u00b7 new ones spawn", font=SANS(18), fill=GREY)
footer(d)
save(img, 7.0)

# ---- Scene 3: the sequence panel ----------------------------------------------
img, d = canvas()
center(d, 54, "A sequ\u00eancia diz o que matar / The sequence tells you what to kill",
       SANS_B(32), GOLD)
seq_line(d, 170, list("e11e1e"), 2)
d.text((240, 280), "\u25a0 verde = j\u00e1 matou / killed", font=SANS(26), fill=GREEN)
d.text((240, 330), "\u25a0 dourada piscando = a PR\u00d3XIMA / the NEXT one", font=SANS(26), fill=GOLD)
d.text((240, 380), "\u25a0 cinza = ainda vem / coming up", font=SANS(26), fill=GREY)
center(d, 480, "errou a ordem? \u22128 QI e \u22122 segundos / wrong order? \u22128 IQ and \u22122 seconds",
       SANS(26), RED)
center(d, 540, "bot\u00e3o DICA acende os alvos por 3 QI / HINT button lights targets for 3 IQ",
       SANS(24), BLUE)
footer(d)
save(img, 8.0)

# ---- Scene 4: kill animation (sequence advancing, tiles dying) -----------------
seq = list("e11e1")
positions = [(0, 0), (0, 3), (2, 1), (1, 2), (1, 0)]  # not used directly; cosmetic
dead = set()
kill_order = [(0, 0), (0, 3), (2, 1), (1, 2)]
for step in range(5):
    img, d = canvas()
    center(d, 40, "FASE 1 \u00b7 CA\u00c7A {e,1} / PHASE 1 \u00b7 {e,1} HUNT", MONO_B(30), GOLD)
    seq_line(d, 100, seq, step)
    board(d, GRID, 320, 200, dead=dead)
    if step < 4:
        r, c = kill_order[step]
        d.text((880, 250), f"pr\u00f3ximo / next:  \u201c{seq[step]}\u201d", font=MONO_B(28), fill=GOLD)
        d.text((880, 310), "+%d QI" % (8 + step * 2) if step else "+8 QI", font=MONO_B(34), fill=GREEN)
        d.text((880, 370), f"combo \u00d7{min(9, 1 + step)}", font=MONO_B(26), fill=BLUE)
    else:
        d.text((880, 290), "sequ\u00eancia completa!", font=SANS_B(26), fill=GREEN)
        d.text((880, 330), "sequence complete!", font=SANS(20), fill=GREY)
    footer(d)
    save(img, 1.15 if step < 4 else 2.6)
    if step < 4:
        dead.add(kill_order[step])

# ---- Scene 5: the four phases ---------------------------------------------------
img, d = canvas()
center(d, 50, "4 miss\u00f5es geradas sem fim / 4 endlessly generated missions", SANS_B(34), GOLD)
rows = [
    ("1 \u00b7 CA\u00c7A {e,1}", "mate e e 1 na ordem \u2014 o alfabeto do Blockz10",
     "kill e and 1 in order \u2014 the Blockz10 alphabet"),
    ("2 \u00b7 S\u00d3 HEX", "0\u20139 e a\u2013f valem \u00b7 g\u2013z s\u00e3o armadilhas",
     "0\u20139 and a\u2013f count \u00b7 g\u2013z are traps"),
    ("3 \u00b7 CODIFICA\u00c7\u00c3O 311", "eee11 \u2192 mate 3, 1, 1 \u2014 a compress\u00e3o real do sistema",
     "eee11 \u2192 kill 3, 1, 1 \u2014 the system's real compression"),
    ("4 \u00b7 ANAGRAMA", "soletre HMAC, SALT, ENTROPIA\u2026 na ordem",
     "spell HMAC, SALT, ENTROPY\u2026 in order"),
]
y = 150
for k, pt, en in rows:
    d.text((120, y), k, font=MONO_B(27), fill=GREEN)
    d.text((520, y), pt, font=SANS(24), fill=WHITE)
    d.text((520, y + 33), en, font=SANS(18), fill=GREY)
    y += 108
center(d, y + 6, "cada fase ensina um conceito real de criptografia",
       SANS(24), GOLD)
save(img, 9.0)

# ---- Scene 6: encoding phase demo -------------------------------------------------
img, d = canvas()
center(d, 54, "FASE 3 \u00b7 a fase de QI / PHASE 3 \u00b7 the IQ phase", SANS_B(34), GOLD)
center(d, 150, "eee11", MONO_B(58), WHITE)
center(d, 230, "\u2193  runs de \u201ce\u201d viram n\u00famero \u00b7 \u201c1\u201d fica literal", SANS(24), GREY)
seq_line(d, 290, list("311"), 1, fs=54)
gx = (W - 6 * 84) / 2
for i, ch in enumerate("3841fz"):
    col = GREEN if ch == "3" else GOLD
    tile(d, gx + i * 84, 420, ch, 72, col)
center(d, 545, "voc\u00ea v\u00ea a compress\u00e3o Blockz10 acontecer a cada abate",
       SANS(24), WHITE)
center(d, 583, "you watch the Blockz10 compression happen with every kill", SANS(19), GREY)
save(img, 8.0)

# ---- Scene 7: timer & score --------------------------------------------------------
img, d = canvas()
center(d, 50, "Tempo e pontua\u00e7\u00e3o / Time and score", SANS_B(36), GOLD)
items = [
    ("\u00bb contagem da fase", "come\u00e7a em 30s e encolhe a cada fase", "starts at 30s, shrinks every phase", GREEN),
    ("\u00bb cron\u00f4metro global", "quanto tempo voc\u00ea sobrevive no total", "how long you survive in total", BLUE),
    ("\u00bb QI CRIPTO", "abate r\u00e1pido vale mais \u00b7 combo at\u00e9 \u00d79", "fast kills are worth more \u00b7 combo up to \u00d79", GOLD),
    ("\u00bb erro", "\u22128 QI \u00b7 \u22122 segundos \u00b7 combo zera", "\u22128 IQ \u00b7 \u22122 seconds \u00b7 combo resets", RED),
]
y = 150
for k, pt, en, col in items:
    d.text((130, y), k, font=SANS_B(28), fill=col)
    d.text((520, y), pt, font=SANS(24), fill=WHITE)
    d.text((520, y + 33), en, font=SANS(18), fill=GREY)
    y += 105
footer(d)
save(img, 8.5)

# ---- Scene 8: ranks -----------------------------------------------------------------
img, d = canvas()
center(d, 60, "No fim, seu QI vira patente / Your IQ becomes a rank", SANS_B(34), GOLD)
ranks = [
    ("1. CRIPT\u00d3GRAFO DA PIR\u00c2MIDE", "220+"),
    ("2. MESTRE DOS BLOCOS", "170+"),
    ("3. CA\u00c7ADOR DE ANAGRAMAS", "130+"),
    ("4. APRENDIZ {e,1}", "100+"),
    ("5. BLOCO G\u00caNESIS", "0+"),
]
y = 160
for name, qi in ranks:
    d.text((280, y), name, font=MONO_B(30), fill=GOLD if "PIR" in name else WHITE)
    d.text((950, y), qi + " QI", font=MONO_B(28), fill=GREEN)
    y += 78
center(d, y + 8, "recorde salvo no navegador / record saved in the browser", SANS(22), GREY)
save(img, 7.0)

# ---- Scene 9: CTA + credits -----------------------------------------------------------
img, d = canvas()
center(d, 150, "Jogue agora / Play now", SANS_B(42), GOLD)
center(d, 250, "elevbit-ai.github.io/blockz10/game.html", MONO_B(32), GREEN)
center(d, 340, "gr\u00e1tis \u00b7 no navegador \u00b7 PT/EN \u00b7 teclado ou clique", SANS(26), WHITE)
center(d, 385, "free \u00b7 in the browser \u00b7 PT/EN \u00b7 keyboard or click", SANS(20), GREY)
center(d, 480, "\u00abBlockz10\u00bb \u2014 block system for creating other functions", MONO(24), DIM)
save(img, 6.0)

img, d = canvas()
center(d, 200, "\u00abBlockz10 Arcade\u00bb", MONO_B(60), GOLD)
center(d, 320, "Criado por / Created by", SANS(26), GREY)
center(d, 365, "Joaquim Pedro de Morais Filho", SANS_B(40), WHITE)
center(d, 450, "j360074@hotmail.com", MONO_B(30), GOLD)
center(d, 515, "\u00a9 2020\u20132026 \u00b7 github.com/elevbit-ai/blockz10", MONO(24), DIM)
save(img, 5.5)

# ---- assemble ---------------------------------------------------------------------------
concat = FRAMES / "list.txt"
with open(concat, "w") as fh:
    for name, dur in frames:
        fh.write(f"file '{name}'\nduration {dur}\n")
    fh.write(f"file '{frames[-1][0]}'\n")

mp4 = OUT / "arcade-explainer.mp4"
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", str(concat),
    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
    "-shortest",
    "-vf", "fps=30,format=yuv420p,scale=1280:720",
    "-c:v", "libx264", "-preset", "slow", "-crf", "22",
    "-c:a", "aac", "-b:a", "64k",
    "-movflags", "+faststart",
    str(mp4),
]
subprocess.run(cmd, check=True, capture_output=True)
print(f"OK {mp4} ({mp4.stat().st_size/1e6:.2f} MB, "
      f"{sum(x for _, x in frames):.1f}s, {len(frames)} frames)")

Image.open(FRAMES / "a0000.png").save(OUT / "arcade-poster.png")
print("poster saved")
