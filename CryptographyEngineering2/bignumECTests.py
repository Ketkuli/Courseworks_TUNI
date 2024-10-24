from bignumEC import *
from bignum import *

Base = 16

"""
Test data for addEC:
"""
# Each element has this form
#	[p,a,b],[x1,x2], [y1,y2], [sum1, sum2]

additions = [
	[[997, 187, 658], [0, 0], [0, 0], [0, 0]], 
	[[997, 187, 658], [0, 0], [259, 116], [259, 116]], 
	[[997, 187, 658], [918, 431], [0, 0], [918, 431]], 
	[[997, 187, 658], [918, 431], [918, 566], [0, 0]], 
	[[997, 187, 658], [918, 431], [918, -431], [0, 0]], # The same as above but with negative sign.
                                                        # This need NOT go right.

	[[997, 187, 658], [918, 431], [259, 116], [954, 104]], 
	[[997, 641, 72], [895, 33], [179, 724], [124, 316]], 
	[[997, 449, 85], [351, 99], [861, 209], [48, 25]], 
	[[997, 812, 126], [887, 690], [989, 842], [865, 27]], 
	[[1009, 506, 186], [251, 445], [23, 981], [525, 801]], 
	[[1009, 273, 538], [459, 851], [109, 928], [615, 717]], 
	[[1009, 761, 603], [472, 594], [709, 484], [831, 654]], 
	[[1009, 391, 602], [136, 943], [16, 70], [652, 449]], 
	[[1013, 742, 812], [893, 9], [868, 790], [638, 534]], 
	[[1013, 507, 388], [910, 565], [950, 449], [610, 591]], 
	[[1013, 936, 282], [880, 603], [184, 684], [157, 697]], 
	[[1013, 139, 838], [797, 515], [90, 498], [373, 587]], 
	[[1019, 53, 581], [787, 47], [37, 382], [461, 609]], 
	[[1019, 397, 550], [963, 403], [570, 436], [347, 82]], 
	[[1019, 300, 858], [486, 764], [744, 680], [656, 808]], 
	[[1019, 569, 886], [798, 700], [211, 557], [364, 916]], 
	[[1021, 141, 798], [305, 689], [665, 145], [800, 59]], 
	[[1021, 292, 323], [515, 111], [981, 210], [193, 251]], 
	[[1021, 939, 907], [860, 208], [490, 479], [893, 277]], 
	[[1021, 773, 243], [624, 54], [177, 637], [952, 488]]
]

"""
Test data for doublEC:
"""
# Each element has this form
#	[p,a,b],[x1,x2], [double1, double2]

doublings = [
	[[997, 187, 658], [0, 0], [0, 0]], 
	[[997, 187, 658], [918, 431], [580, 560]], 
	[[997, 641, 72], [895, 33], [631, 760]], 
	[[997, 449, 85], [351, 99], [268, 801]], 
	[[997, 812, 126], [887, 690], [12, 98]], 
	[[1009, 506, 186], [251, 445], [426, 651]], 
	[[1009, 273, 538], [459, 851], [380, 492]], 
	[[1009, 761, 603], [472, 594], [906, 946]], 
	[[1009, 391, 602], [136, 943], [45, 902]], 
	[[1013, 742, 812], [893, 9], [452, 764]], 
	[[1013, 507, 388], [910, 565], [554, 363]], 
	[[1013, 936, 282], [880, 603], [103, 194]], 
	[[1013, 139, 838], [797, 515], [438, 136]], 
	[[1019, 53, 581], [787, 47], [776, 979]], 
	[[1019, 397, 550], [963, 403], [132, 812]], 
	[[1019, 300, 858], [486, 764], [214, 638]], 
	[[1019, 569, 886], [798, 700], [390, 283]], 
	[[1021, 141, 798], [305, 689], [646, 231]], 
	[[1021, 292, 323], [515, 111], [117, 50]], 
	[[1021, 939, 907], [860, 208], [8, 938]], 
	[[1021, 773, 243], [624, 54], [342, 591]]
]


"""
Test calls:
"""
def testAddEC(testData):
    # Tests for the addEC function:
    print("\nTesting addition in Elliptic curve with BigNum:")
    testNumber = 1
    faulty = 0
    for input in testData:
        c = [tentoB(number,Base) for number in input[0]]
        x = [tentoB(number,Base) for number in input[1]]
        y = [tentoB(number,Base) for number in input[2]]
        result = [tentoB(number,Base) for number in input[3]]
        
        newPoint = addECbig(x,y,c,Base)
        if  newPoint != result:
            #print(newPoint, result)
            print(f"Test for input: {input} on row: {testNumber} is not ok!")
            faulty += 1
        testNumber += 1

    if faulty == 0:
        print("All tests passed!")


def testDoubleEC(testData):
    # Tests for the addEC function:
    print("\nTesting doubling in Elliptic curve:")
    testNumber = 1
    faulty = 0
    for input in testData:
        c = [tentoB(number,Base) for number in input[0]]
        x = [tentoB(number,Base) for number in input[1]]
        result = [tentoB(number,Base) for number in input[2]]

        if doublECbig(x, c, Base) != result:
            print(f"Test for input: {input} on row: {testNumber} is not ok!")
            faulty += 1
        testNumber += 1

    if faulty == 0:
        print("All tests passed!")


def main():
    testAddEC(additions)
    testDoubleEC(doublings)


if __name__ == "__main__":
    main()