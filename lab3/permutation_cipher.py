import random

# Resendiz Rios Diego Emiliano
# Ramirez Flores Rodrigo Pepe XD

SIZE = 100

def message():
    while True:
        text = input().strip()

        if not text.isalpha():
            print("Only English Letters allowed")
            continue

        return text.upper()


def random_number(min_v, max_v):
    return random.randint(min_v, max_v)


def permutation_random(n: int) -> list:
    if n < 3:
        return 0

    P = list(range(1, n + 1))

    for i in range(n - 1, 0, -1):
        num = random_number(0, i)
        P[i], P[num] = P[num], P[i]

    print("Permutation:")
    for i in P:
        print(f"[{i}]", end="")
    print()

    return P


def inverse_permutation():
    n = int(input("Enter the block message segmentation: "))

    P = []
    print("Enter the permutation used for encryption:")

    for i in range(n):
        p = int(input(f"Perm[{i}]: "))
        P.append(p)

    Inv = [0] * n
    for element in range(n):
        Inv[P[element] - 1] = element + 1

    return Inv, n


def permutation_cipher(m: str, P: list) -> str:
    n = len(P)
    cipher_text = ''
    m = m.replace(" ", "").replace("\n","")

    for element in range(0, len(m), n):
        cipher_block = ''
        block = m[element:element+n] # 0 til 0+n, where n is len of Permutation

        while len(block) < n:
            block += 'X' # if length of the block is not enough large, add 'X'

        for j in range(n):
            # block[P[j]] where P[j] is 0 but for example P could be P = [2, 0, 1]
            # so, block[0] but in this case, for the text "HELLO WORLD"
            # the length of block is 3 (because above we had 3 [2,0,1])
            # so block[0] is 2 so we have to count until m[2] -> HEL, we have L in position 2
            # so the first character to cipher_block is L
            cipher_block = cipher_block + block[P[j] - 1]

        cipher_text += cipher_block

    return cipher_text


def permutation_decipher(ciphertext: str, Inv: list, n: int) -> str:
    plaintext = ''

    for element in range(0, len(ciphertext), n):
        block = ciphertext[element:element+n]

        plain_block = ''

        for j in range(n):
            plain_block += block[Inv[j] - 1]

        plaintext += plain_block

    return plaintext


def join():
    plaintext = message()

    n = int(input("Enter the block message segmentation: "))

    P = permutation_random(n)

    print("\nCipher text:")
    cipher = permutation_cipher(plaintext, P)
    print(cipher)

    print("\nEnter ciphertext to decipher:")
    ciphertext = message()

    Inv, n = inverse_permutation()

    print("\nDeciphered text:")
    plain = permutation_decipher(ciphertext, Inv, n)
    print(plain)


if __name__ == '__main__':
    join()