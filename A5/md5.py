import struct
import math

# It left rotate a 32-bit integer by a given number of bits
def left_rotate_32bit(value, shift_amount):
    value &= 0xFFFFFFFF
    return ((value << shift_amount) | (value >> (32 - shift_amount))) & 0xFFFFFFFF

#It generate shift amounts for each of the 64 MD5 operations
def get_shift_amounts():
    return (
        [7, 12, 17, 22] * 4 +
        [5, 9, 14, 20] * 4 +
        [4, 11, 16, 23] * 4 +
        [6, 10, 15, 21] * 4
    )

# The function generates the MD5 constant table using sine values
def get_md5_constants():
    return [int(abs(math.sin(i + 1)) * (2**32)) & 0xFFFFFFFF for i in range(64)]

# This function to prepare the message by padding it to match MD5 specification
def prepare_message(input_string):
    byte_message = bytearray(input_string, 'utf-8')
    original_bit_length = (8 * len(byte_message)) & 0xffffffffffffffff

    # Append '1' bit followed by required '0' bits
    byte_message.append(0x80)
    while (len(byte_message) * 8) % 512 != 448:
        byte_message.append(0)

    # Append the original message length as a 64-bit little-endian integer
    byte_message += struct.pack('<Q', original_bit_length)
    return byte_message

# The function prrocesses a single 512-bit chunk and update intermediate hash state
# process one 64 byte chuck
# convert it into 16 32 bits chuckes
def process_chunk(chunk_bytes, hash_state, shift_amounts, constants):
    a, b, c, d = hash_state
    message_words = list(struct.unpack('<16I', chunk_bytes))

    for i in range(64):
        if 0 <= i <= 15:
            f = (b & c) | (~b & d)
            word_index = i
        elif 16 <= i <= 31:
            f = (d & b) | (~d & c)
            word_index = (5 * i + 1) % 16
        elif 32 <= i <= 47:
            f = b ^ c ^ d
            word_index = (3 * i + 5) % 16
        else:
            f = c ^ (b | ~d)
            word_index = (7 * i) % 16

        f = (f + a + constants[i] + message_words[word_index]) & 0xFFFFFFFF
        a, d, c, b = d, c, b, (b + left_rotate_32bit(f, shift_amounts[i])) & 0xFFFFFFFF

    # then adding the processing chunk's transformed state to the overall hash state
    return [
        (hash_state[0] + a) & 0xFFFFFFFF,
        (hash_state[1] + b) & 0xFFFFFFFF,
        (hash_state[2] + c) & 0xFFFFFFFF,
        (hash_state[3] + d) & 0xFFFFFFFF,
    ]

# ain MD5 function that returns a 32-character hexadecimal digest
def md5(input_string):
    shift_amounts = get_shift_amounts()
    constants = get_md5_constants()
    message = prepare_message(input_string)

    # first -> Initalising initial buffer values (standard constants from RFC 1321)
    hash_state = [
        0x67452301,  # A
        0xefcdab89,  # B
        0x98badcfe,  # C
        0x10325476   # D
    ]

    for chunk_offset in range(0, len(message), 64):
        chunk = message[chunk_offset:chunk_offset + 64]
        hash_state = process_chunk(chunk, hash_state, shift_amounts, constants)

    # Then packing final state into a hexadecimal digest string
    final_digest = struct.pack('<4I', *hash_state)
    return ''.join(f'{byte:02x}' for byte in final_digest)

# Running test cases through the MD5 function
def main():
    test_inputs = [
        # "",
        # "a",
        "abc",
        # "message digest",
        # "abcdefghijklmnopqrstuvwxyz",
        # "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        # "12345678901234567890123456789012345678901234567890123456789012345678901234567890"
    ]

    for test in test_inputs:
        print(f'MD5 of ("{test}") =>  {md5(test)}')

if __name__ == "__main__":
    main()
