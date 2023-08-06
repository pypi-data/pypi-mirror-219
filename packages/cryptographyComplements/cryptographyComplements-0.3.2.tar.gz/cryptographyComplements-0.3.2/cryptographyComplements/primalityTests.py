"In this script you can find all the Primality Test functions."

def LucasLehmerPrimalityTest(n:int):
    "This primality test is deterministic, and is valid only for Mersenne numbers: 2^n - 1, to check whether a mersenne number is prime or not."

    from cryptographyComplements.mathFunctions import MersennePrime

    mersenne = pow(2, n) - 1 # we define it here to avoid repetitions

    lucaslehmerSequence = MersennePrime.LucasLehmerModuloNumbers(n-1, mersenne)

    if lucaslehmerSequence[n-2] % mersenne == 0:
        return True
    
    return False
    
def FermatPrimalityTest(n: int, k: int) -> bool:
    "Given an integer n and k: the number of times to test for primality, the function will return false and it's a composite number or it will return true and it would be a prime number or a Carmichael number. \n\nThis primality test is probabilistic."

    from cryptographyComplements.mathFunctions import FermatLittleTheorem
    import random

    for i in range(k):

        a = random.randint(2, n-1)

        if FermatLittleTheorem(a, n) != 1:
            return False

    return True


def MillerRabinPrimalityTest(n: int, k: int) -> bool:
    "Given a number: n, to check and k: the number of test to execute, see whether the number is a possible prime or a composite. This primality test is probabilistic."

    import random

    if n < 2 or n % 1 != 0:
        return False

    if n in (2, 3): # this numbers need to be checked here to avoid endless while loop for 2, Value Error for 3 | The causes are written on Miller-Rabin documentation page
        return True
    
    q = (n - 1) // 2
    p = 1

    while q % 2 == 0:
        q //= 2
        p += 1

    for i in range(k):
        a = random.randint(2, n - 2)

        x = pow(a, q, n)

        for j in range(p):
            y = pow(x, 2, n)

            if y == 1 and x != 1 and x != (n-1):
                return False
        
            x = y

        if y != 1:
            return False
        
    return True