
"""
part1.py - Toy Cipher Implementation
--------------------------------------

"""

import random

# Define the substitution box (S-box) for our cipher.
S_BOX = [0x6, 0x4, 0xC, 0x5,
         0x0, 0x7, 0x2, 0xE,
         0x1, 0xF, 0x3, 0xD,
         0x8, 0xA, 0x9, 0xB]

# Compute the inverse S-box for decryption or differential analysis.
S_INV = [0] * 16
for index, value in enumerate(S_BOX):
    S_INV[value] = index

# Permutation table to shuffle 16-bit data.
P_BOX = [0, 4, 8, 12,
         1, 5, 9, 13,
         2, 6, 10, 14,
         3, 7, 11, 15]

def substitute(nibble):
    """Apply the S-box to a 4-bit nibble."""
    return S_BOX[nibble]

def inverse_substitute(nibble):
    """Apply the inverse S-box to recover the original nibble."""
    return S_INV[nibble]

def permute(bit_list):
    """Permute a 16-element list of bits according to the fixed P_BOX."""
    permuted = [0] * 16
    for i, bit in enumerate(bit_list):
        permuted[P_BOX[i]] = bit
    return permuted

def int_to_bitlist(value, bits=16):
    """Convert an integer to a list of bits (MSB first)."""
    return [(value >> i) & 1 for i in range(bits - 1, -1, -1)]

def bitlist_to_int(bit_list):
    """Convert a list of bits (MSB first) back into an integer."""
    value = 0
    for bit in bit_list:
        value = (value << 1) | bit
    return value

def split_into_nibbles(num):
    """Break a 16-bit number into 4 nibbles (MSB first)."""
    return [(num >> (4 * (3 - i))) & 0xF for i in range(4)]

def combine_nibbles(nibble_list):
    """Combine 4 nibbles into a single 16-bit integer."""
    value = 0
    for nib in nibble_list:
        value = (value << 4) | nib
    return value

def generate_keys():
    """
    Generate six 16-bit round keys for the 5-round cipher.
    The random generation is retained, but we override the result
    with hard-coded keys.
    """
    # Original random key generation (still present but overridden):
    _ = [random.getrandbits(16) for _ in range(6)]
    
    # Hard-coded keys (override):
    return [0x1111, 0x2222, 0x3333, 0x4444, 0x5555, 0x6666]

def encrypt(plaintext, keys):
    """
    Encrypt a 16-bit plaintext using a 5-round toy cipher.
    The rounds consist of key mixing, S-box substitution, and a permutation (except in the last round).
    """
    state = plaintext
    # First four rounds: mix, substitute, permute.
    for round_index in range(4):
        state ^= keys[round_index]  # Key mixing
        nibbles = split_into_nibbles(state)  # Split into 4-bit pieces
        nibbles = [substitute(nib) for nib in nibbles]  # Apply S-box substitution
        temp = combine_nibbles(nibbles)  # Recombine nibbles
        bits = int_to_bitlist(temp)      # Convert to bits for permutation
        bits = permute(bits)            # Permute the bits
        state = bitlist_to_int(bits)     # Convert back to integer

    # Last round: mix, substitute, and final key mixing (no permutation).
    state ^= keys[4]
    nibbles = split_into_nibbles(state)
    nibbles = [substitute(nib) for nib in nibbles]
    state = combine_nibbles(nibbles)
    return state ^ keys[5]

if __name__ == "__main__":
    random.seed(42)  # For reproducible results
    round_keys = generate_keys()
    print(" Round Keys:")
    for i, key in enumerate(round_keys):
        print(f"  Key {i}: 0x{key:04X}")
    
    # Example encryption
    plain = 0x1234
    cipher = encrypt(plain, round_keys)
    print(f"\nPlaintext:  0x{plain:04X}")
    print(f"Ciphertext: 0x{cipher:04X}")
