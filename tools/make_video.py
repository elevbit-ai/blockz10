# Generates media/blockz10-explainer.mp4 frame by frame (PIL + ffmpeg).
# Aesthetic follows the original blog: black background, terminal green.
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
BG = (6, 8, 6)
GREEN = (0, 230, 118)
DIM = (110, 200, 150)
WHITE = (235, 235, 235)
GREY = (150, 150, 150)
YELLOW = (255, 235, 59)
LEVEL_COLORS = {
    0: (189, 189, 189),
    1: (255, 235, 59),
    2: (129, 212, 250),
    3: (244, 67, 54),
    4: (255, 152, 0),
    5: (76, 255, 80),
}

FONTS = r"C:\Windows\Fonts"
MONO_B = lambda s: ImageFont.truetype(os.path.join(FONTS, "consolab.ttf"), s)
MONO = lambda s: ImageFont.truetype(os.path.join(FONTS, "consola.ttf"), s)
SANS = lambda s: ImageFont.truetype(os.path.join(FONTS, "segoeui.ttf"), s)
SANS_B = lambda s: ImageFont.truetype(os.path.join(FONTS, "segoeuib.ttf"), s)

OUT = Path(__file__).resolve().parents[1] / "media"
FRAMES = OUT / "_frames"
FRAMES.mkdir(parents=True, exist_ok=True)

frames: list[tuple[str, float]] = []  # (filename, duration seconds)
_n = 0


def canvas():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def save(img, dur):
    global _n
    name = f"f{_n:04d}.png"
    img.save(FRAMES / name)
    frames.append((name, dur))
    _n += 1


def center(d, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)


def footer(d):
    center(d, H - 46, "Joaquim Pedro de Morais Filho  ·  j360074@hotmail.com", MONO(20), DIM)


# ---- Scene 1: title -------------------------------------------------------
img, d = canvas()
center(d, 200, "\u00abBlockz10\u00bb", MONO_B(96), GREEN)
center(d, 340, "Block system for creating other functions", SANS(36), WHITE)
center(d, 400, "Sistema de blocos para criar outras fun\u00e7\u00f5es", SANS(28), GREY)
center(d, 500, "por Joaquim Pedro de Morais Filho \u00b7 desde 2020", SANS(26), DIM)
save(img, 4.5)

# ---- Scene 2: the idea ----------------------------------------------------
img, d = canvas()
center(d, 80, "A ideia / The idea", SANS_B(40), GREEN)
lines = [
    ("BLOCO", "unidade m\u00ednima com valor e endere\u00e7o", "minimal unit with value and address"),
    ("ESTRUTURA", "arranjo fixo e finito de blocos", "fixed, finite arrangement of blocks"),
    ("REGRA LOCAL", "contagem \u00b7 divis\u00e3o \u00b7 redistribui\u00e7\u00e3o", "counting \u00b7 division \u00b7 redistribution"),
    ("FUN\u00c7\u00c3O", "o que emerge da regra sobre a estrutura", "what the rule creates over the structure"),
]
y = 190
for k, pt, en in lines:
    d.text((150, y), k, font=MONO_B(30), fill=YELLOW)
    d.text((470, y), pt, font=SANS(28), fill=WHITE)
    d.text((470, y + 38), en, font=SANS(22), fill=GREY)
    y += 105
footer(d)
save(img, 6.5)

# ---- Scene 3: encoding ----------------------------------------------------
img, d = canvas()
center(d, 70, "Codifica\u00e7\u00e3o Blockz10 / Blockz10 encoding", SANS_B(40), GREEN)
center(d, 165, "alfabeto {e, 1} \u2014 ambos d\u00edgitos hexadecimais v\u00e1lidos", SANS(26), GREY)
center(d, 250, "e e e 1 1", MONO_B(64), WHITE)
center(d, 340, "\u2193", MONO_B(48), GREEN)
center(d, 400, "3 1 1", MONO_B(64), GREEN)
center(d, 505, 'runs de "e" viram contagem \u00b7 "1" permanece literal', SANS(26), WHITE)
center(d, 550, 'runs of "e" become a count \u00b7 "1" stays literal', SANS(22), GREY)
footer(d)
save(img, 6.0)

