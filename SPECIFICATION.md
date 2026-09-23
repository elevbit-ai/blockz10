# Blockz10 — Formal Specification / Especificação Formal

**Author / Autor:** Joaquim Pedro de Morais Filho · j360074@hotmail.com
**Origin / Origem:** [blockz10.blogspot.com](https://blockz10.blogspot.com) (2020–2025) · [block155.blogspot.com](https://block155.blogspot.com)
**On-chain registry:** NFT, Blockz10 collection, OpenSea (contract `0x495f947276749ce646f68ac8c248420045cb7b5e`)
**Version:** 1.0.0

---

## 0. Core thesis / Tese central

> **PT** — Regras aritméticas mínimas sobre estruturas finitas de blocos geram
> sistemas computacionais e econômicos completos.
>
> **EN** — Minimal arithmetic rules over finite block structures generate
> complete computational and economic systems.

Every Blockz10 construction has four elements:

| # | Element | Definition |
|---|---------|------------|
| 1 | **Block** | minimal unit carrying a value and an address |
| 2 | **Structure** | fixed, finite arrangement of blocks |
| 3 | **Local rule** | counting, division or redistribution |
| 4 | **Function** | what the rule produces over the structure |

---

## 1. The {e, 1} encoding / A codificação {e, 1}

### 1.1 Original definition (2021)

> *"e" (1–9) and "1" (1) equal* `eee11` → `311`

A run of `e` characters is replaced by the digit counting the run; `1`
characters remain literal. Because `e` and `1` are both valid hexadecimal
digits, a 64-character {e,1} string is **simultaneously** a syntactically
valid Ethereum private key and a compressible Blockz10 message.

### 1.2 Canonical lossless form (this specification)

The original compact notation is ambiguous for single-`e` runs (`1` could
mean "one e" or a literal `1`). The canonical form is bijective:

```
E1  a run of n ≥ 2 "e"  →  the digit n (2..9)
E2  runs longer than 9 are split greedily     e×13 → "94"
E3  a single "e"        →  kept as "e"
E4  "1" characters      →  kept literal
```

Decoding inverts E1–E4 exactly. **Theorem (round-trip):** for every
non-empty s ∈ {e,1}⁺, `decode(encode(s)) = s`. Verified by 500 randomized
round-trip tests plus the published 64-char key (compresses 64 → 54).

### 1.3 Entropy statement (normative)

A random {e,1} key of 64 symbols carries **64 bits** of entropy
(2⁶⁴ combinations), not the 256 bits of an unrestricted hex key.
This is **by design**: puzzle and lottery constructions require the key
to be eventually discoverable.

> ⚠ **Normative rule:** {e,1}-restricted keys MUST NOT be used for
> custody of real funds. They are for puzzles, lotteries, demonstrations
> and mnemonic experiments only.

---

## 2. Lottery yourToken (2021)

A prize-bounty construction over the encoding:

1. A prize wallet is created and its address published.
2. Its private key is encrypted; the ciphertext is published openly
   (grid of 5-letter groups).
3. The decryption password is **30 shuffled characters** ("xX blockz10",
   issued as 3 groups of 10).
4. Anyone may **increase the prize** by sending tokens to the wallet.
5. Whoever reorders the 30 characters correctly decrypts the key and
   takes all tokens.

Distinctive property: the prize is *collaboratively inflatable*, creating
a growing incentive over time — a verifiable, self-funding treasure hunt.

---

## 3. Block 15/5 (2020–2022)

### 3.1 Structure

- Level 0: **1 block** holding value **0** (origin block).
- Levels 1–5: level *n* holds *n* blocks of value **10** each.
- **15 value blocks / 5 levels** → the name 15/5. System total = **150**.
- Level colors: 0 grey · 1 yellow · 2 blue · 3 red · 4 orange · 5 green.
- Each block carries a digit 0–5 — an address pointing to a level,
  making the structure self-referential.

### 3.2 Distribution rule

Each level divides its total by a divisor and sends one quota to each
receptor level. Two rule tables are documented by the author:

**DEFAULT_RULES (manuscript table):**

| level | total | division | quota | receptors |
|-------|-------|----------|-------|-----------|
| 0 | 0  | ÷2 | 0     | 1, 2 |
| 1 | 10 | ÷3 | 3.33  | 2, 3, 4 |
| 2 | 20 | ÷2 | 10.00 | 4, 5 |
| 3 | 30 | ÷4 | 7.50  | 1, 2, 4, 5 |
| 4 | 40 | ÷2 | 20.00 | 3, 5 |
| 5 | 50 | ÷3 | 16.66 | 0, 1, 2 |

**EXAMPLE_RULES (published worked example):** identical, except
level 2 = 20 ÷ 3 = **6.66** to receptor levels **3, 4, 5**
(block155.blogspot.com).

### 3.3 Conservation (the defining property)

The original hand-worked round recomposes:

```
6.66 + 6.66 + 29.96 + 33.26 + 63.32 + 10 = 149.86 ≈ 150
```

The 0.14 difference is **rounding dust** from truncating repeating
decimals (6.66 instead of 6.666…). Normatively:

- With exact arithmetic (`precision=None`), Σ received = 150 exactly.
- With 2-decimal truncation, dust MUST be tracked explicitly and
  satisfies 0 ≤ dust < 1. Implementations MUST NOT silently lose dust
  (allocate it to level 0 or to a fee sink).

### 3.4 Threshold incentives (manuscript)

| level | quota threshold | rate |
|-------|-----------------|------|
| 1 | 16.66 | **+15%** |
| 4 | 13.34 | **+10%** |
| 5 | 11.16 | **+10%** |
| 3 | 6.66  | **−10%** |
| 2 | 3.75  | **−10%** |

Additional manuscript identities: `Block 5 = +10% = 63.32 ÷ 5 = 12.66`;
read bottom-up, `5/15 = −10 < 0` (value returns to the origin block).

### 3.5 The anti-pyramid property

In a classic financial pyramid, value flows to the top and the scheme
requires infinite inflow of new participants. Block 15/5 inverts this:

- total value is **fixed** (150) — no inflow required;
- the **top holds zero**; the base holds the largest accumulations;
- rewards derive from **structural position**, not recruitment;
- the sum is **conserved** and auditable in one round.

---

## 4. Applications / Aplicações

| Domain | Use |
|--------|-----|
| Payments | deterministic payment & royalty splitting (conservation = auditability) |
| Tokenomics | closed-system token distribution without inflationary inflow |
| Gaming / crypto | puzzle wallets, verifiable prize lotteries, treasure hunts |
| Encoding | lossless mnemonic compression of restricted-alphabet keys |
| Education | minimal model of conservative flow networks (cf. CNNs: local kernels aggregating over a grid, level by level) |

---

## 5. Open extensions / Extensões abertas

Documented by the author but not yet normative:

1. A general rule selecting receptor sets for arbitrary divisors.
2. Trigger conditions for the ±10% / +15% incentives (when applied,
   per round or per threshold crossing).
3. The convolutional analogy (2025 post): Block 15/5 as a discrete
   value-propagation layer; kernels = distribution rules.

---

© 2020–2026 Joaquim Pedro de Morais Filho. Specification released under
the MIT License. The Blockz10 concept and name are the intellectual
authorship of Joaquim Pedro de Morais Filho, registered on-chain.
