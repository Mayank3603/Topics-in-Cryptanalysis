
"""
part3.py - Differential Trail Exploration

"""

def compute_normalized_ddt():
    """
    Build the normalized Difference Distribution Table (DDT) for the S-box.
    Each count is divided by 16 (the number of possible input values) to get a probability.
    """
    # S-box definition (same as in Part 1)
    SBOX = [0x6, 0x4, 0xC, 0x5,
            0x0, 0x7, 0x2, 0xE,
            0x1, 0xF, 0x3, 0xD,
            0x8, 0xA, 0x9, 0xB]
    table_size = 16
    ddt = [[0] * table_size for _ in range(table_size)]
    for delta_in in range(table_size):
        for x in range(table_size):
            output_diff = SBOX[x] ^ SBOX[x ^ delta_in]
            ddt[delta_in][output_diff] += 1
    # Normalize each entry by dividing by 16
    normalized_ddt = [[count / 16.0 for count in row] for row in ddt]
    return normalized_ddt

def int_to_bitlist(num, width=16):
    """Convert an integer to a list of bits (MSB first)."""
    return [(num >> (width - 1 - i)) & 1 for i in range(width)]

def bitlist_to_int(bitlist):
    """Convert a list of bits (MSB first) back into an integer."""
    result = 0
    for bit in bitlist:
        result = (result << 1) | bit
    return result

def apply_pbox(input_val):
    """
    Permute a 16-bit integer using the fixed P-box.
    The permutation mapping is hard-coded.
    """
    PBOX = [0, 4, 8, 12,
            1, 5, 9, 13,
            2, 6, 10, 14,
            3, 7, 11, 15]
    bits = int_to_bitlist(input_val)
    permuted_bits = [0] * 16
    for idx, pos in enumerate(PBOX):
        permuted_bits[pos] = bits[idx]
    return bitlist_to_int(permuted_bits)

def split_nibbles(value):
    """Split a 16-bit integer into four 4-bit nibbles (MSB first)."""
    return [(value >> (4 * (3 - i))) & 0xF for i in range(4)]

def merge_nibbles(nibble_list):
    """Combine a list of 4 nibbles into a 16-bit integer."""
    combined = 0
    for nib in nibble_list:
        combined = (combined << 4) | nib
    return combined

def explore_differential_trail(init_diff, rounds=4):
    """
    Explore a differential trail starting from an initial 16-bit difference.
    
    The approach processes each round as follows:
      1. Break the current difference into four 4-bit nibbles.
      2. For each nibble:
         - If inactive (zero), the output nibble stays 0.
         - Otherwise, select the output difference with the highest probability from the DDT.
      3. Combine the output nibbles into a 16-bit value, then apply the P-box.
      4. Multiply the round probability into the cumulative probability.
    
    Returns:
      final_difference: The resulting 16-bit difference after all rounds.
      cumulative_probability: The product of probabilities over all rounds.
      trail_details: A list of tuples (round_difference, round_probability) per round.
    """
    normalized_ddt = compute_normalized_ddt()
    current_diff = init_diff
    cumulative_probability = 1.0
    trail_details = []  # Records output difference and probability for each round

    # Process each round iteratively.
    for rnd in range(1, rounds + 1):
        input_nibbles = split_nibbles(current_diff)
        output_nibbles = [0] * 4
        round_probability = 1.0
        
        # Process each nibble independently.
        for i in range(4):
            nib_val = input_nibbles[i]
            if nib_val == 0:
                # Inactive S-box: no change and probability remains 1.
                output_nibbles[i] = 0
            else:
                best_output = 0
                best_prob = 0.0
                # Choose the output difference with the highest probability.
                for candidate in range(16):
                    candidate_prob = normalized_ddt[nib_val][candidate]
                    if candidate_prob > best_prob:
                        best_prob = candidate_prob
                        best_output = candidate
                output_nibbles[i] = best_output
                round_probability *= best_prob
        
        combined_output = merge_nibbles(output_nibbles)
        permuted_output = apply_pbox(combined_output)
        cumulative_probability *= round_probability
        trail_details.append((permuted_output, round_probability))
        current_diff = permuted_output

    return current_diff, cumulative_probability, trail_details

if __name__ == "__main__":
    print("Differential Trail Exploration (4 rounds):\n")
    best_trail = None
    max_probability = 0.0

    # Evaluate trails for each nonzero initial difference (from 1 to 15)
    for init in range(1, 16):
        final_diff, trail_prob, details = explore_differential_trail(init, rounds=4)
        # print(f"Initial Diff: 0x{init:04X} -> Final Diff: 0x{final_diff:04X}, Overall Prob: {trail_prob:.6f}")
        if trail_prob > max_probability:
            max_probability = trail_prob
            best_trail = (init, final_diff, details)

    if best_trail:
        init_val, final_val, trail_info = best_trail
        print("\nBest Differential Trail:")
        print(f"  Starting Difference: 0x{init_val:04X}")
        for round_num, (diff_val, round_prob) in enumerate(trail_info, start=1):
            print(f"  Round {round_num}: Diff = 0x{diff_val:04X}, Round Prob = {round_prob:.6f}")
        print(f"Overall Trail Probability: {max_probability:.6f}")
