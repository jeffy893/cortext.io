"""
CORTEXT Classification Module

This module provides functionality for processing and analyzing text data using 
machine learning techniques, specifically a Multinomial Naive Bayes classifier.
It handles data loading, encoding, and prediction for the CORTEXT system.
"""

import numpy as np
import csv
import encodeString


def vectorize_sequence(sequences, dimensions):
    """
    Convert sequences to one-hot encoded vectors.
    
    This function transforms a list of sequences (where each sequence is a list of indices)
    into a one-hot encoded matrix representation.
    
    Args:
        sequences (list): List of sequences, where each sequence contains indices to be encoded
        dimensions (int): The dimensionality of the one-hot encoding (vector size)
        
    Returns:
        numpy.ndarray: A matrix of shape (len(sequences), dimensions) with one-hot encoded vectors
    """
    results = np.zeros((len(sequences), dimensions))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results


def targetCortext(csvPath='TARGET_RawActuaryPhen.csv'):
    """
    Load target values from a CSV file for model training.
    
    Reads binary classification labels from the first column of the specified CSV file.
    
    Args:
        csvPath (str): Path to the CSV file containing target values
        
    Returns:
        list: A list of integer target values (0 or 1) for training
    """
    with open(csvPath) as target_file:
        target_reader = csv.reader(target_file, delimiter=',')
        line_count = 0
        
        # instantiate target list
        # Note: This variable is initialized but not used in the current implementation
        targetOutput = [0 for i in range(0, 589)]
        
        yTrain = []
        
        for row in target_reader:
            
            # targetVector = targetOutput
            # targetVector[0] = int(row[0])
            # Note: These commented lines show an alternative approach where a full vector
            # would be created for each target instead of just storing the class value
            
            # Need the ...[:] to append a COPY of the variable
            # Note: This comment refers to a previous implementation. In the current code,
            # we're only appending the integer value from the first column, not a copy of a list
            yTrain.append(int(row[0]))
            
        return yTrain


def sourceCortext(csvPath='INPUT_RawActuaryPhen.csv'):
    """
    Load source data from a CSV file for model training.
    
    Reads feature vectors from the specified CSV file, converting each value to an integer.
    
    Args:
        csvPath (str): Path to the CSV file containing source data
        
    Returns:
        list: A list of integer feature vectors for training
    """
    with open(csvPath) as source_file:
        source_reader = csv.reader(source_file, delimiter=',')
        line_count = 0
        
        # instantiate target list
        # Note: This variable is initialized but not used in the current implementation
        targetOutput = [0 for i in range(0, 589)]
        
        xTrain = []
        
        for row in source_reader:
            rowInt = [int(i) for i in row]
            xTrain.append(rowInt[:])  # Creates a copy of the list to avoid reference issues
        
        return xTrain
        

def inputCortext(csvPath='20200511_usmca_letter.txt'):
    """
    Load and encode input data from a text file for prediction.
    
    Reads text from the specified file, encodes it using the encodeString module,
    and handles exceptions by providing a zero vector.
    
    Args:
        csvPath (str): Path to the text file containing input data
        
    Returns:
        list: A list of encoded feature vectors for prediction
    """
    with open(csvPath) as source_file:
        source_reader = csv.reader(source_file, delimiter=',')
        line_count = 0
      
        xTrain = []
        
        for row in source_reader:
            try:
                rowInt = encodeString.encodeString(row[0])
            except:
                # If encoding fails, use a zero vector of length 589
                rowInt = [0 for i in range(0, 589)]
            xTrain.append(rowInt[:])  # Creates a copy of the list to avoid reference issues
        
        return xTrain


def scoreMNB(inputPath='20200511_usmca_letter.txt', sourcePath="INPUT_RawActuaryPhen.csv", targetPath='TARGET_RawActuaryPhen.csv'):
    """
    Train a Multinomial Naive Bayes model and predict on input data.
    
    This function loads training data, trains a Multinomial Naive Bayes classifier,
    and then uses it to predict on the input data. It returns only the decoded
    strings for inputs that are classified as positive (score = 1.0).
    
    Args:
        inputPath (str): Path to the input text file for prediction
        sourcePath (str): Path to the source data CSV file for training
        targetPath (str): Path to the target data CSV file for training
        
    Returns:
        list: A list of decoded strings for inputs classified as positive
    """
    # Actuarioal Training Data
    # Note: This loads the training data from the specified source and target files
    x_sourceData = sourceCortext(sourcePath)
    y_sourceData = targetCortext(targetPath)

    # Convert lists to numpy arrays and set data type
    x_train = np.asarray(x_sourceData).astype('float32')
    y_train = np.asarray(y_sourceData).astype('float32')

    # Print the shapes of the training data for debugging
    print(x_train.shape)
    print(y_train.shape)

    # Import MultinomialNB here to avoid unnecessary imports if function is not called
    from sklearn.naive_bayes import MultinomialNB

    # Train the Multinomial Naive Bayes model
    mnb = MultinomialNB().fit(x_train, y_train)

    # Print the training accuracy
    print("score on train: " + str(mnb.score(x_train, y_train)))
    
    # Test Input of USMCA Data
    # Note: This loads and encodes the input data for prediction
    x_inputData = inputCortext(inputPath)
    x_input = np.asarray(x_inputData).astype('float32')
    
    output = []

    # Make predictions on the input data
    score = mnb.predict(x_input)

    # Filter results to only include positive predictions
    for i, phen in enumerate(x_inputData):
        if score[i] == 1.0:
            # print(encodeString.decodeString(phen))
            # Note: This commented line would print each decoded positive prediction
            output.append(str(encodeString.decodeString(phen)))
    
    return output
