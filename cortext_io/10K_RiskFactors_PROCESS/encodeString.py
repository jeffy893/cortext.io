"""
This script encodes a string into a number list
the mapping assumes that there are only upper and lower case alphabetical characters
and spaces

Example Encoding
    "The Whole Wide World"
    --> [46, 8, 5, 53, 49, 8, 15, 12, 5, 53, 49, 9, 4, 5, 53, 49, 15, 18, 12, 4, 0, 0, 0, 0, 0,...]
    len(string2) = 589
    
    
Methods
encodeString(input="String")
decodeString(input=[1,2,3,000...]) where len(input) = 589
    return String

"""

import re


def encodeString(input="Test"):
    """
    Encode a string into a fixed-length numeric array.
    
    This function converts a string into a numeric representation by mapping each character
    to a specific number according to a predefined dictionary. The resulting array has a 
    fixed length of 589 elements, with zeros padding any unused positions.
    
    The function also:
    1. Removes all non-alphanumeric characters, replacing them with spaces
    2. Normalizes multiple spaces to single spaces
    3. Truncates the input to a maximum of 589 characters
    
    Args:
        input (str): The string to encode, defaults to "Test"
        
    Returns:
        list: A fixed-length list of 589 integers representing the encoded string
    """
    
    size = len(input)
    
    # Clean the input string: replace non-alphanumeric chars with spaces
    input = re.sub('[^0-9a-zA-Z]+', ' ', input)
    # Normalize multiple spaces to single spaces
    input = re.sub('\s+', ' ', input)
    # Truncate to maximum length of 589
    input = input[:589]
    
    
    # Create list of characters in string
    subInput = [input[i:i+1] for i in range(0, size)]
    
    # Instantiate encoding list with zeros (fixed length of 589)
    output = [0 for i in range(0, 589)]
    
    # Use a dictionary for character-to-number mapping
    stringMap = {   "a":1,
                    "b":2,
                    "c":3,
                    "d":4,
                    "e":5,
                    "f":6,
                    "g":7,
                    "h":8,
                    "i":9,
                    "j":10,
                    "k":11,
                    "l":12,
                    "m":13,
                    "n":14,
                    "o":15,
                    "p":16,
                    "q":17,
                    "r":18,
                    "s":19,
                    "t":20,
                    "u":21,
                    "v":22,
                    "w":23,
                    "x":24,
                    "y":25,
                    "z":26,
                    "A":27,
                    "B":28,
                    "C":29,
                    "D":30,
                    "E":31,
                    "F":32,
                    "G":33,
                    "H":34,
                    "I":35,
                    "J":36,
                    "K":37,
                    "L":38,
                    "M":39,
                    "N":40,
                    "O":41,
                    "P":42,
                    "Q":43,
                    "R":44,
                    "S":45,
                    "T":46,
                    "U":47,
                    "V":48,
                    "W":49,
                    "X":50,
                    "Y":51,
                    "Z":52,
                    " ":53}
    
    
    # Loop through characters and perform mapping
    
    """
    for i in range(0,size):
        
        if subInput[i] == 'a':
            output[i] = 1
        elif subInput[i] == 'b':
            output[i] = 2
        elif subInput[i] == 'c':
            output[i] = 3
        elif subInput[i] == 'd':
            output[i] = 4
    """
    # Note: The commented code above shows an alternative approach using if-elif statements
    # instead of the dictionary-based approach used below
    
    # Map each character to its corresponding number using the dictionary
    for i in range(0, size):
        for letter, number in stringMap.items():
            if subInput[i] in letter:
                output[i] = number
    
    return output
    

def decodeString(input=[46, 8, 5, 53, 49, 8, 15, 12, 5, 53, 49, 9, 4, 5, 53, 49, 15, 18, 12, 4]):
    """
    Decode a numeric array back into a string.
    
    This function converts a numeric array (created by encodeString) back into its
    original string representation by mapping each number back to its corresponding character.
    
    Args:
        input (list): A list of integers representing the encoded string.
                     Default is an example encoding of "The Whole Wide World"
        
    Returns:
        str: The decoded string
    """
    
    # Instantiate output string
    output = ""
    
    # Use the same dictionary as in encodeString for consistency
    stringMap = {   "a":1,
                    "b":2,
                    "c":3,
                    "d":4,
                    "e":5,
                    "f":6,
                    "g":7,
                    "h":8,
                    "i":9,
                    "j":10,
                    "k":11,
                    "l":12,
                    "m":13,
                    "n":14,
                    "o":15,
                    "p":16,
                    "q":17,
                    "r":18,
                    "s":19,
                    "t":20,
                    "u":21,
                    "v":22,
                    "w":23,
                    "x":24,
                    "y":25,
                    "z":26,
                    "A":27,
                    "B":28,
                    "C":29,
                    "D":30,
                    "E":31,
                    "F":32,
                    "G":33,
                    "H":34,
                    "I":35,
                    "J":36,
                    "K":37,
                    "L":38,
                    "M":39,
                    "N":40,
                    "O":41,
                    "P":42,
                    "Q":43,
                    "R":44,
                    "S":45,
                    "T":46,
                    "U":47,
                    "V":48,
                    "W":49,
                    "X":50,
                    "Y":51,
                    "Z":52,
                    " ":53}
    
    
    # Loop through characters and perform mapping
    
    """
    for i in range(0,size):
        
        if subInput[i] == 'a':
            output[i] = 1
        elif subInput[i] == 'b':
            output[i] = 2
        elif subInput[i] == 'c':
            output[i] = 3
        elif subInput[i] == 'd':
            output[i] = 4
    """
    # Note: The commented code above is from encodeString and is not relevant for decoding,
    # but kept for reference to the alternative approach
    
    # Map each number back to its corresponding character
    for i in input:
        for letter, number in stringMap.items():
            if i == number:
                output += letter
    
    return output
