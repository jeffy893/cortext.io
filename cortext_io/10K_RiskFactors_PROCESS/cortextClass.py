import numpy as np
import csv
import encodeString




def vectorize_sequence(sequences,dimensions):
    results=np.zeros((len(sequences),dimensions))
    for i, sequence in enumerate(sequences):
        results[i,sequence] = 1.
    return results


def targetCortext(csvPath='TARGET_RawActuaryPhen.csv'):
    with open(csvPath) as target_file:
        target_reader = csv.reader(target_file, delimiter=',')
        line_count = 0
        
        # instantiate target list
        targetOutput = [0 for i in range(0,589)]
        
        yTrain = []
        
        
        for row in target_reader:
            
            # targetVector = targetOutput
            # targetVector[0] = int(row[0])
            
            
            # Need the ...[:] to append a COPY of the variable
            yTrain.append(int(row[0]))
            
        return yTrain

def sourceCortext(csvPath='INPUT_RawActuaryPhen.csv'):
    with open(csvPath) as source_file:
        source_reader = csv.reader(source_file, delimiter=',')
        line_count = 0
        
        # instantiate target list
        targetOutput = [0 for i in range(0,589)]
        
        xTrain = []
        
        
        for row in source_reader:
            rowInt = [int(i) for i in row]
            xTrain.append(rowInt[:])
        
        return xTrain
        
def inputCortext(csvPath='20200511_usmca_letter.txt'):
    with open(csvPath) as source_file:
        source_reader = csv.reader(source_file, delimiter=',')
        line_count = 0
      
        xTrain = []
        
        
        for row in source_reader:
            try:
                rowInt = encodeString.encodeString(row[0])
            except:
                rowInt = [0 for i in range(0,589)]
            xTrain.append(rowInt[:])
        
        return xTrain


def scoreMNB(inputPath='20200511_usmca_letter.txt',sourcePath="INPUT_RawActuaryPhen.csv",targetPath='TARGET_RawActuaryPhen.csv'):

    # Actuarioal Training Data
    x_sourceData = sourceCortext(sourcePath)
    y_sourceData = targetCortext(targetPath)




    x_train = np.asarray(x_sourceData).astype('float32')
    y_train = np.asarray(y_sourceData).astype('float32')


    print(x_train.shape)
    print(y_train.shape)


    from sklearn.naive_bayes import MultinomialNB


    mnb = MultinomialNB().fit(x_train, y_train)

    print("score on train: "+ str(mnb.score(x_train, y_train)))
    
    # Test Input of USMCA Data
    x_inputData = inputCortext(inputPath)
    x_input = np.asarray(x_inputData).astype('float32')
    
    output = []

    score = mnb.predict(x_input)

    for i, phen in enumerate(x_inputData):
        if score[i] == 1.0:
            # print(encodeString.decodeString(phen))
           output.append(str(encodeString.decodeString(phen)))
    
    return output
