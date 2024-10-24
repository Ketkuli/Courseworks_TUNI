# Ex6. Bignum operations.

Write a library of functions for operations on _positive_ big numbers expressed in base B (=integer>1; B itself is not a bignum). Include all nine that are def'd below. Use the small-endian order: the least significant digit (LSD) comes first in a list and the most sigfnicant digit (MSD) last. It works like this when N is a list containing a bignum:

Return the decimal value of bignum N in base B.  
**def Bto10(N, B):**  
&nbsp;&nbsp;&nbsp;&nbsp;return sum(digit * B**i for i, digit in enumerate(N))

>For example, Bto10( [1, 3, 1, 4], 5) gives 541 because [1, 3, 1, 4] as a bignum means 1 + 3·5 + 1·52 + 4·53 = 1 + 3·5 + 1·25 + 4·125 = 541. You can see the similarity to polynomials.

You will include division later but now you need the other basic operations. The following is actually for testing only, but it is the first one you should implement:

**def tentoB(N, B):**
&nbsp;&nbsp;&nbsp;&nbsp;Convert a non-negative decimal number N to a bignum in base B. Note: 0 must become [0], not empty list (which would work with the above Bto10, though). So, tentoB(541,5) returns [1, 3, 1, 4].

To be useful, the library must include a version of both conversions (10→B→10), where the _decimal representation is a not a number but a string_ (which is a "bigendian bignum" in base 10, like "541"=1 + 4·10 + 5·102). Because Python can deal with arbitrary large integers you need   
not bother too much with this right now—also meaning that you can use the above two conversions for testing. However, when you reach the programming assignment you will input and output hexadecimal strings (i.e., you need 16→B→16, but they are given to you). The hexadecimals may be converted to a large base like 1000 and back and here is a general conversion:

