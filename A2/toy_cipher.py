import random # Importing random to generate 32 bit string for Part-3

# S-BOX same as AES
Sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# Function to add Round Key
def AR(state, key):
    return [state[i] ^ key[i] for i in range(len(state))]

# Function to add S-box Layer
def SB(state):
    return [Sbox[i] for i in state]

# Function for Linear Mixing as described in the Assignment
def LM(state):
    xor_of_all = state[0] ^ state[1] ^ state[2] ^ state[3]
    return [xor_of_all ^ i for i in state]

# Function for Single Encryption Round
def Enc_Round(state, key):
    state_out = AR(state, key)
    state_out = SB(state_out)
    state_out = LM(state_out)
    return state_out


# Part-1 : Implementaion of the Toy Cipher

# Function for the encrption of the Toy Cipher
def TC1_Enc(Plaintext, key, rounds=10):
    Cipher = Plaintext
    for _ in range(rounds):
        Cipher = Enc_Round(Cipher, key)
    return Cipher



# Part-2 : Exhaustively Searchig for the key

# Function that will take the input as plaintext and ciphertext and output the exhaustive key using brute force 

def exhaustive_search(plaintexts, ciphertexts):
    # To reduce the complexity: Fixing  the first byte of the exhaustive key key to 0x00 [0x00 , ? , ? , ?]
    for byte1 in range(256):
        for byte2 in range(256):
            for byte3 in range(256):
                # Construct a candidate key
                candidate_key = [0x00, byte1, byte2, byte3]

                #  Condition to check this key works for all plaintext-ciphertext pairs 
                is_key_valid = True
                for plaintext, ciphertext in zip(plaintexts, ciphertexts):
                    if TC1_Enc(plaintext, candidate_key) != ciphertext:
                        #Check if key found or not
                        is_key_valid = False
                        break

                # If a valid key is found, return it
                if is_key_valid:
                    return candidate_key

    # If no key has been found we return None
    return None


# Function to generate 32-bit random string for Part-3 
def random_32_bit():
    return [random.randint(0, 255) for b in range(4)]

# Part-3 : TMTO Attack for key recovery

# Function to make the preprocess table in the TMTO attack (Offine Phase) 
def Offline_phase(m, chain_length):

    # This Table will store Starting point and Ending point of chains as a single tuple
    # eg -> table = [(sp1,ep1), {sp2,ep2}...... {spn, epn}]
    table = []

    for _ in range(m):
        sp = random_32_bit()
        tmp = sp.copy()
        for _ in range(chain_length - 1):
            tmp = TC1_Enc(tmp, tmp) 
        ep = tmp
        table.append((sp, ep))
    return table
# Function to search the table (precomputed table of the TMTO attack) -- (Online Phase)
def Online_phase(table, plaintext, ciphertext, chain_length):

    for sp, ep in table:
        tmp = sp.copy()
        for i in range(chain_length):
            if TC1_Enc(plaintext, tmp) == ciphertext:
                return tmp
            tmp = TC1_Enc(tmp, tmp)
    return None


# Main function to test all the parts
if __name__ == "__main__":


    # Test case of 32-bit plaintext and key split into 4 bytes to test Toy Cipher-----Part-1
    plaintext = [0x12, 0x34, 0x56, 0x78]
    key = [0x9A, 0xBC, 0xDE, 0xF0]

    # Perform encryption
    ciphertext = TC1_Enc(plaintext, key)

    # Printing the Toy-Cipher Results---- Part-I
    print(f"Plaintext:{plaintext}")
    print()
    print(f"Key:{key}")
    print()
    print(f"Ciphertext:{ciphertext}")
    print()
    print("--------------------------------------------------------------------")


    # Test case to test the Exhaustive Search Algorithm ----Part-2
    plaintexts = [[0x00, 0x00, 0x00, 0x00], [0x01, 0x02, 0x03, 0x04]]
    ciphertexts = [[180, 31, 145, 240], [228, 99, 105, 79]]

    # Calling the function that will implement the brute force algorithm to search the key--------Part-2
    exhaustive_key = exhaustive_search(plaintexts, ciphertexts)
    print()
    if exhaustive_key:
        #Print the output/key for the Part-2 (Exhaustive key Search)
        print(f"The key has been found using exhaustive Search")
        print(f"The found key is : {exhaustive_key}")
        print("----------------------------------------------------------------")
    else:
        print("Key not found.")


    # Part -3 : TMTO attack for key recovery.
    m = 2**16  # Number of chains
    chain_length = 2**16  # Length of each chain

    # First step is to generate the precomputed table.
    print("Step -1 : Generating the precomputed table.")
    table = Offline_phase(m, chain_length)

    # Displaying the first few chains of the precompute table (10)
    print("Precomputed Table (SP -> EP):")
    for sp, ep in table[:10]:  
        print("Start Points")
        print(sp)
        print("End Points")
        print(ep)
    # Test case for TMTO attack for key recovery ---- Part-3 of the assignment
    plaintext = [18, 52, 86, 120]
    ciphertext = [86, 116, 35, 75]

    # The Second step is Search the table 
    print("Searching for the key...")
    TMTO_key = Online_phase(table, plaintext, ciphertext, chain_length)
    if TMTO_key:
        print(f"The key has been found using TMTO attack")
        print(f"The found key is : {TMTO_key}")
    else:
        print("Key not found.")
