'''
Programming assignment for COMP.SEC.210 Cryptography Engineering 2:

Author: Paavo Peltopihko
Student number = H123456
Corresponding public key = ['C670C6F15690D2D592A6236E6F98', 
                            '89984310E4B42A7439080A79E750']


Values to use for the curve. Please note that the "0x" is removed from each of 
the value, but those are still hexadecimal strings.
'''

# Student number and the corresponding public argument B, here as "pubkey"
# This is worded as pubkey so that the collision with base B is not happening.
# Output of the file bignumKeyGenerator.py
sNum = 'H123456'
pubkey = ['C670C6F15690D2D592A6236E6F98', '89984310E4B42A7439080A79E750']

# Generator: 
Generator = ["9487239995A5EE76B55F9C2F098", 
     "A89CE5AF8724C0A23E0E0FF77500"]

p = "DB7C2ABF62E35E668076BEAD208B"
a = "DB7C2ABF62E35E668076BEAD2088"
b = "659EF8BA043916EEDE8911702B22"
Curve = [p, a, b]

# Order of the G i.e. the size of the subgroup:
Q = "DB7C2ABF62E35E7628DFAC6561C5"


'''
4 functions provided by teacher to use to convert hex to bignum base 16 and back
'''
# A string N of hexadecimals (without initial 0x) into a bignum in base 16
def hexto16(N):
    return [int(h,16) for h in N[::-1]] # reverse order of the argument string

# A bignum N in base 16 into a string of hexadecimals
def from16tohex(N):
    return ''.join([hex(i)[2].upper() for i in N[::-1]])

# Convert a string of hexadecimals H (without initial 0x) to its representation 
# in base B.
def hextoB(H,B):
    if B == 16:
        return hexto16(H)
    else:
        return convert(hexto16(H),16,B)

# Convert a bit string K to its representation in base B, via hexadecimals.
def bitstoB(K,B):
    res = ''
    while len(K) % 4 != 0:  # Pad K to a length that is a multiple of 4.
        K = '0'+K
    for i in range(0, len(K), 4): # Convert each chunk of four bits to an integer.
        chunk = K[i:i + 4]
        dec = int(chunk, 2)    
        res += hex(dec)[2:].upper()  # join them into a hex string
    return hextoB(res,B)


'''
Import libraries for calculations, from here it is all my own work:
'''
from bignum import *    # Including all the bignum calculations
from bignumEC import *  # Includes all the functions to work with EC
import random           # Imported to create the ephemeral key kE.


def kEGeneration(B):
    '''
    Generates Ephemeral key that is 112 bit long and between 0 < kE < q
    Returns the Ephemeral key as bignum in base 16.
    '''

    while True:
        # Generate 14 random bytes meaning 112 bits:
        testKey = ""
        for i in range(112):
            bit = str(random.randint(0, 1))
            testKey += bit

        # Convert testKey and q to bignum:
        testKeybig = bitstoB(testKey, B)
        qBig = hextoB(Q, B)

        # Check if testkey is smaller than q:
        if compare(testKeybig, qBig) == -1:
            return testKeybig



def ECDSA(privkey, hash, B):
    '''
    Return the ECDSA signature as two strings of hexadecimals from function 
    ECDSA(privkey, hash, B), where privkey and hash are strings of 
    hexadecimals, and B is the base for the bignum operations.
    '''

    # Create ephemeral key kE for randomness:
    kE = kEGeneration(B)

    # Change hex-string arguments on q, G and C to bignum
    # G and C are global variables.
    q = hextoB(Q,B)
    G = [hextoB(N, B) for N in Generator]
    C = [hextoB(N, B) for N in Curve]
    p, a, b = C
    
    # Calculate R = kE * G, where kE is bignum and G is point on the curve
    R = double_addECbig(G, kE, C, B)

    # Create signature:    
    r = R[0]    # r is the x value in R

    # Calculate s in the signature:
    # s = ((h(x) + d * r)* inversekE) mod q, where d == privkey

    d = hextoB(privkey,B)
    hX = hextoB(hash, B)
    inversekE = modinv(kE, q, B)
    dTimesR = reduce(multiply(r, d, B), q, B)
    hashPlusDTimesR = reduce(add(hX, dTimesR, B), q, B)
    s = reduce(multiply(hashPlusDTimesR, inversekE, B), q, B)

    return [from16tohex(convert(r, B,16)),from16tohex(convert(s, B,16))]



if __name__ == "__main__":
    hash = '1234567890'
    Base = 16
    
    # Checking if the student number is with H or K before going to function:
    if sNum[0].isalpha():
        sNum = sNum[1:]

    output = ECDSA(sNum, hash, Base)

    print(f"The given signature for hash {hash} is:")
    print(output)
    print("")

