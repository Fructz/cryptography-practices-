# GCD Program

ASCII_FIRST = 32
ASCII_SECOND = 126

"""
Compute greatest common divisor using Euclid's algorithm
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

def code_to_char(code: int) -> str:

    if code == -1:
        return '\n'
    final = code - 32
    return final

if __name__ == '__main__':

    print(f"[+] Please, insert 2 numbers to get their gcd\n")
    n1= int(input("Number 1: "))
    n2 = int(input("Number 2: "))
    n = int(input("Insert n: "))

    result = gcd(n1,n2)
    resultZn = generate_zn_star(n)

    print(f"Z_{n}* = {resultZn}")
    print(result)
    result2 = char_to_code(str(result))
    print(result2)
    result3 = code_to_char(result2)
    print(result3)
