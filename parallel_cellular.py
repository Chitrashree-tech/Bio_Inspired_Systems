import numpy as np

# -------------------------
# Cellular Automata Parameters
# -------------------------
n = 8  # number of cells in CA
rule_number = 30  # Wolfram rule 30

# -------------------------
# Apply CA rule
# -------------------------
def apply_rule(left, center, right, rule):
    index = (left << 2) | (center << 1) | right
    return (rule >> index) & 1

# -------------------------
# Generate CA key stream
# -------------------------
def generate_key(seed, rule, length):
    state = seed.copy()
    key_stream = []
    for _ in range(length):
        key_stream.append(state[-1])  # output last cell
        new_state = np.zeros_like(state)
        for i in range(len(state)):
            left = state[i-1] if i>0 else state[-1]
            center = state[i]
            right = state[i+1] if i<len(state)-1 else state[0]
            new_state[i] = apply_rule(left, center, right, rule)
        state = new_state
    return np.array(key_stream)

# -------------------------
# XOR for encryption/decryption
# -------------------------
def xor_bits(data_bits, key_bits):
    return np.array([d ^ k for d, k in zip(data_bits, key_bits)])

# -------------------------
# Convert string to bits and back
# -------------------------
def string_to_bits(s):
    bits = []
    for char in s:
        bits.extend([int(b) for b in format(ord(char), '08b')])
    return bits

def bits_to_string(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int(''.join(map(str, byte)), 2)))
    return ''.join(chars)

# -------------------------
# Main
# -------------------------
plaintext_str = "HELLO"
plaintext_bits = string_to_bits(plaintext_str)
print("Plaintext:", plaintext_str)
print("Plaintext bits:", plaintext_bits)

# Random CA seed of 8 bits
seed = np.random.randint(0, 2, n)
print("Initial CA Seed:   ", seed.tolist())

# Repeat key stream to match plaintext length
key_stream = np.tile(generate_key(seed, rule_number, n), len(plaintext_bits)//n + 1)[:len(plaintext_bits)]
print("Generated Key Bits:", key_stream.tolist())

# Encrypt
ciphertext_bits = xor_bits(plaintext_bits, key_stream)
print("Ciphertext bits:   ", ciphertext_bits.tolist())

# Decrypt
decrypted_bits = xor_bits(ciphertext_bits, key_stream)
decrypted_str = bits_to_string(decrypted_bits)
print("Decrypted bits:    ", decrypted_bits.tolist())
print("Decrypted Text:    ", decrypted_str)
