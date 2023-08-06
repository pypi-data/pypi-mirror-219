"In this script you can find all the functions relative to Cryptosystems."
class Ciphers:
    "In this class you can find all the Ciphers, moreover a cryptanalysis for ciphertext and a plaintext to ciphertext function."

    class Encryption:

        def MonoalphabeticCipher() -> dict:
            "This function generates a cipher using the monoalphabetic encryption"
            import string, random
            elements = string.ascii_letters + string.digits + string.punctuation + "àèéìíòù" + "ÀÁÈÉÌÍÒÓÙÚ"
            cipher = {elements[i]: None for i in range(len(elements))}

            already_sorted = []

            for i in cipher.keys():
                while True:
                    sort = random.randint(0, len(elements) -1)
                    if sort in already_sorted:
                        continue
                    else:
                        break

                already_sorted.append(sort)
                cipher[i] = elements[sort]

            return cipher

        def CaesarCipher() -> dict:
            "This functions generate the Caesar Cipher with a random shift."
            import string, random
            elements = string.ascii_letters + string.digits + string.punctuation + "àèéìíòù" + "ÀÁÈÉÌÍÒÓÙÚ"
            cipher = {elements[i]: None for i in range(len(elements))}

            shift = random.randint(0, len(cipher))

            modulo = int(len(cipher))
            for i in cipher.keys():
                index = shift % modulo
                cipher[i] = elements[index]
                shift += 1

            return cipher
        
        def cryptanalysisCiphertext(ciphertext: str) -> dict:
            "From a given ciphertext in input, the function will return the frequency of the characters that occurs in the ciphertext."

            import decimal

            lenght = len(ciphertext)

            letters = {}

            for c in ciphertext:
                try:
                    letters[c] += 1

                except KeyError:
                    letters[c] = 1


            if ' ' in letters.keys():
                lenght -= letters[' ']

            lettersFrequency = {}

            for letter in letters.keys():

                if letter == ' ':
                    continue

                freq = ((decimal.Decimal(letters[letter])/decimal.Decimal(lenght))*decimal.Decimal(100))

                lettersFrequency[letter] = float(freq.quantize(decimal.Decimal('0.00'), rounding=decimal.ROUND_DOWN))

            return lettersFrequency

        def convertPlaintextToCiphertext(plaintext: str, cipher: dict) -> str|None:
            "From a given plaintext and a cipher, convert the plaintext to a ciphertext. \n\nIf a letter isn't in the cipher the function will return None."

            ciphertext = ""

            for plain in plaintext:
                if plain == " ":
                    ciphertext+= " "
                    continue
                
                try:
                    ciphertext += cipher[plain]

                except KeyError:
                    return None

            return ciphertext


class Asymmetric:
    "In this class you can find all the Asymmetric Cryptosystems"
    class RSA:
        "The RSA implementation, including the Creation of the Key, Encryption and Decryption."

        def KeyCreation(p: int, q: int) -> tuple:
            "Given two distinct primes: p and q. Return p, q, N=p*q, e=65537"

            N = p * q

            e = pow(2, 16) + 1

            return p, q, N, e
        
        def Encryption(plaintext: int, e: int, N: int) -> int:
            "Given the plaintext converted in an integer, the public encryption exponent (e) and N: product of p and q, return the plaintext encrypted."

            if not 1 <= plaintext < N:
                return None
            
            ciphertext = pow(plaintext, e, N)

            return ciphertext


        def Decryption(p: int, q: int, e: int, ciphertext: int) -> int:
            "Given p and q the prime numbers used for the creation of the key, the public encryption exponent (e) and the ciphertext, return the ciphertext decrypted."

            from cryptographyComplements.mathFunctions import ExtendedEuclideanModularMultiplicativeInverse

            n = (p-1)*(q-1)

            N = p*q

            d = ExtendedEuclideanModularMultiplicativeInverse(e, n)

            plaintext = pow(ciphertext, d, N)

            return plaintext


