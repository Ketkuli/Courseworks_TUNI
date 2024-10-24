'''
Write a library of functions for operations on positive big numbers expressed 
in base B (=integer>1; B itself is not a bignum). Include all nine that are 
def'd below. Use the small-endian order: the least significant digit (LSD) 
comes first in a list and the most sigfnicant digit (MSD) last. It works like 
this when N is a list containing a bignum:
'''

def tentoB(N,B):
    '''
    Convert a non-negative decimal number N to a bignum in base B. 
    Note: 0 must become [0], not empty list (which would work with the above 
    Bto10, though). 
    So, tentoB(541,5) returns [1, 3, 1, 4].
    To be useful, the library must include a version of both conversions 
    (10 -> B -> 10), where the decimal representation is a not a number 
    but a string.
    '''

    # Convert the N from string to integer:
    N = int(N)

    # Check the note:
    if N == 0:
        return [0]
    
    bigNumList = []

    # Find what power of B is larger than N:
    powerB = 0
    while N > B**powerB:
        powerB += 1
    
    # Largest power of B that fits into N is powerB-1
    # Iterate through numbers from powerB-1 to 0:
    remainder = N
    for i in range(powerB-1, -1, -1):
        divisor = remainder // (B**i)

        # This creates the list in reverse order than required
        bigNumList.append(divisor)
        remainder = remainder % (B**i)

    # Returning a reversed list to be as per the specs     
    return bigNumList[::-1]


def Bto10(N, B):
    # Return the decimal value of bignum N in base B.
    return sum(digit * B**i for i, digit in enumerate(N))


def EEA(A, B, Base, As=1, Bs=1):
    '''
    This is the Extended Euclidean algorithm implementation to work on bignum
    as per instructed in the exercise.
    
    M : Bignum and the number which to find the modular inverse
    N : Bignum and the p in mod p
    B : integer and the base for M.

    Ms and Ns are signatures to indicate negative or positive number. Default
    is positive unless otherwise stated just to get recursive call working!

    Returns GCD, M, Ms, N, Ns
    '''
    # For finding multiplicative inverse in field:
    # Base Case
    if A == [0]:
        return B, [0], As, [1], Bs

    BmodA = reduce(B, A, Base)

    # gcd, x1, y1 = gcdExtended(b % a, a)
    gcd, x1, x1s, y1, y1s = EEA(BmodA, A, Base, As, Bs)

    # Update x and y using results of recursive call
    # x = y1 - (b//a) * x1

    bFloorA, _ = divide(B, A, Base)
    bFloorATimesX1 = reduce(multiply(bFloorA, x1, Base), B, Base)
    x, xs = signedsubtract(y1, y1s, bFloorATimesX1, x1s, Base)

    # y = x1
    y = x1
    ys = x1s
 
    return gcd, x, xs, y, ys


'''
Given by teacher starts:
Input an "improper" bignum N (small-endian in base B) and 
return it in the normal form where each digit is 0..B-1 and the last one>0.
Return [0] if N=0. Declare error if N represents a negative number.
'''
def normalize(N, B):
    lenN = len(N)
    for i in range(lenN-1):   # Borrow from more significant side to make all non-negative
        if N[i] < 0:
            borrow = 1 + (-N[i]-1) // B # 
            N[i] += B * borrow
            N[i+1] -= borrow
    if N[-1] < 0:
        # Checking this in the beginning would not help when N[-2] is too far below zero.
        print ("The number is negative (resulting in ", N, ")")
        raise SystemExit

    for i in range(lenN-1, 0, -1): # remove leading zeros: leave N[0].
        if N[i]>0:
            break
        else:
            N.pop()
    carry = 0                   # carry excess values toward more significant side
    for i in range(len(N)): # first within the existing N,...
        N[i] += carry
        carry = N[i] // B
        N[i] %= B
    while carry > 0:        # ...and then extending N if needed
        N.append(carry % B)     # carry may be >= B, and .. 
        carry //= B             # ... then there is more to extend
    return N


# Invert bignum M modulo P in base B,
# assuming the gcd(M,P) equals 1.

def modinv(M, P, B):
    _, x, xs, _, _ = EEA(M,P,B)
    if xs < 0:                      # So, X := xs*x = -x < 0. Reduce it mod P:
        _,y = divide( x, P, B)      # y := x mod P = -X mod P; Now y is in range 0..P-1.
        x = subtract(P,y,B)         # x := P-y = P - (-X mod P ) = X mod P, in range 0..P-1.
    return x


# Given: absolute values M and N, with indication of their actual signs: Ms and Ns.
# Return the absolute value of M-N and the sign of M-N.

