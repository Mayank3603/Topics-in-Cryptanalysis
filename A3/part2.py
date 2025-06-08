
"""
my_part2.py - S-box Difference Distribution Table (DDT)
--------------------------------------------------------
"""

# S-box definition (16 elements, each in [0..15])
SBOX_TABLE = [
    0x6, 0x4, 0xC, 0x5,
    0x0, 0x7, 0x2, 0xE,
    0x1, 0xF, 0x3, 0xD,
    0x8, 0xA, 0x9, 0xB
]

def build_difference_table():
    """
    Construct the DDT for the SBOX_TABLE.
    difference_table[a][b] = number of x values such that
        SBOX_TABLE[x] XOR SBOX_TABLE[x ^ a] = b.
    """
    size = 16
    difference_table = [[0 for _ in range(size)] for _ in range(size)]
    # For each possible input difference a:
    for a in range(size):
        # Test all x in {0..15} to see how the output difference is distributed.
        for x in range(size):
            output_diff = SBOX_TABLE[x] ^ SBOX_TABLE[x ^ a]
            difference_table[a][output_diff] += 1
    return difference_table

def display_ddt(difference_table):
    """

    """
    header = "Δ_in \\ Δ_out | " + " ".join(f"{col:2X}" for col in range(16))
    print(header)
    print("-" * len(header))
    for delta_in, row in enumerate(difference_table):
        row_str = " ".join(f"{count:2d}" for count in row)
        print(f"      {delta_in:2X}     | {row_str}")

if __name__ == "__main__":
    ddt_result = build_difference_table()
    print("Difference Distribution Table (Counts):")
    display_ddt(ddt_result)
