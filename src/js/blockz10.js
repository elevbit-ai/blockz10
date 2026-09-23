/**
 * Blockz10 — Block system for creating other functions.
 * Reference JavaScript implementation (mirrors src/blockz10 in Python).
 *
 * Author : Joaquim Pedro de Morais Filho
 * Contact: j360074@hotmail.com
 * License: MIT
 */

const ALPHABET = /^[e1]+$/;

/** Encode an {e,1} string into canonical Blockz10 form. eee11 -> 311 */
export function encode(s) {
  if (!ALPHABET.test(s)) throw new Error("invalid characters for Blockz10 alphabet {e,1}");
  let out = "", i = 0;
  while (i < s.length) {
    const c = s[i];
    let j = i;
    while (j < s.length && s[j] === c) j++;
    let run = j - i;
    if (c === "e") {
      while (run > 9) { out += "9"; run -= 9; }
      out += run === 1 ? "e" : String(run);
    } else {
      out += "1".repeat(run);
    }
    i = j;
  }
  return out;
}

/** Decode a canonical Blockz10 string back to its {e,1} source. */
export function decode(s) {
  if (!/^[e1-9]+$/.test(s)) throw new Error("invalid Blockz10 symbols (expected e, 1-9)");
  let out = "";
  for (const c of s) {
    if (c === "1") out += "1";
    else if (c === "e") out += "e";
    else out += "e".repeat(Number(c));
  }
  return out;
}

/**
 * Generate a random {e,1} string (default 64 chars = syntactically valid
 * ETH private key). WARNING: 64 bits of entropy by design — for puzzle
 * and lottery constructions only, never for storing real funds.
 */
export function generateKey(length = 64) {
  const bytes = new Uint8Array(length);
  (globalThis.crypto ?? require("node:crypto").webcrypto).getRandomValues(bytes);
  return Array.from(bytes, (b) => (b & 1 ? "1" : "e")).join("");
}

/** Entropy in bits of a random key of `length` symbols. */
export function keyEntropyBits(length = 64, alphabetSize = 2) {
  return length * Math.log2(alphabetSize);
}

// ---------------------------------------------------------------- Block 15/5

export const BLOCK_VALUE = 10;
export const LEVELS = [0, 1, 2, 3, 4, 5];

/** Manuscript table: 0/2, 10/3, 20/2, 30/4, 40/2, 50/3. */
export const DEFAULT_RULES = {
  0: { divisor: 2, receptors: [1, 2] },
  1: { divisor: 3, receptors: [2, 3, 4] },
  2: { divisor: 2, receptors: [4, 5] },
  3: { divisor: 4, receptors: [1, 2, 4, 5] },
  4: { divisor: 2, receptors: [3, 5] },
  5: { divisor: 3, receptors: [0, 1, 2] },
};

/** Published worked example: level 2 = 20 -> /3 -> 6.66 to levels 3, 4, 5. */
export const EXAMPLE_RULES = {
  ...DEFAULT_RULES,
  2: { divisor: 3, receptors: [3, 4, 5] },
};

/** Manuscript threshold incentives: level -> [quota, rate]. */
export const INCENTIVES = {
  1: [16.66, +0.15],
  2: [3.75, -0.10],
  3: [6.66, -0.10],
  4: [13.34, +0.10],
  5: [11.16, +0.10],
};

const trunc2 = (x) => Math.trunc(x * 100) / 100;

/** Run one full distribution round. precision=null for exact math. */
export function distribute(rules = DEFAULT_RULES, precision = 2) {
  const received = Object.fromEntries(LEVELS.map((l) => [l, 0]));
  const sent = Object.fromEntries(LEVELS.map((l) => [l, 0]));
  for (const lv of LEVELS) {
    const { divisor, receptors } = rules[lv];
    if (receptors.length !== divisor) throw new Error(`rule ${lv}: divisor/receptor mismatch`);
    let q = (lv * BLOCK_VALUE) / divisor;
    if (precision === 2) q = trunc2(q);
    for (const r of receptors) { received[r] += q; sent[lv] += q; }
  }
  const totalIn = LEVELS.reduce((a, l) => a + l * BLOCK_VALUE, 0);
  const totalOut = Object.values(received).reduce((a, b) => a + b, 0);
  const dust = Math.round((totalIn - totalOut) * 1e10) / 1e10;
  return { received, sent, totalIn, totalOut, dust, conserved: dust >= 0 && dust < 1 };
}
