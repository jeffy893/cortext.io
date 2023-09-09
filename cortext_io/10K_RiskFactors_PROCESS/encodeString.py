
"""
This scrip encodes a string into a number list
the mapping assumes that theres are only upper and lower case alphabetical char
and spaces

Example Encoding
    "The Whole Wide World"
    --> [46, 8, 5, 53, 49, 8, 15, 12, 5, 53, 49, 9, 4, 5, 53, 49, 15, 18, 12, 4, 0, 0, 0, 0, 0,...]
    len(string2) = 589
    
    
Methods
encodeString(input="String")
decodeString(input=[1,2,3,000...]) where len(input) = 589
    return Sting

"""


import re


# Returns number from letter


def encodeString(input="Test"):
    
    size = len(input)
    
    input = re.sub('[^0-9a-zA-Z]+', ' ', input)
    input = re.sub('\s+', ' ', input)
    input = input[:589]
    
    
    # Create list of characters in string
    subInput = [input[i:i+1] for i in range(0,size)]
    
    # Instantiate encoding list
    output = [0 for i in range(0,589)]
    
    # Use a dictionary
    
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
    # Returns number from letter
    
    for i in range(0,size):
        for letter, number in stringMap.items():
            if subInput[i] in letter:
                output[i] = number
    
    
    return output
    
# Returns letter from number

def decodeString(input=[46, 8, 5, 53, 49, 8, 15, 12, 5, 53, 49, 9, 4, 5, 53, 49, 15, 18, 12, 4]):
    
    
    
    # Instantiate encoding list
    output = ""
    
    # Use a dictionary
    
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
    
    # Returns letter from number
    
    for i in input:
        for letter, number in stringMap.items():
            if i == number:
                output += letter
    
    
    return output