img, d = canvas()
center(d, 70, "Uma chave, duas leituras / One key, two readings", SANS_B(38), GREEN)
key = "111e1ee1e1eeeee11111ee1111e11e11111e"
key2 = "11e1e111e11ee11e1111ee1e1eee"
enc = "111e121e151111121111e11e11111e"
enc2 = "11e1e111e11211e111121e13"
d.text((115, 190), "chave ETH v\u00e1lida / valid ETH key (64):", font=SANS(24), fill=WHITE)
d.text((115, 235), key, font=MONO(30), fill=WHITE)
d.text((115, 272), key2, font=MONO(30), fill=WHITE)
d.text((115, 360), "forma Blockz10 / Blockz10 form (54):", font=SANS(24), fill=GREEN)
d.text((115, 405), enc, font=MONO(30), fill=GREEN)
d.text((115, 442), enc2, font=MONO(30), fill=GREEN)
d.text((115, 530), "compress\u00e3o sem perda \u00b7 lossless \u00b7 64 \u2192 54 s\u00edmbolos", font=SANS(26), fill=YELLOW)
footer(d)
save(img, 6.5)

# ---- Scene 4: crypto application ------------------------------------------
img, d = canvas()
center(d, 70, "Aplica\u00e7\u00e3o: puzzle wallets & loterias", SANS_B(40), GREEN)
center(d, 125, "Application: puzzle wallets & prize lotteries", SANS(26), GREY)
pts = [
    "carteira-pr\u00eamio p\u00fablica com chave encriptada",
    "public prize wallet, encrypted private key",
    "",
    "30 caracteres embaralhados abrem a carteira",
    "30 shuffled characters unlock the wallet",
    "",
    "qualquer um pode aumentar o pr\u00eamio com tokens",
    "anyone can grow the prize by adding tokens",
]
y = 200
for i, t in enumerate(pts):
    if t:
        col = WHITE if (i % 3 == 0) else GREY
        f = SANS(28) if (i % 3 == 0) else SANS(22)
        center(d, y, t, f, col)
        y += 44 if i % 3 == 0 else 40
    else:
        y += 22
center(d, y + 18, "entropia calibrada: descobr\u00edvel por design \u2014 nunca para custódia",
       SANS(24), YELLOW)
footer(d)
save(img, 7.0)

