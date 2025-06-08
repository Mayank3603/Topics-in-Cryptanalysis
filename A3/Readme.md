# Toy Cipher and Differential Cryptanalysis Project

This project demonstrates a simple toy cipher and applies differential cryptanalysis to attack it. Although the cipher is deliberately simplistic and not secure by modern standards, it serves as a great learning tool for understanding basic principles of symmetric encryption, S-box design, and cryptanalytic techniques.

---

## Project Structure

- **Part 1: Toy Cipher Implementation**  
  Implements a 5-round toy cipher that operates on 16-bit blocks. It features:
  - A fixed S-box (and its inverse) for nibble-wise substitution.
  - A fixed bit permutation (P-box) to scramble bits.
  - Helper functions for converting between integers, bit lists, and 4-bit nibbles.
  - A key generation routine that produces six 16-bit round keys (hard-coded for reproducibility).
  - An encryption function that processes the plaintext through 5 rounds of encryption.

- **Part 2: Difference Distribution Table (DDT)**  
  (Not included in the files here but conceptually described.)  
  This part computes the DDT for the S-box. The DDT is used to analyze how differences in the input propagate through the S-box and is an essential tool in differential cryptanalysis.

- **Part 3: Differential Trail Exploration**  
  (Conceptually described.)  
  This part explores possible differential trails over 4 rounds of the toy cipher.  
  Initially, I attempted to consider every S-box as potentially active, but that approach resulted in an overwhelming number of possibilities.  
  Instead, I refined the method by:
  - Normalizing the DDT.
  - For each round, treating inactive nibbles (i.e., those with an input difference of zero) separately.
  - For active nibbles, choosing the output difference with the highest probability from the DDT.
  - Permuting the combined output difference and proceeding to the next round.
  
  This more structured, iterative approach greatly simplified the search for the most likely differential trail.

- **Part 4: Differential Attack for Key Recovery**  
  This part demonstrates a differential attack on the toy cipher by:
  1. **Data Collection:**  
     Generating \(2^{12}\) plaintext pairs, where each plaintext is paired with its variant (obtained by XORing with a fixed input difference, 0x0020).
  2. **Filtering:**  
     Keeping only those ciphertext pairs where the XOR difference shows zeros in the inactive nibbles (positions 0, 1, and 3).
  3. **Active Nibble Recovery:**  
     Recovering the active nibble (nibble index 2) of the final round key. Initially, my attempts to recover the full key directly failed due to the large key space. By focusing only on the active nibble (which, based on the differential trail, is the only one that changes), the search space was drastically reduced.
  4. **Brute Force:**  
     After recovering the active nibble, the remaining 12 bits of the key were brute-forced using a known plaintext-ciphertext pair. This two-step approach eventually allowed us to correctly determine the final round key.

## Challenges Faced

### Differential Trail Exploration (Part 3)

**Initial Approach:**  
I initially attempted to treat every S-box in every round as active, exploring all possible differences. This approach led to an explosion of possibilities and quickly became unmanageable.

**Refined Strategy:**  
To overcome this, I normalized the DDT and processed each round by:
- Treating inactive nibbles (with an input difference of zero) separately.
- For active nibbles, choosing the output difference that had the highest probability according to the DDT.
- Permuting the results and using the outcome as the input for the next round.

This iterative, round-by-round method significantly reduced complexity and provided a clear path toward identifying the most likely differential trail.

### Differential Attack for Key Recovery (Part 4)

**Initial Attempts:**  
My first attempts to recover the entire 16-bit last round key directly were unsuccessful because the search space was simply too large with limited data.

**Refined Approach:**  
I then focused on the fact that, according to the differential trail, only one nibble (nibble index 2) is active in the final round. By:
- Recovering only this active nibble using a candidate counting mechanism.
- Once that nibble was determined, brute-forcing the remaining 12 bits using a known plaintext-ciphertext pair.

This targeted approach greatly reduced the search space and ultimately enabled successful key recovery.