Bignum N, given in base B1 is returned in base B2.  
**def convert(N,B1,B2):**  
&nbsp;&nbsp;&nbsp;&nbsp;x = [0]  
&nbsp;&nbsp;&nbsp;&nbsp;for digit in reversed(N):  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;x = multiply(x, [B1], B2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;x = add(x, [digit], B2)  
&nbsp;&nbsp;&nbsp;&nbsp;return x

The conversion is done very simply by treating N as a polynomial and computing it at _point_ B1 using _arithmetic_ in base B2. Digits of N may far exceed the base B2, but the following functions will treat such overflows.

So, after tentoB(N, B), implement these functions:

**def normalize(N, B):**  
Well, this function is given to you [here](https://moodle.tuni.fi/mod/resource/view.php?id=2842542), and it is an essential helper function for the actual operations, because they need not care about "overflow" of their digits (how much would they create maximally?). Normalization modifies an "improper" bignum N to have each digit within 0..B-1 and the MSD>0. The function firsts uses *borrowing* to make all digits positive. It outputs an error if this leads to a negative MSD. Then it uses *carrying* to make all digits less than B. This may require one or more new digits to the MSD end. Leading zeros are removed after borrowing before carrying, using the method .pop().

**def compare(M, N):**  
&nbsp;&nbsp;&nbsp;&nbsp;Return 1, if M>N, 0, if M=N, −1, if M<N  
&nbsp;&nbsp;&nbsp;&nbsp;If M and N are normalized, comparison will work without knowing B.

**def add(M, N, B):**  
&nbsp;&nbsp;&nbsp;&nbsp;Return a normalized sum M+N in base B.  
  
**def subtract(M, N, B):**  
&nbsp;&nbsp;&nbsp;&nbsp;Return a normalized difference M−N in base B.  
&nbsp;&nbsp;&nbsp;&nbsp;Check that M≥N. Soon you will also need a signed subtraction, but concentrate on these functions now.  
  
**def multiply(M, N, B):**  
&nbsp;&nbsp;&nbsp;&nbsp;Return a normalized product M*N in base B.

**def modsubtract(M, N, P, B):**  
&nbsp;&nbsp;&nbsp;&nbsp;Assuming M and N are within 0,...,P-1, return (normalized) difference M−N mod P in base B. Note that P is a bignum.

All the other functions are very straightforward with the help of normalization. The last function is just somewhat special at this stage, because of the modularity. If you inspect the situation carefully, you'll notice that depending on the relative size of M and N you will only need to write two calls to subtract(), and one call to add().

### Ex7. Bignum division, reduction, EC operations.

[Here](https://moodle.tuni.fi/mod/resource/view.php?id=2842543) is a code that gives the integer quotient and remainder when dividing a bignum by a smaller one using the algorithm familiar from the elementary school. The notable exception is that finding the next digit to the quotient has to be done with some searching. Here a trial is calculated for it and trial subtrahend trahend is probed until a proper trial is found to be the next digit. This search should be made faster. Can you do something to improve it?

Division readily gives you the modular reduction, but you may write it as a function **reduce(M,P,B)**. If M is already less than P, you avoid calling divide().

Assume you already have the inversion function from Ex8. **Modify your EC operations from Hp5 to run with bignums.** You can of course do Ex8 at this moment, but the idea is that you prepare all the rest for bignums and work on the inversion next week. Note that unlike the EEA in Ex8, you need not bother with negative numbers in EC operations. Just use your modsubtract() when computing the differences. If a number can be out of the modular range, use your reduce() (or just divide()) before calling any arithmetic functions.

### Ex8. Bignum modular inversion.

Modify your EEA from Ex1 to run with bignums. The algorithm will necessarily output a negative number as one of the Bezout coefficients. This causes some trouble, because until now there is no representation of negative integers. The need is a very specialized one, and so it suffices to take it as a special case in the EEA and subtraction routine: Each bignum that can be negative, travels as an absolute value _accompanied_ by a sign, and when such a number is treated, different cases with the sign are separated. Eventually no negative numbers will be treated in your earlier library from Ex6 and Ex7. Note that in EAA the quotient and remainder will always be non-negative, but any of the auxiliary variables can be negative, and some certainly will be.

So, for instance in base 10 the number −52 is represented with the bignum [2,5] accompanied by its sign −1, using two variables, a list and an integer. Similarly [2,5] with +1 would be 52, and you cannot drop out the +1 in such a context in the way you are used to writing 52 instead of +52.

[Here](https://moodle.tuni.fi/mod/resource/view.php?id=2842545)** is the code for signedsubtract(M,Ms,N,Ns,B) that you will need to call from your EEA, when doing the subtractions with the sign-accompanied values. The same file contains modinv(M,P,B), which is the ultimate goal of this exercise. It is given to you because of a small complication with the possible negative coefficient in the Bezout identity, before returning it as an inverse of M modulo P. As an example, consider the case of inverting 2 modulo 7. The Bezout identity is gcd(2,7) = 1 = (−3)·2+(1)·7. Taken modulo 7 this gives you 1 = (−3)·2, and the inverse of 2 must be reduced modulo 7 from being (−3) to be −3+7=4.

### Ex9. EC scalar multiplication with bignums.

Using the same idea as in square&multiply in Ex1, write a script for scalar multiplication of EC elements, that is, an algorithm for double&add.

### Programming assignment. Sign with ECDSA.

Create your own ECDSA **public key** and **a script** to make ECDSA signatures using bignums but the fairly small 112-bit group taken from the [old standard SEC2](https://www.secg.org/SEC2-Ver-1.0.pdf) from year 2000 (see section 2.2.1). The curve E is defined by these values

&nbsp;&nbsp;&nbsp;&nbsp;p = 0xDB7C2ABF62E35E668076BEAD208B  
&nbsp;&nbsp;&nbsp;&nbsp;a = 0xDB7C2ABF62E35E668076BEAD2088  
&nbsp;&nbsp;&nbsp;&nbsp;b = 0x659EF8BA043916EEDE8911702B22

Note that a is very close to p. You can subtract the entire numbers (or just 0xB−0x8) in a Python shell to see that a = p−3 = −3 mod p. In your script you will work with positive numbers only, and you cannot use these over 100-bit numbers as integers. You must input them as strings and convert them to your base, and then do all calculations with your bignum library. In the end the result (a pair of integers) must be converted back to hexadecimals.

The group definition also needs the generator G = (Gx, Gy) of a subgroup of E. Here are the coordinates. (The standard gives Gx as 0x0948... but the initial zero would require normalization in hexto16() below)

&nbsp;&nbsp;&nbsp;&nbsp;Gx = 0x9487239995A5EE76B55F9C2F098  
&nbsp;&nbsp;&nbsp;&nbsp;Gy = 0xA89CE5AF8724C0A23E0E0FF77500

Then you need the order of G, i.e. the size of the subgroup it generates. This is denoted by n in the standard, but by q in the Paar's book. So, let's use q.

&nbsp;&nbsp;&nbsp;&nbsp;q = 0xDB7C2ABF62E35E7628DFAC6561C5

Also, you may have noted that Paar uses A for the generator G. You can choose your notation.

**What is your own public key?** It is the key you obtain with the above curve parameters and using again your student number. Take the numeric part of your student number, interpret it directly as a hexadecimal number, and use it as your private key (the random integer d) in the ECDSA key generation algorithm. Submit your entire student number and your hexadecimally written public key as the first two lines in your ECDSA signature code in this format:  

&nbsp;&nbsp;&nbsp;&nbsp;snum='H123456789'  
&nbsp;&nbsp;&nbsp;&nbsp;pubkey = ['4A344D697065350237C1CA5A7F0C', 'F6E49D16FE078145D45441FB859']  

That key is real for that student number, to enable testing your key-creating function. Note, your submission should not include the function, just the resulting key.  

**What to sign?** Your ECDSA signing function must input the message as a nonempty hexadecimal string, without initial '0x'. It represents a hash value of a meaningful message. (You need not plug in your AES-Keccak from CE1.) Just input a hexstring into your signing function and convert it to a bignum. Here is the function for the conversion, and its inverse.  

A string N of hexadecimals (without initial 0x) into a bignum in base 16  
**def hexto16(N):**  
&nbsp;&nbsp;&nbsp;&nbsp;return [int(h,16) for h in N[::-1]] # reverse order of the argument string  
  
A bignum N in base 16 into a string of hexadecimals  
**def from16tohex(N):**  
&nbsp;&nbsp;&nbsp;&nbsp;return ''.join([hex(i)[2].upper() for i in N[::-1]])

Note, that these resemble conversions **Bto10** and **tentoB** of Ex6, which dealt with numbers, not strings. If you need input or output in decimals, e.g. for testing, you must include those conversions in your submitted file. The explanation of ''.join([hex(i)[2]... above is this: an empty string '' has a method join which inputs a list and returns a string of its elements concatenated. The elements are individual hex characters made from integers i (assumedly within 0..15) with function hex, where [2] takes only the third character from the representation that starts with 0x.

**Summary:** Your code must use the functions created in programming tasks Ex6,...,Ex9, but your submission does not include them. Instead it must import the module bignum, which will contain the teacher's version of the same functions. The bignum EC functions provided in bignum are:

&nbsp;&nbsp;&nbsp;&nbsp;addECbig(v, w, c, Base) -> v+w, with curve c=[p,a,b]  
&nbsp;&nbsp;&nbsp;&nbsp;doublECbig(v, c, Base) -> v+v  
&nbsp;&nbsp;&nbsp;&nbsp;double_addECbig(A, k, c, Base) -> scalar k times generator A

Import also random (and possibly os or sys if you need them), but nothing else. Continue your code by assigning the curve parameters as given above and defining all functions you use for conversions. Return the ECDSA signature as two strings of hexadecimals from function ECDSA(privkey, hash, B), where privkey and hash are strings of hexadecimals, and B is the base for the bignum operations. So, do the parameter conversions inside the ECDSA function.

**Checking** the functionality of your submission happens by first checking the validity of your public key. Then a few signatures are created and verified, both with your keys and others, for varying hash values. You can do such checks yourself against the [**calculator**.](https://tie-sec.rd.tuni.fi/cren/index.php?ex=2016) The teacher will use a [script like this](https://moodle.tuni.fi/mod/page/view.php?id=2958143), calling your file preferrably by your last name (the script formatting is intentionally copied from MS Visual Studio Code, but Moodle does its own things on top of that.)

**End note.** You may find it convenient to generate the ephemeral key (kE , with 0 < kE < q) as a random _bit string_ and convert that to its representation in arbitrary base. Here are functions for that purpose. The first one is just a helper, using one of the functions above:

 Convert a string of hexadecimals H (without initial 0x) to its representation in base B.  
**def hextoB(H,B):**  
&nbsp;&nbsp;&nbsp;&nbsp;if B == 16:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return hexto16(H)  
&nbsp;&nbsp;&nbsp;&nbsp;else:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return convert(hexto16(H),16,B)  
  
Convert a bit string K to its representation in base B, via hexadecimals.  
**def bitstoB(K,B):**  
&nbsp;&nbsp;&nbsp;&nbsp;res = ''  
&nbsp;&nbsp;&nbsp;&nbsp;while len(K) % 4 != 0: # Pad K to a length that is a multiple of 4.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;K = '0'+K  
&nbsp;&nbsp;&nbsp;&nbsp;for i in range(0, len(K), 4): # Convert each chunk of four bits to an integer.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;chunk = K[i:i + 4]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dec = int(chunk, 2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;res += hex(dec)[2:].upper() # join them into a hex string  
&nbsp;&nbsp;&nbsp;&nbsp;return hextoB(res,B)