# ---- Scene 5: pyramid build animation --------------------------------------
PYR = {0: 1, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
CELL, GAP = 74, 14
TOPY = 150


def draw_pyramid(d, upto_level, upto_block, labels=True):
    for lv in range(6):
        n = PYR[lv]
        y = TOPY + lv * (CELL + GAP)
        x0 = 320
        for b in range(n):
            if lv > upto_level or (lv == upto_level and b > upto_block):
                continue
            x = x0 + b * (CELL + GAP)
            col = LEVEL_COLORS[lv]
            d.rectangle([x, y, x + CELL, y + CELL], outline=col, width=5)
            d.rectangle([x - 3, y - 3, x + CELL + 3, y + CELL + 3], outline=(255, 255, 255), width=1)
            val = "0" if lv == 0 else "10"
            f = MONO_B(26)
            w = d.textlength(val, font=f)
            d.text((x + (CELL - w) / 2, y + CELL / 2 - 16), val, font=f, fill=GREEN)
        if labels and lv <= upto_level:
            d.text((240, y + CELL / 2 - 16), str(lv), font=MONO_B(28), fill=LEVEL_COLORS[lv])


order = [(lv, b) for lv in range(6) for b in range(PYR[lv])]
for i, (lv, b) in enumerate(order):
    img, d = canvas()
    center(d, 50, "\u00abBlock 15/5\u00bb", MONO_B(48), GREEN)
    draw_pyramid(d, lv, b)
    d.text((880, 200), "n\u00edvel n guarda n\u00d710", font=SANS(26), fill=WHITE)
    d.text((880, 240), "level n holds n\u00d710", font=SANS(21), fill=GREY)
    shown = sum(min(PYR[l], b + 1 if l == lv else PYR[l]) for l in range(lv + 1))
    d.text((880, 320), f"blocos / blocks: {i + 1}", font=MONO_B(30), fill=YELLOW)
    save(img, 0.28 if i < len(order) - 1 else 1.2)

img, d = canvas()
center(d, 50, "\u00abBlock 15/5\u00bb", MONO_B(48), GREEN)
draw_pyramid(d, 5, 4)
d.text((880, 190), "15 blocos \u00b7 5 n\u00edveis", font=SANS_B(28), fill=WHITE)
d.text((880, 235), "15 blocks \u00b7 5 levels", font=SANS(22), fill=GREY)
d.text((880, 300), "topo vale 0", font=SANS(26), fill=WHITE)
d.text((880, 340), "top holds 0", font=SANS(21), fill=GREY)
d.text((880, 410), "TOTAL = 150", font=MONO_B(38), fill=GREEN)
save(img, 4.0)

# ---- Scene 6: distribution math -------------------------------------------
img, d = canvas()
center(d, 60, "Distribui\u00e7\u00e3o conservativa / Conservative distribution", SANS_B(36), GREEN)
rows = [
    ("n\u00edvel 1", "10 \u00f7 3", "3,33"),
    ("n\u00edvel 2", "20 \u00f7 3", "6,66  \u2192 receptores 3, 4, 5"),
    ("n\u00edvel 3", "30 \u00f7 4", "7,50"),
    ("n\u00edvel 4", "40 \u00f7 2", "20,00"),
    ("n\u00edvel 5", "50 \u00f7 3", "16,66"),
]
y = 160
for a, b, c in rows:
    d.text((180, y), a, font=MONO_B(28), fill=WHITE)
    d.text((400, y), b, font=MONO_B(28), fill=YELLOW)
    d.text((620, y), c, font=MONO_B(28), fill=GREEN)
    y += 58
d.line([160, y + 10, 1120, y + 10], fill=(180, 40, 40), width=4)
d.text((180, y + 34), "6,66+6,66+29,96+33,26+63,32+10 =", font=MONO_B(30), fill=WHITE)
d.text((860, y + 34), "149,86 \u2248 150", font=MONO_B(34), fill=GREEN)
d.text((180, y + 92), "o valor circula e se conserva \u00b7 value flows and is conserved",
       font=SANS(24), fill=GREY)
footer(d)
save(img, 8.0)

# ---- Scene 7: real-world applications --------------------------------------
img, d = canvas()
center(d, 70, "Aplica\u00e7\u00f5es / Applications", SANS_B(40), GREEN)
apps = [
    ("Split de pagamentos e royalties", "deterministic payment & royalty splitting"),
    ("Tokenomics de sistema fechado", "closed-system tokenomics \u2014 no infinite inflow"),
    ("Anti-pir\u00e2mide: valor flui para a base", "anti-pyramid: value flows to the base"),
    ("Puzzle wallets e ca\u00e7as ao tesouro", "puzzle wallets & crypto treasure hunts"),
    ("Compress\u00e3o mnem\u00f4nica de chaves", "mnemonic key compression"),
]
y = 180
for pt, en in apps:
    d.text((190, y), "\u25a0", font=SANS(24), fill=GREEN)
    d.text((240, y), pt, font=SANS_B(28), fill=WHITE)
    d.text((240, y + 38), en, font=SANS(22), fill=GREY)
    y += 92
footer(d)
save(img, 7.0)

# ---- Scene 8: credits -------------------------------------------------------
img, d = canvas()
center(d, 180, "\u00abBlockz10\u00bb", MONO_B(72), GREEN)
center(d, 300, "Criado por / Created by", SANS(26), GREY)
center(d, 345, "Joaquim Pedro de Morais Filho", SANS_B(40), WHITE)
center(d, 430, "j360074@hotmail.com", MONO_B(30), GREEN)
center(d, 500, "github.com/elevbit-ai/blockz10", MONO(26), DIM)
center(d, 545, "\u00a9 2020\u20132026 \u00b7 registrado on-chain via NFT \u00b7 OpenSea", SANS(22), GREY)
save(img, 6.0)

# ---- assemble with ffmpeg ---------------------------------------------------
concat = FRAMES / "list.txt"
with open(concat, "w") as f:
    for name, dur in frames:
        f.write(f"file '{name}'\nduration {dur}\n")
    f.write(f"file '{frames[-1][0]}'\n")  # concat demuxer quirk: repeat last

mp4 = OUT / "blockz10-explainer.mp4"
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
size = mp4.stat().st_size
print(f"OK {mp4} ({size/1e6:.2f} MB, {sum(d for _, d in frames):.1f}s, {len(frames)} frames)")

# poster for the site
poster = Image.open(FRAMES / "f0000.png")
poster.save(OUT / "poster.png")
print("poster saved")
