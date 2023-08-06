"In this script you can find all the mathematical functions relative to Number Theory."

def EulerTotientFunction(n: int) -> int:
    "Calculate, from a given number, the Euler Totient function."
    
    if n <= 1:
        if n == 1:
            return 1
        return None
    
    factorization = FactorizationMethods.TrialDivision(n, n)

    relativePrime = n

    used = []

    for prime in factorization:
        if prime in used:
            continue

        relativePrime *= ((prime-1)/prime)
        
        used.append(prime)


    return int(relativePrime)

def EuclideanAlgorithm(a: int, b: int) -> int:
    "Given two numbers, a and b, calculate their Great Common Divisor."

    import math

    q = math.floor(a/b)
    r = a-(b*q)

    if r == 0:
        return b

    q2 = math.floor(b/r)
    r2 = b-(q2*r)

    if r2 == 0:
        return q2

    previous = [q, r, q2, r2]

    while True:
        q = math.floor(previous[1]/previous[3])
        r = previous[1]-(q*previous[3])

        if r == 0:
            return previous[3]
        
        previous.pop(0)
        previous.pop(0)
        previous.append(q)
        previous.append(r)

def ExtendedEuclideanAlgorithm(a: int, b: int) -> tuple:
    "Given two numbers, a and b, calculate their Great Common Divisor and the coefficients of Bézout's identity"

    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        r = a % b
        x = x0 - (a // b)*x1
        y = y0 - (a // b)*y1
        a, b, x0, x1, y0, y1 = b, r, x1, x, y1, y

    return a, x0, y0 # a is the GCD of a and b

def MultiplicativeOrder(a: int, n: int) -> int:
    "Calculate the multiplicative order of a in mod n. The function if n is relatively prime to a it will return the Carmichael function, in any other case it will use the bruteforce algorithm."

    if EuclideanAlgorithm(a, n) == 1:
        Carmichael = CarmichaelFunction(n)
        return Carmichael
    
    k = 0

    while pow(a, k, n) != 1:
        k += 1

    return k


class DiscreteLogarithm:
    "This class contains all the Discrete Logarithm algorithms to solve the Discrete Logarithm Problem: g^x ≡ h (mod p) or g^X = h in Fp"

    def BruteforceAlgorithm(g: int, h: int, p: int) -> int:
        "Using the Bruteforce algorithm, solve the Discrete Logarithm Problem. \n\nThe functions search for all numbers up to p. If there isn't a solution or it's greater than p the algorithm will return None."

        for x in range(0, p+1):

            if pow(g, x, p) == (h % p):
                return x

        return None

    def ShanksBabyStepGiantStepAlgorithm(g:int, h:int, p:int) -> int:
        "Using the Shanks Baby-Step Giant-Step algorithm, solve the Discrete Logarithm Problem: g^x ≡ h (mod p) \n\nThe function returns None if there isn't a solution to the Discrete Logarithm."
        
        import math
        n = math.floor(math.sqrt(MultiplicativeOrder(g, p))) + 1

        u = pow(g, EulerTotientFunction(p)-n, p)

        l1, l2 = [], []

        for i in range(0, n+1):
            l1.append(pow(g, i, p))

        for j in range(0, n):
            keep = (h*(pow(u, j))) % p
            l2.append(keep)
            if keep in l1:
                break

        try:
            value = l1.index(keep)
        except ValueError:
            return None

        value2 = l2.index(keep)

        x = value + (n * value2)

        return x
    
def ChineseRemainderTheorem(congruences:list, modulo: list) -> int:
    "From a list of congruences and a list of modulos, tuples are accepted too, of the same lenght, calculate the Chinese Remainder Theorem. \n\nIf there is a solution it will be returned as a number, but if there isn't it will return None."
    
    from cryptographyComplements.tools import Numbers

    try:
        for i in range(0, len(modulo)):
            if i == (len(modulo)-1):
                break

            try:
                # check if the numbers are relatively prime, if not there isn't a solution to the congruence
                if EuclideanAlgorithm(int(modulo[i]), int(modulo[i+1])) != 1:
                    return None

            except ValueError:
                return None

    except TypeError:
        return None
          
    M = Numbers.listMultiplication(modulo)
    totalM = []

    for i in modulo:
        moduloI = M/i
        totalM.append(moduloI)

    moduloInverses = []
    for i in range(0, len(congruences)):
        moduloI = ExtendedEuclideanModularMultiplicativeInverse(totalM[i], modulo[i])

        if moduloI == None: # If there is no inverse modulo, then there isn't a solution for that congruence
            return None

        moduloInverses.append(moduloI)

    y = 0
    for i in range(0, len(congruences)):
        y += (moduloInverses[i] * totalM[i] * congruences[i])

    return int((y % M))

class MersennePrime:
    "In this class you can find all the math functions about Mersenne numbers: 2^n - 1"

    def LucasNumbers(limit: int) -> list:
        "Calculate the Lucas Numbers from a given number in limit: it defines at what number the algorithm stops."

        sequence = [2, 1, 3]
        x0, x1 = 1, 3

        for i in range(limit):

            x = x0 + x1
            x0 = x1
            x1 = x

            sequence.append(x)

        return sequence

    def LucasLehmerNumbers(limit: int) -> list:
        "Calculate the Lucas-Lehmer Numbers from a given number in limit: it defines when the algorithm stops."

        sequence = [4]
        x = 4

        for i in range(1, limit):

            x = pow(x, 2) - 2

            sequence.append(x)

        return sequence
    
    def LucasLehmerModuloNumbers(limit: int, modulo: int) -> list:
        "This version of the Lucas-Lehmer numbers sequence uses the limit and the modulo too. The modulo needs to be added to reduce the computational time required. \n\nUse this only for the Lucas-Lehmer primality test."

        sequence = [4]
        x = 4

        for i in range(1, limit):

            x = ((pow(x, 2)-2) % modulo)
            sequence.append(x)

        return sequence

def ExtendedEuclideanModularMultiplicativeInverse(a: int, m: int) -> int:
    "Calculate the modular multiplicative inverse of the number an integer a modulo m. The functions uses the coefficients of the Bézout identity to calculate it. \n \nNote: The function will return None if there isn't a inverse modulo."

    gcd, x, y = ExtendedEuclideanAlgorithm(a, m)


    if gcd != 1:
        return None # this happens only if there isn't an inverse modulo
    
    return x % m

def FermatLittleTheorem(a:int, n:int) -> int:
    "From a given integer and a modulo, calculate the Fermat Little Theorem. \n\nNote: The function will return 1 if n is either a prime number or a carmichae number."

    return pow(a, n-1, n)

def MultiplicativePersistence(num: int) -> int:
    "From a given integer in input, calculate the multiplicative persistence. The function will return the number of steps required."

    result, steps = 1, 0

    for i in str(num):
        result = int(i) * result

    steps += 1


    while len(str(result)) != 1:
        num = result
        result = 1        
        for i in str(num):

            result *= int(i)

        steps += 1

    return steps

def FermatEulerTheorem(a:int, n:int) -> int:
    "From a given two given integers calculate Fermat-Euler Theorem. \n\nNote: a is the number and n is the modulo. Moreover, the function will return 1 if and only if a and are coprime positive."
    return pow(a, EulerTotientFunction(n), n)

def EulerFormulaForPQ(p: int, q: int) -> bool:
    "The Euler Formula from two given integers p and q returns True if the congruence a^((p-1)(q-1)/g) mod pq is congruent to 1 and False if it's not."

    if p == 2 or q == 2:
        return FermatEulerTheorem(p, q)

    g = EuclideanAlgorithm(p-1, q-1)

    a = pow(2, (p-1)*(q-1)//g, p*q) # 2 can be set, to the base, because is coprime with p*q if p or q isn't 2

    if EuclideanAlgorithm(a, p*q) != 1:
        return False

    if pow(a, (p-1)*(q-1)//g, p*q) != 1:
        return False

    return True

def PrimeNumberTheorem(n: int) -> float:
    "Calculate the Prime Number Theorem for n using n/ln(n). The value returned is an approximation."

    import math

    if n <= 1:
        return 0.0
    return n / (math.log(n)) # here log is the natural logarithm ln(x)

from cryptographyComplements.primalityTests import MillerRabinPrimalityTest
class FactorizationMethods:
    "This class contains factorization methods, including special purpose and general purpose ones."

    def TrialDivision(n: int, maxN: int) -> list:
        "This factorization method uses the trial division and it's a special purpose algorithm, so it's not recommended for numbers that could be possibly be prime, or for large composites.\n\nNote: maxN defines the maximum value for which will be searched primes that factorize n. It has been implemented to avoid large computations. \nIf you want to search up to n, just put maxN=n"

        from cryptographyComplements.tools import Numbers

        if MillerRabinPrimalityTest(n, 100):
            return [n]        

        primeFactors = []
        keep = n

        for i in range(2, maxN+1):

            flag = False

            if n / i % 1 == 0:

                for prime in primeFactors:
                    if i/prime % 1 == 0:
                        flag = True
                        break

                if not flag:
                    primeFactors.append(i)
                    n /= i

                    while n/i % 1 == 0:
                        primeFactors.append(i)
                        n /= i


            if Numbers.listMultiplication(primeFactors) == keep:
                break

        return primeFactors

    def PollardRhoFactorizationAlgorithm(n: int) -> int:
        "The Pollard Rho factorization algorithm is a special purpose algorithm \n\n The algorithm returns a prime factor of n."

        def gx(x, n):
            return (x**2 + 1) % n

        x = 2
        y = 2
        d = 1

        while d == 1:
            x = gx(x, n)
            y = gx(gx(y, n), n)
            
            d = ExtendedEuclideanAlgorithm(abs(x-y), n)[0]

        if d == n:
            return None
        
        return d

    def PollardFactorizationAlgorithm(n: int) -> int:
        "The Pollard's p-1 algorithm is a factorization algorithm for special purpose \n\n The algorithm returns a prime factor of n."

        a = 2
        for j in range(2, n):
            a = pow(a, j, n)
            d = ExtendedEuclideanAlgorithm(a-1, n)[0]
            if 1 < d < n:
                return d

    def FermatFactorizationAlgorithm(n: int) -> None|tuple|bool:
        "The Fermat factorization algorithm is exponential and special purpose. \n\nIf n it's not odd, it will return None, in any other case it will return a nontrivial divisor of n or it will return True if n is prime."

        import math

        if n % 2 == 0:
            return None
        
        rad = math.ceil(math.sqrt(n))
        maxN = math.ceil((n+9)/6)

        steps = 1

        if n % 4 == 1:
            steps = 2
            if rad % 2 == 0:
                rad += 1

        elif n % 3 == 2:
            steps = 3

            while rad % 3 != 0:
                rad += 1

        for a in range(rad, maxN+1, steps):
            b = math.sqrt(a**2 - n)

            if b % 1 == 0:
                return (int(a-b), int(a+b))
            
        return True

def CarmichaelFunction(n: int) -> int:
    "Calculate the Carmichael function for n."

    from cryptographyComplements.tools import Numbers

    factorization = FactorizationMethods.TrialDivision(n, n)

    powers = {}

    for prime in factorization:
        try:
            powers[prime] += 1

        except KeyError:
            powers[prime] = 1

    phis = []

    for prime in powers.keys():

        if prime == 2 and powers[prime] >= 3:
            phis.append((EulerTotientFunction(pow(prime, powers[prime]))*(1/2)))

        else:
            phis.append(EulerTotientFunction(pow(prime, powers[prime])))

    return Numbers.lcm_list(phis)

def BertrandPostulate(n: int) -> int:
    "From a given integer n > 1 find the first prime number that verifies the inequality: n < p < 2n."

    from cryptographyComplements.primalityTests import MillerRabinPrimalityTest

    if n <= 1:
        return None
    
    for i in range(n+1, 2*n):
        
        if MillerRabinPrimalityTest(i, 100):
            return i
        
def SieveOfEratosthenes(n: int) -> list:
    "Calculate all the prime numbers less than n using the Sieve of Eratosthenes."

    import math

    nums = [i for i in range(2, n+1)]

    maxN = math.ceil(math.sqrt(n))

    for p in nums:

        if p > maxN:
            break

        t = 2

        while t*p <= n:
            tp = p*t

            try:
                nums.remove(tp)

            except ValueError:
                pass

            t+=1

    return nums

def MobiusFunction(n: int) -> int:
    "From a given n, calculate the Möbius function."

    if n == 1:
        return 1
    
    factorization = FactorizationMethods.TrialDivision(n, n)

    seen = []

    for f in factorization:
        if f in seen:
            return 0

        seen.append(f)
    
    if len(factorization) % 2 == 0:
        return 1
    
    return -1


class Conjectures:
    "In this class you can find all the conjectures developed."

    def CollatzConjecture(n: int) -> tuple:
        "From a given number in input, calculate the Collatz Conjecture. \n\nIt will return at: Index 0: True if the number reaches 1, False if the number reaches the initial number given in input | Index 1: the number of steps taken | Index 2: The steps (numbers reached) |"
        number = n
        steps = []
        while True:
            if n == 1:
                return (True, len(steps), steps)

            n = 3*n + 1
            steps.append(n)
            while n % 2 == 0:
                n //= 2
                steps.append(n)

            if n == number:
                return (False, len(steps), steps)

    def GoldbachConjecture(n: int) -> list:
        "The Golbach conjecture states that for any even integer exists two primes p and q with their sum being n. \n\nThe function will use the Sieve of Eratosthenes to calculate all primes below n, and then it will return all the possible combinations."

        if n % 2 == 1:
            return None

        primes = SieveOfEratosthenes(n)
        sum = 0
        Goldbach = []

        for p in primes:
            sum += p

            for j in primes:

                if sum + j == n:
                    Goldbach.append((p, j))
                
            sum = 0

        return Goldbach
    
    def TwinPrimeConjecture(x: int, y: int) -> list:
        "Given an interval of the type: [x, y] check if there are twin primes in there. \n\nThe fuction will return the twin primes found."

        from cryptographyComplements.primalityTests import MillerRabinPrimalityTest

        twinPrimes = []

        if x % 2 == 0: 
            x+= 1

        for n in range(x, y+1, 2):

            if MillerRabinPrimalityTest(n, 100) and MillerRabinPrimalityTest(n+2, 100):
                twinPrimes.append((n, n+2))

        return twinPrimes
    

