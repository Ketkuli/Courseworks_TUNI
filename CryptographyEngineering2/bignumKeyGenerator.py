"""
This file is used to convert private key to public key 
"""

from bignum import *
from bignumEC import *

'''
Provided by teacher begins
'''
# A string N of hexadecimals (without initial 0x) into a bignum in base 16
def hexto16(N):
    return [int(h,16) for h in N[::-1]] # reverse order of the argument string

# A bignum N in base 16 into a string of hexadecimals
def from16tohex(N):
    return ''.join([hex(i)[2].upper() for i in N[::-1]])

'''
Provided by teacher ends    
'''

def keyGenerator(kPR, G, Curve, B):
    '''
    Creates a public key using bignum from the private key kPR that was given
    as parameter.

    B is calculated by: B = kPR * Generator
    '''

    d = hexto16(kPR)
    #Gx = hexto16(G[0])
    #Gy = hexto16(G[1])
    G = [hexto16(G[0]), hexto16(G[1])]

    p = hexto16(Curve[0])
    a = hexto16(Curve[1])
    b = hexto16(Curve[2])
    C = [p, a, b]

    B = double_addECbig(G, d, C, B)
    

    Bx = from16tohex(B[0])
    By = from16tohex(B[1])

    return [Bx, By]  





if __name__ == "__main__":

    G = ["9487239995A5EE76B55F9C2F098", 
     "A89CE5AF8724C0A23E0E0FF77500"]

    C = ["DB7C2ABF62E35E668076BEAD208B", 
     "DB7C2ABF62E35E668076BEAD2088", 
     "659EF8BA043916EEDE8911702B22"]

    testNum='123456789'
    pubkey = ['4A344D697065350237C1CA5A7F0C', 'F6E49D16FE078145D45441FB859']

    print("Test prints to check that the function works:")
    output = keyGenerator(testNum, G, C, 16)
    print(f"If this is True the output is correct: {output == pubkey}")
    print(output)
    print(pubkey)

    print("\nThis is the real deal:")
    snum = "123456"
    publicKey = keyGenerator(snum, G, C, 16)
    print(f"Student number = H{snum}")
    print(f"Corresponding public key = {publicKey}")