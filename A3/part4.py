
"""
part4.py - Differential Attack for Key Recovery and Bruteforce
----------------------------------------------------------------

"""

import random
from part1 import encrypt, generate_keys, split_into_nibbles, inverse_substitute

# Differential parameters
DIFF_INPUT = 0x0020   # The input difference (nibbles: 0, 0, 2, 0)
DIFF_OUTPUT = 0x0020  # Expected output difference for the trail

def gather_attack_data(num_pairs=2**12):
    """
    Collect plaintext-ciphertext pairs for the attack.
    For each pair:
      - Generate a random plaintext 'pt'.
      - Compute 'pt_variant' = pt XOR DIFF_INPUT.
      - Encrypt both with the same key schedule.
    Returns:
      (keys, data_pairs): the 6 round keys and a list of pairs
         [(pt, ct, pt_variant, ct_variant), ...].
    """
    data_pairs = []
    # Use the hard-coded keys from part1
    keys = generate_keys()
    
    for _ in range(num_pairs):
        pt = random.getrandbits(16)
        pt_variant = pt ^ DIFF_INPUT
        ct = encrypt(pt, keys)
        ct_variant = encrypt(pt_variant, keys)
        data_pairs.append((pt, ct, pt_variant, ct_variant))
    return keys, data_pairs

def filter_valid_pairs(pairs):
    """
    Filter out pairs whose ciphertext difference does not match
    the condition: nibbles 0,1,3 are zero and nibble 2 is nonzero.
    (In other words, only nibble index 2 may be active.)
    """
    valid = []
    for pt, ct, pt_variant, ct_variant in pairs:
        diff = ct ^ ct_variant
        nibs = split_into_nibbles(diff)
        # Only nibble at index 2 is allowed to be nonzero.
        if nibs[0] == 0 and nibs[1] == 0 and nibs[3] == 0:
            valid.append((pt, ct, pt_variant, ct_variant))
    return valid

def recover_active_nibble(filtered_pairs):
    """
    Recover the 4-bit value of nibble index 2 in the final round key.
    For each candidate in [0..15], count how many filtered pairs yield
    the expected nibble difference (which is 2, from DIFF_OUTPUT=0x0020)
    after reversing the final round S-box operation.
    """
    counts = [0] * 16
    # The active nibble from DIFF_OUTPUT is the nibble at index 2: 0x2.
    expected_active = (DIFF_OUTPUT >> 4) & 0xF  # => 0x2

    for _, ct, _, ct_variant in filtered_pairs:
        ct_nibs = split_into_nibbles(ct)
        ct_variant_nibs = split_into_nibbles(ct_variant)
        for candidate in range(16):
            # Undo final key XOR and S-box on nibble 2
            v = inverse_substitute(ct_nibs[2] ^ candidate)
            v_var = inverse_substitute(ct_variant_nibs[2] ^ candidate)
            if (v ^ v_var) == expected_active:
                counts[candidate] += 1
    
    # The candidate with the highest count is considered correct.
    recovered_nibble = max(range(16), key=lambda i: counts[i])
    return recovered_nibble, counts

def brute_force_remaining_key_bits(fixed_keys, recovered_nibble, known_pt, known_ct):
    """
    Brute-force the remaining 12 bits of the last round key.
    The last round key is 16 bits, with nibble index 2 fixed to 'recovered_nibble'.
    We iterate over all possible values for nibbles 0,1,3 (2^12 possibilities).
    """
    for candidate in range(2**12):
        nibble0 = (candidate >> 8) & 0xF
        nibble1 = (candidate >> 4) & 0xF
        nibble3 = candidate & 0xF
        # Construct the 16-bit candidate key: (nibble0, nibble1, recovered_nibble, nibble3)
        candidate_key = (nibble0 << 12) | (nibble1 << 8) | (recovered_nibble << 4) | nibble3
        test_keys = fixed_keys + [candidate_key]
        if encrypt(known_pt, test_keys) == known_ct:
            return candidate_key
    return None

if __name__ == "__main__":
    random.seed(42)
    print("=== Differential Attack for Key Recovery ===")
    
    # Step 1: Data Collection
    keys, data_pairs = gather_attack_data()
    print(f"Collected {len(data_pairs)} plaintext-ciphertext pairs.")
    
    # Step 2: Filtering Phase
    valid_pairs = filter_valid_pairs(data_pairs)
    print(f"Number of valid pairs after filtering: {len(valid_pairs)}")
    
    # Step 3: Recover the Active Nibble
    active_nibble, candidate_counts = recover_active_nibble(valid_pairs)
    print("\nCandidate counts for the last round's active nibble (index 2):")
    for cand, count in enumerate(candidate_counts):
        print(f"  Nibble 0x{cand:X}: {count}")
    print(f"Recovered active nibble: 0x{active_nibble:X}")
    
    # Step 4: Bruteforce the Remaining 12 Bits
    if valid_pairs:
        # Use the first filtered pair for bruteforce
        known_pt, known_ct, _, _ = valid_pairs[0]
        # The first 5 keys are fixed from 'keys'
        fixed_round_keys = keys[:5]
        full_last_key = brute_force_remaining_key_bits(fixed_round_keys, active_nibble,
                                                       known_pt, known_ct)
        if full_last_key is not None:
            print(f"\nRecovered final 16-bit key for last round: 0x{full_last_key:04X}")
        else:
            print("\nBrute force did not yield a valid key.")
    else:
        print("No valid pairs available for key recovery.")
