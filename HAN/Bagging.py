import numpy as np
import pandas as pd

def get_labels(df):

    labels = []
    
    for i in range(len(df)):
      temp = []
      for j in range(8):
        temp.append(df.iloc[i,j+1])
      labels.append(np.array(temp))

    return np.array(labels)

def Bagging(ScoreList,label):

    prediction = np.zeros(label.shape)
    for i in range(len(label)):
        for j in range(len(ScoreList)):
            prediction[i] += ScoreList[j][i] 
    prediction /= len(ScoreList)
    
    for i in range(len(prediction)):
        for j in range(len(prediction[i])):
            if prediction[i][j] < 0:
                prediction[i][j] = -1
            else:
                prediction[i][j] = 1
  
    ExactMatchAccuracy = 0
    for i in range(len(prediction)):
        correctMatch = 0
        for j in range(len(prediction[i])):
            if int(prediction[i][j]) == int(label[i][j]):
                correctMatch+=1
        if correctMatch == 8:
            ExactMatchAccuracy += 1

    return (ExactMatchAccuracy/len(prediction))

#*************************************************
test = pd.read_pickle('path to test.pkl')
#*************************************************
labels = get_labels(test)

NLL=np.load('path to result of test with NLL loss ,it will in .npy extension')
Hg = np.load('path to result of test with Hinge loss ,it will in .npy extension')
HgSqr = np.load('path to result of test with Hinge square loss ,it will in .npy extension')

ScoreList = [NLL,Hg,HgSqr]
print('All_losses_combined :', Bagging(ScoreList,labels))
print("NLL & Hg :", Bagging(ScoreList[0:2],labels))
print("NLL & HgSqr :", Bagging([ScoreList[0],ScoreList[1]],labels))
print("Hg & HgSqr :", Bagging(ScoreList[1:],labels))
