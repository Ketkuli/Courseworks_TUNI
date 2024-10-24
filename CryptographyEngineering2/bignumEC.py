"""
Assume you already have the inversion function from Ex8. Modify your EC 
operations from Hp5 to run with bignums. You can of course do Ex8 at this 
moment, but the idea is that you prepare all the rest for bignums and work 
on the inversion next week. Note that unlike the EEA in Ex8, you need not 
bother with negative numbers in EC operations. Just use your modsubtract() 
when computing the differences. If a number can be out of the modular range, 
use your reduce() (or  just divide()) before calling any arithmetic functions.
"""

# Import calculation operations
from bignum import *

def addECbig(Point1:list, Point2:list, Curve:list, Base:int):
    '''
    Point1 and Point2 are points on curve Curve that are added together
    
    Point1 is [x,y] as [bignum,bignum]
    Point2 is [x,y] as [bignum,bignum]
    Curve is [p,a,b] as [bignum,bignum,bignum]

    Returns Point3 [x,y] as [bignum, bignum] which is a point on the curve Curve
    '''

    # Checking the input first:
    infinity = [[0],[0]]
    if Point1 == infinity:
        return Point2
    elif Point2 == infinity:
        return Point1
    
    elif Point1 == Point2:
        return doublECbig(Point1,Curve)
    
    # Go to the calculation of the parameters in the elliptic curve:
    else:
        x1, y1 = Point1
        x2, y2 = Point2
        p, a, b = Curve
        # Calculations to get the slope s:
        # Get multiplicative modular inverse for x2-x1:
        # gcd, amodp, pmoda = gcdExtended((x2-x1)%p,p)
        x2minusx1 = modsubtract(x2, x1, p, Base)
        remainder = reduce(x2minusx1, p, Base)

        '''
        Change this part!!!
        '''
        # gcd, amodp, pmoda = gcdExtendedBignum(remainder, p, Base)
        # g, amodp, pmod = gcdExtended(Bto10(remainder,Base), Bto10(p,Base))

        aModP = modinv(remainder, p, Base)

        # There is no number that fulfills the equation:
        # a * a^-1 = 1 mod p, where a^-1 == 0.
        if aModP == [0]:
            return infinity
        
        # Calculate the slope:
        # s = ((y2-y1)*amodp)%p
        y2minusy1 = modsubtract(y2, y1, p, Base)
        #y2minusy1 = subtract(y2, y1, Base)
        timesAmodP = multiply(y2minusy1, aModP, Base)
        slope = reduce(timesAmodP, p, Base)

        # Calculate new points:
        # x3 = (s**2-x1-x2)%p
        sSquared = multiply(slope, slope, Base)
        sSquared = reduce(sSquared, p, Base)
        sSquaredMinusX1 = modsubtract(sSquared, x1, p, Base)
        sSquaredMinusX1MinusX2 = modsubtract(sSquaredMinusX1, x2, p, Base)
        #sSquaredMinusX1 = subtract(sSquared, x1, Base)
        #sSquaredMinusX1MinusX2 = subtract(sSquaredMinusX1, x2, Base)
        x3 = reduce(sSquaredMinusX1MinusX2, p, Base)

        # y3 = (s*(x1-x3)-y1)%p
        x1MinusX3 = modsubtract(x1, x3, p, Base)
        #x1MinusX3 = subtract(x1, x3, Base)
        sTimesX1MinusX3 = multiply(slope, x1MinusX3, Base)
        sTimesX1MinusX3 = reduce(sTimesX1MinusX3, p, Base)
        sTimesX1MinusX3MinusY1 = modsubtract(sTimesX1MinusX3, y1, p, Base)
        #sTimesX1MinusX3MinusY1 = subtract(sTimesX1MinusX3, y1, Base)
        y3 = reduce(sTimesX1MinusX3MinusY1, p, Base)

        return [x3,y3]



def doublECbig(Point:list, Curve:list, Base:int)->list:
    """
    Point is a point on the curve Curve that is added with itself

    Point is [x,y] as [bignum,bignum]
    Curve is [p,a,b] as [bignum,bignum,bignum]

    Returns newPoint [x,y] as [bignum, bignum] which is a point on the curve Curve 
    """

    x1, y1 = Point
    p, a, b = Curve

    # Calculations to get the slope s:
    # Get the multiplicative inverse for 2*y1:
    # gcd, amodp, pmoda = gcdExtended((2*y1)%p,p)

    twoTimesY1 = add(y1, y1, Base)
    twoTimesY1ModP = reduce(twoTimesY1, p, Base)

    aModP = modinv(twoTimesY1ModP, p, Base)
    
    # Calculate the slope:
    # s = ((3*x1**2+a)*aModP)%p
    
    x1Squared = reduce(multiply(x1, x1, Base), p, Base)
    threeTimesX1Squared = reduce(add(add(x1Squared,x1Squared, Base),x1Squared, Base),p, Base)
    threeTimesX1SquaredPlusA = reduce(add(threeTimesX1Squared, a, Base),p, Base)
    slope = reduce(multiply(threeTimesX1SquaredPlusA, aModP, Base), p, Base)

    # Calculate new points:
    # x2 = (s**2-x1-x1)%p
    # y2 = (s*(x1-x2)-y1)%p

    slopeSquared = reduce(multiply(slope, slope, Base), p, Base) 
    twoTimesX1 = reduce(add(x1, x1, Base), p, Base)
    x2 = reduce(modsubtract(slopeSquared, twoTimesX1, p, Base), p, Base)

    x1MinusX2 = modsubtract(x1, x2, p, Base)
    slopeTimesX1MinusX2 = reduce(multiply(slope, x1MinusX2, Base), p, Base)
    y2 = reduce(modsubtract(slopeTimesX1MinusX2, y1, p, Base), p, Base)

    return [x2,y2]


def double_addECbig(M, d, c, B):
    '''
    Works as double and add algorithm
    M is bignum point on curve
    d is bignum scalar
    c is curve parameters
    B is base

    Returns a bignum point on a curve c
    '''

    if d == [0]:
        return [0]
    elif d == [1]:
        return M
    else:
        quotient, remainder = divide(d, [2], B)
        if remainder == [1]:
            return addECbig(M, double_addECbig(M, subtract(d, [1], B), c, B), c, B)
        else:
            return double_addECbig(doublECbig(M, c, B), quotient, c, B)
    


if __name__ == "__main__":
    input = [997, 187, 658], [918, 431], [580, 560]
    
    d = tentoB(9, 16)
    M = [tentoB(number,16) for number in input[1]]
    C = [tentoB(number,16) for number in input[0]]

    output = doublECbig(M, C, 16)
    print(Bto10(output[0],16), Bto10(output[1],16))
    output = addECbig(M, output, C, 16)
    print(Bto10(output[0],16), Bto10(output[1],16))
    output = doublECbig(output, C, 16)
    print(Bto10(output[0],16), Bto10(output[1],16))

    output = double_addECbig(M, [6], C, 16)
    print(Bto10(output[0],16), Bto10(output[1],16))