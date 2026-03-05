import random

# Printable ASCII range
ASCII_FIRST = 32
ASCII_SECOND = 126
MOD = ASCII_SECOND - ASCII_FIRST + 1  # Size of alphabet (95)


def gcd(a: int, b: int) -> int:
    """
    Compute the greatest common divisor using Euclidean algorithm.
    """
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def key_generation() -> list:
    """
    Generate a valid 2x2 Hill cipher key matrix.
    The matrix is valid if gcd(det(K), MOD) == 1.
    """
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
    """
    Compute multiplicative inverse of a modulo n
    using Extended Euclidean Algorithm.
    """
    if n < 2:
        raise ValueError("Modulo must be >= 2")

    a_0 = n
    b_0 = a
    t_0 = 0
    t = 1

    while b_0 != 0:
        q = a_0 // b_0
        a_0, b_0 = b_0, a_0 - q * b_0
        t_0, t = t, (t_0 - q * t) % n

    if a_0 != 1:
        raise ValueError("Inverse does not exist")

    return t_0


def matrix_inverse(K: list) -> list:
    """
    Compute inverse of 2x2 matrix K modulo MOD.
    """
    a = K[0][0]
    b = K[0][1]
    c = K[1][0]
    d = K[1][1]

    det = (a*d - b*c) % MOD
    det_inv = Mult_Inv(det, MOD)

    K_inv = [
        [(d * det_inv) % MOD, (-b * det_inv) % MOD],
        [(-c * det_inv) % MOD, (a * det_inv) % MOD]
    ]

    return K_inv


def hill_encrypt(text: str, K: list) -> str:
    """
    Encrypt text using Hill cipher (2x2) over printable ASCII.
    Line breaks are preserved and not encrypted.
    """
    ciphertext = ""
    buffer = ""

    for char in text:

        # Preserve line breaks
        if char == '\n':
            ciphertext += '\n'
            continue

        buffer += char

        # Process block of size 2
        if len(buffer) == 2:
            p0 = ord(buffer[0]) - ASCII_FIRST
            p1 = ord(buffer[1]) - ASCII_FIRST

            c0 = (p0*K[0][0] + p1*K[0][1]) % MOD
            c1 = (p0*K[1][0] + p1*K[1][1]) % MOD

            ciphertext += chr(c0 + ASCII_FIRST)
            ciphertext += chr(c1 + ASCII_FIRST)

            buffer = ""

    # Padding if one character remains
    if len(buffer) == 1:
        buffer += "X"

        p0 = ord(buffer[0]) - ASCII_FIRST
        p1 = ord(buffer[1]) - ASCII_FIRST

        c0 = (p0*K[0][0] + p1*K[0][1]) % MOD
        c1 = (p0*K[1][0] + p1*K[1][1]) % MOD

        ciphertext += chr(c0 + ASCII_FIRST)
        ciphertext += chr(c1 + ASCII_FIRST)

    return ciphertext


def hill_decipher(text: str, K_inv: list) -> str:
    """
    Decrypt text using inverse Hill matrix.
    Line breaks are preserved.
    """
    plaintext = ""
    buffer = ""

    for char in text:

        if char == '\n':
            plaintext += '\n'
            continue

        buffer += char

        if len(buffer) == 2:
            p0 = ord(buffer[0]) - ASCII_FIRST
            p1 = ord(buffer[1]) - ASCII_FIRST

            c0 = (p0*K_inv[0][0] + p1*K_inv[0][1]) % MOD
            c1 = (p0*K_inv[1][0] + p1*K_inv[1][1]) % MOD

            plaintext += chr(c0 + ASCII_FIRST)
            plaintext += chr(c1 + ASCII_FIRST)

            buffer = ""

    return plaintext


def encrypt_file(input_file: str, output_file: str, K: list):
    """
    Encrypt contents of input_file and write result to output_file.
    """
    with open(input_file, "r") as f:
        plaintext = f.read()

    ciphertext = hill_encrypt(plaintext, K)

    with open(output_file, "w") as f:
        f.write(ciphertext)

    print("Ciphertext saved in:", output_file)


def decipher_file(input_file: str, output_file: str, K_inv: list):
    """
    Decrypt contents of input_file and write result to output_file.
    """
    with open(input_file, "r") as f:
        ciphertext = f.read()

    plaintext = hill_decipher(ciphertext, K_inv)

    with open(output_file, "w") as f:
        f.write(plaintext)

    print("Plaintext saved in:", output_file)


def main():
    """
    Execute full encryption-decryption cycle.
    """
    K = key_generation()
    K_inv = matrix_inverse(K)

    encrypt_file("test.txt", "ciphertexts.txt", K)
    decipher_file("ciphertexts.txt", "decrypted_file.txt", K_inv)


if __name__ == "__main__":
    main()
