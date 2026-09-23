<div align="center">

# «Blockz10»

### Block system for creating other functions
*Sistema de blocos para criar outras funções*

**[🌐 Site](https://elevbit-ai.github.io/blockz10/) · [🎬 Vídeo explicativo](https://elevbit-ai.github.io/blockz10/#video) · [📜 Especificação](SPECIFICATION.md)**

![Python](https://img.shields.io/badge/Python-3.10+-00e676?style=flat-square&logo=python&logoColor=white&labelColor=060806)
![JavaScript](https://img.shields.io/badge/JavaScript-ES2022-00e676?style=flat-square&logo=javascript&logoColor=white&labelColor=060806)
![Tests](https://img.shields.io/badge/tests-12%2F12%20passing-00e676?style=flat-square&labelColor=060806)
![License](https://img.shields.io/badge/license-MIT-00e676?style=flat-square&labelColor=060806)

Criado por **Joaquim Pedro de Morais Filho** · j360074@hotmail.com · 2020–2026

</div>

---

## O que é / What it is

**PT** — Blockz10 é um sistema conceitual e executável: blocos discretos,
uma estrutura fixa e uma regra aritmética local geram funções completas —
compressão sem perda, loterias criptográficas verificáveis e a pirâmide
conservativa de distribuição de valor **Block 15/5**. Documentado
publicamente desde 2020 e registrado on-chain como NFT.

**EN** — Blockz10 is a conceptual and executable system: discrete blocks,
a fixed structure and a local arithmetic rule generate complete functions —
lossless compression, verifiable crypto lotteries and the conservative
value-distribution pyramid **Block 15/5**. Publicly documented since 2020
and registered on-chain as an NFT.

## Os três pilares / The three pillars

### 1 · Codificação {e, 1} — `eee11 → 311`

Runs de `e` viram um dígito de contagem; `1` permanece literal. Como `e` e
`1` são dígitos hexadecimais válidos, uma string {e,1} de 64 caracteres é
**ao mesmo tempo** uma chave privada Ethereum sintaticamente válida e uma
mensagem comprimível (64 → 54 símbolos na chave publicada, sem perda).

```python
>>> from blockz10 import encode, decode
>>> encode("eee11")
'311'
>>> decode("311")
'eee11'
```

> ⚠ **Segurança:** chaves restritas a {e,1} têm 64 bits de entropia — por
> design, para puzzles e loterias onde a chave deve ser descobrível.
> **Nunca** para custódia de fundos reais.

### 2 · Lottery yourToken — o prêmio que cresce

Carteira-prêmio pública, chave privada encriptada e publicada, senha de 30
caracteres embaralhados. Qualquer um pode aumentar o prêmio depositando
tokens; quem reordenar os caracteres leva tudo. Uma caça ao tesouro
verificável e **colaborativamente inflável**.

### 3 · Block 15/5 — a anti-pirâmide

15 blocos de valor 10 em 5 níveis + bloco de origem (valor 0). Total 150.
Cada nível divide seu total entre níveis receptores — e a soma **sempre
fecha**:

```
6,66 + 6,66 + 29,96 + 33,26 + 63,32 + 10 = 149,86 ≈ 150
```

A diferença de 0,14 é poeira de arredondamento rastreada, não perdida.
Ao contrário da pirâmide financeira clássica: sistema fechado, topo vale
zero, valor flui para a base, recompensa vem da posição estrutural — não
de recrutamento.

```python
>>> from blockz10 import Block155
>>> r = Block155().distribute()
>>> r.total_in, r.conserved, r.dust
(150.0, True, 0.03)
```

## Instalação / Install

```bash
git clone https://github.com/elevbit-ai/blockz10
cd blockz10
python tests/test_blockz10.py     # 12 tests passed.
```

JavaScript (browser ou Node ≥ 18):

```js
import { encode, decode, distribute } from "./src/js/blockz10.js";
```

## Aplicações no mundo real / Real-world applications

| Domínio | Uso |
|---------|-----|
| **Pagamentos** | split determinístico de pagamentos e royalties — conservação = auditabilidade |
| **Tokenomics** | distribuição de tokens em sistema fechado, sem entrada inflacionária |
| **Cripto & jogos** | puzzle wallets, loterias verificáveis, caças ao tesouro on-chain |
| **Codificação** | compressão mnemônica sem perda de chaves de alfabeto restrito |
| **Educação** | modelo mínimo de redes de fluxo conservativo (analogia com CNNs) |

## Estrutura do repositório / Repository layout

```
blockz10/
├── src/blockz10/        # implementação de referência (Python)
│   ├── encoding.py      # codificação {e,1} canônica + geração de chave
│   └── block155.py      # simulador Block 15/5 (regras, conservação, incentivos)
├── src/js/blockz10.js   # implementação espelho (JavaScript ES module)
├── tests/               # 12 testes: round-trip, conservação, regras do blog
├── docs/                # site (GitHub Pages) com demos interativas + vídeo
├── media/               # vídeo explicativo (60s) + poster
├── tools/               # gerador do vídeo (PIL + ffmpeg)
└── SPECIFICATION.md     # especificação formal bilíngue
```

## Origem e registro / Origin & registry

- Blog original: [blockz10.blogspot.com](https://blockz10.blogspot.com) (2020–2025)
- Blog do modelo 15/5: [block155.blogspot.com](https://block155.blogspot.com)
- Registro on-chain: NFT, coleção **Blockz10**, OpenSea
  (contrato `0x495f947276749ce646f68ac8c248420045cb7b5e`)

## Autor / Author

**Joaquim Pedro de Morais Filho**
📧 j360074@hotmail.com

Criador do conceito Blockz10 (2020) e do modelo Block 15/5 (2022).
Todo o conteúdo, conceito e autoria pertencem exclusivamente ao autor.

## Licença / License

[MIT](LICENSE) © 2020–2026 Joaquim Pedro de Morais Filho
