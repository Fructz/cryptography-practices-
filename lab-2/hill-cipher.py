import random

ASCII_FIRST = 32
ASCII_SECOND = 126
MOD = ASCII_SECOND - ASCII_FIRST + 1 # 95

def gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a

def key_generation() -> tuple:
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

def Mult_Inv(a: int, n: int) -> int:
    
    if n < 2:
        print("\n\n[!] ERROR -> n has to be greater or equal than 2.\n")
        return 0

    a_0 = n
    b_0 = a
    t_0 = 0
    t = 1
    q = (a_0 // b_0)
    r = (a_0 - q*b_0)
    temp = 0

    while r > 0: # b_0
        temp = (t_0 - q*t) % n
        t_0 = t
        t = temp
        a_0 = b_0
        b_0 = r
        q = (a_0 // b_0)
        r = (a_0 - q*b_0)
    if b_0 != 1:
        return 0
    else:
        return t

def hill_encrypt(text, K):

    ciphertext = ""
    buffer = ""

    for char in text:

        if char == '\n':
            ciphertext += '\n'
            continue

        buffer += char

        if len(buffer) == 2:

            p0 = ord(buffer[0]) - ASCII_FIRST # ord: letter -> number unicode
            p1 = ord(buffer[1]) - ASCII_FIRST

            c0 = (p0*K[0][0] + p1*K[0][1]) % MOD
            c1 = (p0*K[1][0] + p1*K[1][1]) % MOD

            ciphertext += chr(c0 + ASCII_FIRST) # chr: number unicode -> letter
            ciphertext += chr(c1 + ASCII_FIRST)

            buffer = ""

    # Padding 
    if len(buffer) == 1:
        buffer += "X"

        p0 = ord(buffer[0]) - ASCII_FIRST
        p1 = ord(buffer[1]) - ASCII_FIRST

        c0 = (p0*K[0][0] + p1*K[0][1]) % MOD
        c1 = (p0*K[1][0] + p1*K[1][1]) % MOD

        ciphertext += chr(c0 + ASCII_FIRST)
        ciphertext += chr(c1 + ASCII_FIRST)

    return ciphertext

def encrypt_file(input_file, output_file, K: tuple):

    with open(input_file, "r") as f:
        plaintext = f.read()

    ciphertext = hill_encrypt(plaintext, K)

    with open(output_file, "w") as f:
        f.write(ciphertext)

    print("\nCiphertext saved in:", output_file)

def matrix_inverse(K: tuple) -> int:
    
    a = K[0][0]
    b = K[0][1]
    c = K[1][0]
    d = K[1][1]

    det = (K[0][0]*K[1][1] - K[0][1]*K[1][0]) % MOD
    det_inv = Mult_Inv(det, MOD)

    k_inv = [[(d * det_inv) % MOD,(-b * det_inv) % MOD],
    [(-c * det_inv) % MOD, (a * det_inv) % MOD]]

    return k_inv, det_inv

def hill_decipher(text: str, k_inv: int) -> str:

    ciphertext = ""
    buffer = ""
    plaintext = ""

    for char in text:

        if char == '\n':
            plaintext += '\n'
            continue

        buffer += char

        if len(buffer) == 2:

            p0 = ord(buffer[0]) - ASCII_FIRST # ord: letter -> number unicode
            p1 = ord(buffer[1]) - ASCII_FIRST

            c0 = (p0*k_inv[0][0] + p1*k_inv[0][1]) % MOD
            c1 = (p0*k_inv[1][0] + p1*k_inv[1][1]) % MOD

            plaintext += chr(c0 + ASCII_FIRST) # chr: number unicode -> letter
            plaintext += chr(c1 + ASCII_FIRST)

            buffer = ""

    return plaintext

def decipher_file(encrypted_file, output_file, K: tuple):

    with open(encrypted_file, "r") as f:
        ciphertext = f.read()

    plaintext = hill_decipher(ciphertext, K)

    with open(output_file, "w") as f:
        f.write(plaintext)

    print("\nPlaintext saved in:", output_file)


def join():
    K = key_generation()
    k_inv, det_inv = matrix_inverse(K)
    encrypt_file("test.txt", "ciphertexts.txt", K)
    decipher_file("ciphertexts.txt", "decrypted_file.txt", k_inv)

if __name__ == "__main__":
    join()
