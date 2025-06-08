import numpy as np

# Adds a round key to the state using XOR  
# This step "mixes" the key with the data, making it unique for each round  

def add_round_key(state, round_key):
    return np.bitwise_xor(state, round_key)

# Substitutes each byte in the state using an S-Box  
# This introduces non-linearity, making the encryption stronger and harder to reverse  

def sub_bytes(state):
    sbox = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    ] * 4  # Repeated to cover all 256 possible byte values  
    return np.array([sbox[byte] for byte in state.flatten()]).reshape(4, 4)

# Shifts rows cyclically to the left  
# This step spreads the bytes across columns, improving diffusion  

def shift_rows(state):
    state[1] = np.roll(state[1], -1)
    state[2] = np.roll(state[2], -2)
    state[3] = np.roll(state[3], -3)
    return state

# Simplified version of MixColumns (not a full AES implementation)  
# Normally, this operation blends bytes within each column for better security  

def mix_columns(state):
    return np.array([[state[i][j] for j in range(4)] for i in range(4)])

# Simulates 3 rounds of an AES-like encryption process with debugging output  

def aes_3_rounds(plaintext, round_keys):
    state = plaintext.reshape(4, 4)
    print("Initial State:")
    print(state)
    
    state = add_round_key(state, round_keys[0])
    print("After AddRoundKey (Round 0):")
    print(state)
    
    for i in range(1, 4):
        state = sub_bytes(state)
        print(f"After SubBytes (Round {i}):")
        print(state)
        
        state = shift_rows(state)
        print(f"After ShiftRows (Round {i}):")
        print(state)
        
        if i != 3:  # The last round skips MixColumns  
            state = mix_columns(state)
            print(f"After MixColumns (Round {i}):")
            print(state)
        
        state = add_round_key(state, round_keys[i])
        print(f"After AddRoundKey (Round {i}):")
        print(state)
    
    return state.flatten()

# Simulates an integral attack on the 3-round AES encryption  

def integral_attack():
    # Generate 3 round keys  
    round_keys = [np.random.randint(0, 256, (4, 4), dtype=np.uint8) for _ in range(4)]
    
    # Initialize a zero matrix to accumulate XOR results  
    tmp = np.zeros((4, 4), dtype=np.uint8)
    
    for i in range(256):
        # Create plaintexts where the first byte changes while the rest stay the same  
        plaintext = np.full((4, 4), 0xCC, dtype=np.uint8)
        plaintext[0][0] = i  # Only modifying the first byte  
        
        ciphertext = aes_3_rounds(plaintext, round_keys)
        tmp ^= ciphertext.reshape(4, 4).astype(np.uint8)
    
    print("\nBalanced Property Check (Should be all zeros):")
    print(tmp)
    
    return np.all(tmp == 0)

if __name__ == "__main__":
    result = integral_attack()
    if result:
        print("Oracle is AES 3 rounds.")
    else:
        print("Oracle is a random permutation.")
