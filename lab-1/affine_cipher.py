# Affine cipher Program
# Ramirez Flores Rodrigo Iñaki
# Resendiz Rios Dieg Emiliano

import sys
import signal
import random
import os

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
Obtain b when gcd(a,b) = 1 testing all the numbers --- Get inverse of 1 number
"""
def getb_zn(a: int, n: int) -> int:
    if isinstance(n, int) and isinstance(a, int): # isinstance is to be sure that a and b are integers
        if gcd(a,n) != 1:
            # print("\n[!] No inverse exists")
            return None
        zn_star = generate_zn_star(n)
        for element in zn_star:
            if (a * element) % n == 1: # gcd((a * element), n) == 1
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
Encrypt the data
"""
def encrypt_file(filename: str, key: tuple):

    if not os.path.isfile(filename):
        print(f"[!] ERROR: '{filename}' is not a valid file")
        return None
    
    try:
        with open(filename, 'r') as f:
            plaintext = f.read()
    except Exception as e:
        print(f"[!] Unexpected error while opening file: {e} \n\nPlease be sure that the data was started correctly\n")
        return None

    ciphertext = ""

    for char in plaintext:
        if char == '\n':
            ciphertext += '\n'
        else:
            num = ord(char) - 32 # Get number and minus 32 to work with 0 value
            encrypted = (key[0] * num + key[1]) % VALID_KEY
            ciphertext += chr(encrypted + 32) # Back adding 32

    with open("ciphertext.txt", 'w') as f:
        f.write(ciphertext)

    print("\n[+] Encryption completed -> ciphertext.txt")

"""
Decipher the data
"""
def deciphering_file(inputFile: str, outputFile: str):
    print("Enter your key:")
    a = int(input("a: "))
    b = int(input("b: "))

    a_inv = getb_zn(a, VALID_KEY)

    with open(inputFile, 'r') as f:
        ciphertext = f.read()

    decoded_text = ""

    for char in ciphertext:
        if char == '\n':
            decoded_text += '\n'
        else:
            num = ord(char) - 32
            decoded = (a_inv * (num - b)) % VALID_KEY
            decoded_text += chr(decoded + 32)

    with open(outputFile, 'w') as f:
        f.write(decoded_text)

    print(f"[+] Decryption completed -> {outputFile}")

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
    encrypt_file("test.txt", key)
    deciphering_file("ciphertext.txt", "decoded.txt")

if __name__ == '__main__':

    joining_data()
