"In this script you can find additional functions to reduce the code written."
class Numbers:
    "In this class you can find general functions about numbers. \n\nThe purpose of this class is to avoid code repetion."

    def listMultiplication(arg: list) -> int:
        "From a given list or tuple in input, calculate the multiplication of the numbers inside it. \n\nNote: Non-numerical values will be skipped."

        if isinstance(arg, int) or isinstance(arg, float):
            return arg

        result = 1

        for i in arg:

            try:
                result *= int(i)
            
            except ValueError:
                continue

        return result

    def listSum(arg: list) -> int:
        "From a given list or tuple in input, calculate the addition of the numbers inside it. \n\nNote: Non-numerical values will be skipped."
        
        if isinstance(arg, int) or isinstance(arg, float):
            return arg
        
        result = 0

        for i in arg:

            try:
                result += int(i)

            except ValueError:
                continue

        return result
    
    def lcm(n1: int, n2: int) -> int:
        "Calculate the least common multiple for two numbers n1 and n2."
        from cryptographyComplements.mathFunctions import EuclideanAlgorithm

        gcd = EuclideanAlgorithm(n1, n2)

        return abs(n1) * (abs(n2)/gcd)

    def lcm_list(numbers: list) -> int:
        "Calculate the least common multiple for a list of integer numbers."

        lcmN = numbers[0]
        for i in range(1, len(numbers)):

            lcmN = Numbers.lcm(lcmN, numbers[i])

        return int(lcmN)


class stopwatch:
    "Create as many stopwatch as you need."
    def start() -> float:
        "Start a stopwatch. \nNote: The stopwatch needs to be saved into a variable."
        import time
        return time.time()

    def stop(stopwatch: float) -> float:
        "Stop a given stopwatch, and prints out the execution time."
        import time
        elapsed = time.time() - stopwatch
        return elapsed
    

class UnicodeConversion:
    "This class provides two functions that allows you to convert a text to an integer and convert it again to a text."

    def TextToInt(text: str) -> int:
        "Given a string in input convert it into a integer."
        unicode_text = text.encode('utf-8')
        int_value = int.from_bytes(unicode_text, byteorder='big')

        return int_value
    
    def IntToText(text_integer: int) -> str:
        "Given an integer in input convert it to text.\n\nWarning: If the integer that has to be converted to text wasn't, before, converted to integer using the TextToInt function it won't work."
        byte_sequence = text_integer.to_bytes((text_integer.bit_length() + 7) // 8, byteorder='big')
        unicode_text = byte_sequence.decode('utf-8')

        return unicode_text
    
