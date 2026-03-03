import random

ASCII_FIRST = 32
ASCII_SECOND = 126
MOD = ASCII_SECOND - ASCII_FIRST + 1 # 95


def gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a

def key_generation():
    while True:
        K = [
            [random.randint(0, MOD - 1), random.randint(0, MOD - 1)],
            [random.randint(0, MOD - 1), random.randint(0, MOD - 1)]
        ]

        det = (K[0][0]*K[1][1] - K[0][1]*K[1][0]) % MOD

        if gcd(det, MOD) == 1:
            print("Generated key:")
            print(K[0])
            print(K[1])
            return K

def hill_encrypt(text, K):
    if len(text) % 2 != 0:
        text += "X"

    ciphertext = ""

    for i in range(0, len(text), 2):
        p0 = ord(text[i]) - ASCII_FIRST
        p1 = ord(text[i+1]) - ASCII_FIRST

        c0 = (p0*K[0][0] + p1*K[0][1]) % MOD
        c1 = (p0*K[1][0] + p1*K[1][1]) % MOD

        ciphertext += chr(c0 + ASCII_FIRST)
        ciphertext += chr(c1 + ASCII_FIRST)

    return ciphertext

def encrypt_file(input_file, output_file):
    K = key_generation()

    with open(input_file, "r") as f:
        plaintext = f.read()

    ciphertext = hill_encrypt(plaintext, K)

    with open(output_file, "w") as f:
        f.write(ciphertext)

    print("\nCiphertext saved in:", output_file)

if __name__ == "__main__":
    encrypt_file("plaintext.txt", "ciphertext.txt")