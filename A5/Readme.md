# MD5 Hash Function Implementation

This project implements the **MD5 (Message-Digest Algorithm 5)** , without using any external libraries like `hashlib`.
## 📌 What is MD5?

MD5 is a widely used **cryptographic hash function** that produces a **128-bit (16-byte) hash value**, typically rendered as a **32-character hexadecimal number**. It is used in:

- File integrity checking
- Password hashing
- Digital signatures
- Checksums for network transmissions

---

##  Features

- Full implementation from scratch
- Follows the **5 major steps** of MD5:
  1. Padding the input
  2. Appending original length
  3. Initialization of MD buffer
  4. Processing message in 512-bit chunks
  5. Final output as hexadecimal digest
- All operations use **32-bit unsigned integers**
- Includes **test suite** based on known MD5 outputs
---

##  How It Works

### Functions Breakdown

- `prepare_message(input_string)`  
  Pads the message and appends its original length in bits.

- `left_rotate_32bit(value, shift_amount)`  
  Performs 32-bit left rotation.

- `get_shift_amounts()`  
  Returns predefined shift values for each MD5 round.

- `get_md5_constants()`  
  Generates the constant table using `sin(i + 1)` as described in the MD5 specification.

- `process_chunk(chunk_bytes, hash_state, shift_amounts, constants)`  
  Applies the MD5 transformation logic to each 512-bit chunk.

- `md5(input_string)`  
  Main function to compute the MD5 hash of a string.

- `main()`  
  Runs the test suite to verify the correctness of the implementation.

---

## 🧪 Test Cases

These are hardcoded in the program and verified against standard MD5 outputs:

| Input | MD5 Output |
|-------|------------|
| `""` | `d41d8cd98f00b204e9800998ecf8427e` |
| `"a"` | `0cc175b9c0f1b6a831c399e269772661` |
| `"abc"` | `900150983cd24fb0d6963f7d28e17f72` |
| `"message digest"` | `f96b697d7cb7938d525a2f31aaf161d0` |
| `"abcdefghijklmnopqrstuvwxyz"` | `c3fcd3d76192e4007dfb496cca67e13b` |
| `"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"` | `d174ab98d277d9f5a5611c2c9f419d9f` |
| `"12345678901234567890123456789012345678901234567890123456789012345678901234567890"` | `57edf4a22be3c955ac49da2e2107b67a` |

---

### Run the Code

```bash
python md5.py
```