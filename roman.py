""" Module to convert a user input integer to Roman numeral """

from math import floor
from math import log
import sys
from typing import Tuple
from typing import Union

numeralMap = [
    ["I", 1],
    ["V", 5],
    ["X", 10],
    ["L", 50],
    ["C", 100],
    ["D", 500],
    ["M", 1000]
]

def integer_to_numeral(integer: int) -> str:
    """ Function to convert an Arabic numeral to a Roman numeral

    :param int integer: integer from user input to convert

    :returns: the converted Roman numeral.
    :rtype: str

    """

    output: str = ""

    def subtract_or_not(index: int, current_input: int) -> Union[Tuple[str, int],
                                                           Tuple[None, None]]:
        """ Tries to build a Roman number using the substraction rules.

        :param int index: the index from the main loop currently tried
        :param int current_input: the number left over from user input currently being processed

        :returns: if a successful "compound substracted" Roman numeral is found, the function
            returns a tuple of this numeral and the left over after subtracting this value from
            the input. If that's not the case, it returns a tuple of (None, None), signaling
            no success.
        :rtype: typle of str and int or None

        """

        if index == 6:
            # We can't subtract anything from "I"/1, so skip this one
            return None, None
        if index == 5:
            # Only "I"/1 can be subtracted from "V"/5, so we only need to look one item downward
            downward = [1]
        else:
            # For the other numerals we need to look 2 items downward to find a possible Roman
            # numeral that is a valid candidate for subtracting purposes
            downward = [2,1]
        for i in downward:
            # Try the 1 or 2 possible numerals which can or cannot be used for subtracting
            totry = index+i
            if log(numeralMap[totry][1], 10).is_integer():
                # Only powers of 10 can be used to subtract
                subtracted = numeralMap[index][1] - numeralMap[totry][1]
                if subtracted <= current_input:
                    # We can only subtract a number if it isn't larger than the input
                    return (f"{numeralMap[totry][0]}{numeralMap[index][0]}",
                            current_input - subtracted)
        return None, None

    i = 0

    while integer != 0:
        (roman, arabic) = numeralMap[i]
        # Iterate over numeralMap with i as index
        remainder = integer % arabic
        result = floor(integer / arabic)
        if integer == remainder:
            # If the user input is larger than the current numeralMap index, try to subtract
            # a smaller numeral from the current and use that subtracted compount numeral
            subtr_roman, subtracted = subtract_or_not(i, integer)
            if subtr_roman:
                output += subtr_roman
                if subtracted == 0:
                    return output
                integer = subtracted
            else:
                i += 1
        elif remainder == 0:
            # If the remainder is exactly zero, we've hit an exact match and we're DONE!
            output += roman*int(integer/arabic)
            return output
        else:
            # If no exact match and no subtraction compound numeral is found, we use the current
            # Roman numeral, subtract this value from the integer and run the loop again
            output += roman*result
            integer = remainder
            i = 0
    # If we haven't entered the above while loop, the user input has to be zero. Strictly
    # speaking, the Roman numeral system did not have a numeral for 0, but we're using "N" here.
    # See https://en.wikipedia.org/wiki/Roman_numerals#Zero for more info
    return "N"

def main():
    """ Main function for user input and calling integerToNumeral() """

    # Reverse the original numeralMap so we loop from large to small instead of small to large
    numeralMap.reverse()
    print("Press Ctrl-C or Ctrl-D to quit.")

    while True:
        # User input loop
        try:
            number = input("Enter a positive integer to convert to Roman numeral: ")
            if number.isdigit():
                # Only call integer_to_numeral() if the user input is actually a digit
                print(f"The Arabic numeral {number} is {integer_to_numeral(int(number))} in Roman.")
            else:
                # User input is not a digit, print error message and loop around
                print("Invalid input, try a number this time!")
        except (EOFError, KeyboardInterrupt):
            # User has pressed Ctrl-C or Ctrl-D, exit the program
            sys.exit("\nExiting.")

if __name__ == "__main__":
    main()