def signedsubtract(M,Ms,N,Ns,B):
    if Ms==0:
        if M != [0]: raise SystemExit("M is not zero but its sign is.")
        return N, -Ns
    if Ns==0:
        if N != [0]: raise SystemExit("N is not zero but its sign is.")
        return M, Ms
    comparison = compare(M,N)
    if Ms > 0:
        if Ns > 0:
            if comparison == 0:
                return [0], 0
            if comparison > 0:
                return subtract(M,N,B), 1   # M-N > 0
            else:
                return subtract(N,M,B), -1  # -(N-M) < 0
        else:
            return add(M,N,B), 1            # M-(-N) > 0
    else:
        if Ns > 0:
            return add(M,N,B), -1           # -(-M + N) < 0
        else:
            if comparison == 0:
                return [0], 0
            if comparison > 0:
                return subtract(M,N,B), -1  # -(-M-(-N)) < 0
            else:
                return subtract(N,M,B), 1   # -N-(-M) > 0

'''
Given by the teacher ends
'''


def compare(M, N):
    '''
    Return 1, if M>N,   0, if M=N,   -1, if M<N
    If M and N are normalized, comparison will work without knowing B.
    Assuming that both are the same base B and normalized.
    '''
    # This returns zero if both lists are same
    if M == N:
        return 0
    # Check if M has more elements than N, hence being larger
    elif len(M) > len(N):
        return 1
    # Check if N has more elements than M, hence being larger
    elif len(N) > len(M):
        return -1
    # Both are same lenght, need to do element wise comparison
    else:
        # This loops finds the difference and lists are not the same
        for i in range(-1, (-1*(len(M))-1), -1):
            if M[i] > N[i]:
                return 1
            elif M[i] < N[i]:
                return -1
            else: 
                continue


def add(M, N, B):
    '''
    Return a normalized sum M+N in base B.
    '''

    # Check which list is larger in elements using compare-function
    comparisionResult = compare(M, N)
    if comparisionResult == 0 or comparisionResult == 1:
        sumOfBigNum = M[:]
        additive = N[:]
    else:
        sumOfBigNum = N[:]
        additive = M[:]

    # Loop to add values from smaller list to larger list
    for i in range(len(additive)):
        sumOfBigNum[i] += additive[i]

    # Normalize the sumOfBigNum
    sumOfBigNum = normalize(sumOfBigNum, B)

    return sumOfBigNum


def subtract(M, N, B):
    '''
    Return a normalized difference M-N in base B.
    Check that M≥N. Soon you will also need a signed subtraction, 
    but concentrate on these functions now.
    '''
    # Check if M is larger or the same as N:
    comparisionResult = compare(M, N)
    if comparisionResult == 0 or comparisionResult == 1:
        resultBigNum = M[:]
        subtractive = N[:]
    else:
        # If unable to do subtraction, then returns M
        return M

    # Loop for subtraction
    for i in range(len(subtractive)):
        resultBigNum[i] -= subtractive[i]

    # Normalize the result:
    resultBigNum = normalize(resultBigNum, B)

    return resultBigNum


def multiply(M, N, B):
    '''
    Return a normalized product M*N in base B.
    '''
    multiplicationOfBigNum = [0 for element in range(len(M)*len(N))]

    for i in range(len(M)):
        for j in range(len(N)):
            multiplicationOfBigNum[i+j] += (M[i]*N[j])

    # Normalize the result:    
    multiplicationOfBigNum = normalize(multiplicationOfBigNum, B)
    
    return multiplicationOfBigNum


def modsubtract(M, N, P, B):
    '''
    Assuming M and N are within 0,...,P-1, return (normalized) difference 
    M-N mod P in base B. Note that P is a bignum.
    '''
    # Check if M is larger or the same as N:
    comparisionResult = compare(M, N)
    # Case when M is larger or equal to N:
    if comparisionResult == 1 or comparisionResult == 0:
        return subtract(M,N,B)
    else:
        return subtract(add(M,P,B),N,B)


def convert(N,B1,B2):
    '''
    Bignum N, given in base B1 is returned in base B2.
    '''

    x = [0]
    for digit in reversed(N):
        x = multiply(x, [B1], B2)
        x = add(x, [digit], B2)
    return x


