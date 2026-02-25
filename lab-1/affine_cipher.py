# GCD Program

import sys
import signal
import random

ASCII_FIRST = 32
ASCII_SECOND = 126
VALID_KEY = ASCII_SECOND - ASCII_FIRST + 1 # 95

"""
Function to enable ctrl + c
"""
def def_handler(sig, frame):
    print("\n\n[!] Leaving...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

"""
Get greatest common divisor using Euclid's algorithm
"""
def gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a

"""
Generate the Z_n* set (All numbers from 1 to n-1 that are coprime to n)
"""
def generate_zn_star(n: int) -> list:
    zn_star = []

    for i in range(1, n):
        if gcd(i, n) == 1:
            zn_star.append(i)

    return zn_star

"""
Obtain b when gcd(a,b) = 1 testing all the numbers
"""
def getb_zn(a: int, n: int) -> int:
    if isinstance(n, int) and isinstance(a, int):
        if gcd(a,n) != 1:
            # print("\n[!] No inverse exists")
            return None
        zn_star = generate_zn_star(n)
        for element in zn_star:
            if (a * element) % n == 1:
                return element
"""
Generate K by random key generation using the get_zn function.
"""
def key_generation():
    while True:
        a = random.randrange(0, VALID_KEY)
        if getb_zn(a, VALID_KEY) is not None:
            break

    b = random.randrange(0, VALID_KEY)

    return (a, b)
"""
Convert a single character to its ASCII code if its printable.
Keep '\n' as a special case to preserve line breaks
"""
def char_to_code(code: str) -> int:

    if code == '\n':
        return -1
    con = ord(code) # return the ASCII to code (number)
    if con < ASCII_FIRST or con > ASCII_SECOND:
        print("[!] Error")
        return -1
    return con

"""
Encrypt the data
"""
def encrypt_file(filename: str, key: tuple):

    with open(filename, 'r') as f:
        plaintext = f.read()
    ciphertext = ""

    for char in plaintext:
        if char == '\n':
            ciphertext += '\n'
        else:
            num = ord(char) - 32
            encrypted = (key[0] * num + key[1]) % VALID_KEY
            ciphertext += chr(encrypted + 32)

    with open("ciphertext.txt", 'w') as f:
        f.write(ciphertext)
    
    print("[+] Encryption completed -> ciphertext.txt")


def code_to_char(code: int) -> str:

    if code == -1:
        return '\n'
    final = code - 32
    return final

"""
Function to join and gather all the functions
"""
def joining_data():
    """
    print(f"\n\n[+] Please, insert 2 numbers: \n")

    n1= int(input("Number 1: "))
    n2 = int(input("Number 2: "))
    n = int(input("Insert n: "))

    result = gcd(n1,n2)
    resultZn = generate_zn_star(n)

    print(result)
    print(f"Z_{n}* = {resultZn}")
    result2 = char_to_code(str(result))
    print(result2)
    result3 = code_to_char(result2)
    print(result3)

    a = int(input("a: "))
    n = int(input("n: "))
    element = getb_zn(a,n)
    print(element)
    """
    key = key_generation()
    print(f"[{key[0]}, {key[1]}]")

    print("\n\n")
    result = encrypt_file("test.txt", key)
    print(result)

if __name__ == '__main__':

    joining_data()
