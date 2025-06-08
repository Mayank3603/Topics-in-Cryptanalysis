from tables import get_s_box_value, get_inv_s_box_value, get_r_con_value

# Function to convert matrix format back to bytes output 
def convert_matrix_to_bytes(matrix):
    byte_list = []
    for row in matrix:
        for byte in row:
            byte_list.append(byte)
    return bytes(byte_list)


# Function to converet bytes format to matrix format to do all set of operations
def convert_bytes_to_matrix(key):
    matrix = []
    for i in range(0, len(key), 4):
        temp_row = []
        for j in range(4):
            temp_row.append(key[i + j])
        matrix.append(temp_row)
    return matrix


# Function Used in key expansion
def rotate_word_left(word):
    
    return word[1:]+[word[0]]

# Function used to optimise the mix column function 
def multiply_by_two(a):
    if (a & 0x80):
        result = ((a << 1) ^ 0x1B) & 0xFF
    else:
        result = (a << 1)
    return result

# Function used to do xor of two arrays in key expansion 
def xor_two_byte_arrays(a, b):

    length = len(a)
    x = []
    for i in range(length):
        x.append(a[i] ^ b[i])
    return x 

# Function to exapnd key 
def expand_key(key, rounds):
     # Convert key into a matrix and initialize expanded key

    key_matrix = convert_bytes_to_matrix(key)
    Nk = len(key) // 4   # Key length in words
    Nb = 4 
    expanded_key = key_matrix[:]

    i = Nk
    while len(expanded_key) < Nb * (rounds + 1):
        temp = expanded_key[-1][:]
       
        if i % Nk == 0:

            temp = rotate_word_left(temp)
            temp = [get_s_box_value(byte // 0x10, byte % 0x10) for byte in temp]
            temp[0] ^= get_r_con_value(i // Nk)

        elif Nk > 6 and i % Nk == 4:
            # Substitute word for 256-bit keys
            temp = [get_s_box_value(byte // 0x10, byte % 0x10) for byte in temp]
        # XOR with the word Nk positions earlier

        temp = xor_two_byte_arrays(temp, expanded_key[-Nk])

        expanded_key.append(temp)
        i += 1
    return expanded_key


# Function to apply the round key
def apply_round_key(state,key):
    # XOR state with the round key
    Nk=4
    state=[[state[i][j]^key[i][j] for j in range(Nk)] for i in range(Nk)]
    return state

#Function to Substitute bytes using the S-Box
def substitute_bytes(s):
    new_state = []
    for i in range(4):
        temp_row = []
        for j in range(4):
            temp_row.append(get_s_box_value(s[i][j] // 0x10, s[i][j] % 0x10))
        new_state.append(temp_row)
    return new_state
#Function to Substitute bytes using the inverse S-Box
def inverse_substitute_bytes(state):
    
    new_state = []
    for i in range(4):
        temp_row = []
        for j in range(4):
            temp_row.append(get_inv_s_box_value(state[i][j] // 0x10, state[i][j] % 0x10))
        new_state.append(temp_row)
    return new_state

#Function to transpose the matrix
def transpose_matrix(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

#Function to shift rows left 
def shift_rows_left(state):
    
    state=transpose_matrix(state)
    state[1] = [state[1][1], state[1][2], state[1][3], state[1][0]] # Left shifting the rows with the offset
    state[2] = [state[2][2], state[2][3], state[2][0], state[2][1]]
    state[3] = [state[3][3], state[3][0], state[3][1], state[3][2]]
    return state
#Function to shift rows right
def shift_rows_right(state):
    state=transpose_matrix(state)
    state[1] = [state[1][3], state[1][0], state[1][1], state[1][2]]# Right shifting the rows with the offset
    state[2] = [state[2][2], state[2][3], state[2][0], state[2][1]]
    state[3] = [state[3][1], state[3][2], state[3][3], state[3][0]]
    return state


#Function to apply mix column function  (in which we mulitiple the output from shift rows with a matrix during encrption)
def mix_column_values(state):
  
    state = transpose_matrix(state)
    new_state = []

    for column in state:

        t = column[0] ^ column[1] ^ column[2] ^ column[3]
        new_column = [
            column[0] ^ t ^ multiply_by_two(column[0] ^ column[1]),
            column[1] ^ t ^ multiply_by_two(column[1] ^ column[2]),
            column[2] ^ t ^ multiply_by_two(column[2] ^ column[3]),
            column[3] ^ t ^ multiply_by_two(column[3] ^ column[0]),
        ]
        new_state.append(new_column)

    return new_state

#Function to apply inverse mix column function  (in which we mulitiple the output from shift rows with a matrix during decrption)

def inverse_mix_columns(state):
    for i in range(4):
        x = multiply_by_two(state[i][0] ^ state[i][2])
        y = multiply_by_two(state[i][1] ^ state[i][3])
        state[i][0] ^= multiply_by_two(x)
        state[i][1] ^= multiply_by_two(y)
        state[i][2] ^= multiply_by_two(x)
        state[i][3] ^= multiply_by_two(y)

    state=transpose_matrix(state)
    state = mix_column_values(state)
    return state

#Function for debugging (printing the expanded key)
def print_expanded_key(expanded_key):
    for row in expanded_key:
        print(" ".join(f"{byte:02x}" for byte in row))


#Function for encryption ( encrypt the plaintext using the AES)
def perform_encryption(plaintext, key, rounds):
    state = convert_bytes_to_matrix(plaintext)
   
    expanded_key = expand_key(key, rounds)

    state = apply_round_key(state, expanded_key[0:4])
    
    
    for round in range(1, rounds):
        state = substitute_bytes(state)
        state = shift_rows_left(state)
        state = mix_column_values(state)        
        state = apply_round_key(state, expanded_key[4 * round:4 * (round + 1)])
    

    state = substitute_bytes(state)
    state = shift_rows_left(state)
    state = apply_round_key(transpose_matrix(state), expanded_key[rounds * 4:(rounds + 1) * 4])
    return state

#Function to print the byte code into matirx format 
def format_bytes_as_matrix(byte_array):

    matrix = [byte_array[i:i + 4] for i in range(0, len(byte_array), 4)]
    transposed = list(zip(*matrix))  
    return "\n".join([" ".join([f"{byte:02x}" for byte in row]) for row in transposed])


#Function for decryption ( decrypt the ciphertext using the AES)

def perform_decryption(ciphertext, key, rounds):
   

    state = ciphertext
    expanded_key = expand_key(key, rounds)
 
    state = apply_round_key(state, expanded_key[rounds * 4:(rounds + 1) * 4])
    state = shift_rows_right(state)
    state = inverse_substitute_bytes(state)

    

    for round in range(rounds - 1, 0, -1):
        state=transpose_matrix(state)
        state = apply_round_key(state, expanded_key[round * 4:(round + 1) * 4])        
        state = inverse_mix_columns(state)
        state = shift_rows_right(state)
        state = inverse_substitute_bytes((state))
      

    state=transpose_matrix(state)
    state = apply_round_key(state, expanded_key[0:4])
    return state

 # High-level function to perform AES encryption and decryption

def execute_aes(pt, k, rounds):
    print("\n-----------------------------------------------------\n")
    key = bytes.fromhex(k)

    print("Input (Hex):", pt)
    print(f"The key used for AES (Hex): {k}")
 
    print("\nStarting Encryption...\n")
    
    # Divide the plaintexts into blocks of 128 bytpes 
    blocks = [pt[i:i + 32] for i in range(0, len(pt), 32)]
    ciphertext_blocks = [] # store the ciphertext in this

    # Function to encrpyion each blcok of plaintext
    for block_index, block in enumerate(blocks):
        plaintext = bytes.fromhex(block)
        print(f"Processing Block {block_index + 1}:")
        print("Plaintext (Hex):", block)

        ciphertext = perform_encryption(plaintext, key, rounds)
        ciphertext_bytes = convert_matrix_to_bytes(ciphertext)

        print("Ciphertext in Hex (4x4 Matrix):")
        print(format_bytes_as_matrix(ciphertext_bytes))
        ciphertext_blocks.append(ciphertext)
        print("\n")

    print("\n-----------------------------------------------------\n")
     
    print("Starting Decryption...\n")
    
    decrypted_blocks = [] #store the decrpted blocks in this

    for block_index, ciphertext in enumerate(ciphertext_blocks):
        
        print(f"Processing Block {block_index + 1}:")
        print("Ciphertext (Hex):", block)

        plaintext = perform_decryption(ciphertext, key, rounds)
        plaintext_bytes = convert_matrix_to_bytes(plaintext)

        print("Decrypted Plaintext (Hex):")
        print(format_bytes_as_matrix(plaintext_bytes))
        decrypted_blocks.append(plaintext_bytes.hex())
        print("\n")

    # joining all the decrypted plaintexts to return final plaintext
    final_plaintext = "".join(decrypted_blocks)

    print("\n-----------------------------------------------------\n")
    print("Final Decrypted Plaintext (Hex):", final_plaintext)
    print("\n-----------------------------------------------------\n")




if __name__ == '__main__':
  
    print("Enter plaintext and key in hexadecimal format (space-separated bytes, 16 bytes each).")
    #input plaintext 
    pt = input("Enter plaintext (Hex): ").replace(" ", "")
 
    # Input  key 
    k = input("Enter key (Hex): ").replace(" ", "")

    #Input the rounds 
    rounds = int(input("Enter Number of Rounds: "))

    # Error handling to check the size of input recevied 
    if len(pt)%32!=0  or len(k)%32!=0 :
        print("INVALID INPUT! Plaintext and key length should be 16 bytes (32 hex characters) or 128 bits.")
    else:
        execute_aes(pt, k, rounds)
           
