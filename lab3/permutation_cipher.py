import random

# Resendiz Rios Diego Emiliano
# Ramirez Flores Rodrigo Pepe XD
def permutation_random(n: int) -> list:
    if n < 3:
        return 0
    P = list(range(n))
    random.shuffle(P)
    return P

    return P

def inverse_permutation(P: list) -> list:
    n = len(P)
    if n < 3:
        return 0

    Inv = [0] * n
    for element in range(n):
        Inv[P[element]] = element
    
    return Inv

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
            cipher_block = cipher_block + block[P[j]] 
        
        cipher_text += cipher_block
    
    return cipher_text


def join():
    P = permutation_random(3)
    print(P)
    print(permutation_cipher("HELLO WORLD", P))

if __name__ == '__main__':
    join()
