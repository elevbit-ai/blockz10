"""
Blockz10 — Block system for creating other functions.

Reference implementation of the Blockz10 concepts:

  * Blockz10 RLE encoding over the {e, 1} alphabet (canonical lossless form)
  * {e, 1}-restricted Ethereum-style key generation (demonstrative)
  * Block 15/5 conservative value-distribution pyramid

Author : Joaquim Pedro de Morais Filho
Contact: j360074@hotmail.com
Site   : https://elevbit-ai.github.io/blockz10/
"""

from .encoding import encode, decode, generate_key, key_entropy_bits
from .block155 import Block155, DistributionRule, DEFAULT_RULES, EXAMPLE_RULES

__all__ = [
    "encode",
    "decode",
    "generate_key",
    "key_entropy_bits",
    "Block155",
    "DistributionRule",
    "DEFAULT_RULES",
    "EXAMPLE_RULES",
]

__version__ = "1.0.0"
__author__ = "Joaquim Pedro de Morais Filho"
__contact__ = "j360074@hotmail.com"