def divide(M, N, B):
    '''
    Provided by the teacher. Gives the integer quotient and remainder when 
    dividing a bignum by a smaller one using the algorithm familiar from the 
    elementary school.
    '''

    if N==[0]:
        raise ValueError("Division by zero")
    Q = []              # quotient
    R = normalize(M,B)  # remainder
    N_digit = N[-1] # most significant digit of the divisor
    N_len = len(N)  # divisor length
    countinner=0        # These two counters are for those of you
    countouter=0        # ... who want to study and improve the performance.

    # Repeat as long as the remainder didn't get below divisor
    while compare(R, N) >= 0:
        countouter += 1
        # Estimate the position for the next quotient digit 
        # and get the most significant digit (or two) of the remainder
        if R[-1] >= N_digit:
            estimate = len(R) - N_len 
            R_digit = R[-1]
        else:
            estimate = len(R) - N_len - 1
            R_digit = B * R[-1] + R[-2]

        # Estimate the next digit in the quotient using Python's division
        Q_digit_estimate = min(R_digit // N_digit, B-1)

        # Create a trial divisor
        trial = [0] * estimate + [Q_digit_estimate]

        # Make a (sub)trahend and adjust it and the trial as long as trahend is too big
        trahend = multiply(trial, N, B)
        while compare(trahend, R) > 0:
            countinner += 1
            Q_digit_estimate -= 1
            if Q_digit_estimate == 0: # if this goes to zero, we must move to lower significance
                trial.pop()
                trial[-1] = B-1        # ... and start from the biggest value there
                Q_digit_estimate = B-1
            else:
                trial[-1] = Q_digit_estimate

            trahend = multiply(trial, N, B) # This will be subtracted if looping does not continue

        R = subtract(R, trahend, B)
        Q = add(Q, trial, B)
    return Q, R # , countouter, countinner  # See these two to know where the time was spent.


def reduce(M, P, B):
    '''
    Does a modular reduction:
    '''
    comparisionResult = compare(M, P)
    if comparisionResult == -1:
        return M
    else:
        Q, R = divide(M, P, B)
        return R


if __name__ == '__main__':
    # Tests:
    integerTest = tentoB(541, 5)
    print(integerTest) # Should be [1, 3, 1, 4]

    stringTest = tentoB('541', 5)
    print(stringTest) # Should be [1, 3, 1, 4]

    stringTest = tentoB('541', 10)
    print(stringTest) # Should be [1, 4, 5]

    number = Bto10([1, 3, 1, 4], 5) 
    print(number) # Should be 541

    # M is smaller
    compareTest = compare([1, 2, 1, 4], [1, 3, 1, 4])
    print(compareTest) # Should be -1

    # M is larger
    compareTest = compare([1, 4, 1, 4], [1, 3, 1, 4])
    print(compareTest) # Should be 1

    # M is shorter
    compareTest = compare([1, 4, 1], [1, 3, 1, 4])
    print(compareTest) # Should be -1

    # N is shorter
    compareTest = compare([1, 4, 1, 4], [1, 4, 1])
    print(compareTest) # Should be 1

    # Lists are same
    compareTest = compare([1, 4, 1], [1, 4, 1])
    print(compareTest) # Should be 0


    # Test for addition:
    additionTest = add([1,2,3],[1,1,1], 5)
    print(additionTest) # should be [2,3,4]   

    additionTest = add([1,2,3],[1,1,2], 5)
    print(additionTest) # should be [2,3,0,1] 


    # Test for substraction:
    subtractTest = subtract([1,2,3],[1,1,1], 5)
    print(Bto10([1,2,3], 5)) # 86
    print(Bto10([1,1,1], 5)) # 31
    print(subtractTest) # Should be [0,1,2]
    print(Bto10([0,1,2], 5)) # 55


    # Tests for multiplication:
    a = [1,2] # 11 in base 5
    b = [2,1] # 7 in base 5
    c = [1,3,1,4] # 541 in base 5
    d = tentoB(10, 5) # [0,2] 
    multiTest = multiply(a,b, 5)
    print(multiTest)
    print(Bto10(multiTest,5)) # Should be 77
    
    multiTest = multiply(c,d, 5)
    print(multiTest)
    print(Bto10(multiTest,5)) # Should be 5410


    # Tests for modsubtract:
    a = [1, 3, 1, 4] # 541 in base 5
    b = [1, 2, 1, 4] # 536 in base 5
    P = tentoB(550,5)

    # Case when M is larger than N:
    modResult = modsubtract(a,b,P,5)
    print(modResult) # [0, 1] as 541 - 536 mod 550 is 5

    # Case when N is larger than M:
    modResult = modsubtract(b,a,P,5)
    print(modResult) # [0, 4, 1, 4] 
    # Check if correct:
    print(tentoB((536-541)%550, 5) == modResult) # True
    

    # Testcase for divide:
    a = 550
    p = 500

    quontinent, remainder = divide(tentoB(a,5),tentoB(p,5),5)
    print(Bto10(remainder,5) == 50)
    print(reduce(tentoB(a,5),tentoB(p,5),5) == tentoB(50, 5))