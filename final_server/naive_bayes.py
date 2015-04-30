from numpy import *
import bayes

def main():
    listOPosts, listClasses = bayes.loadDataSet()
    myVocabList = bayes.createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(bayes.setOfWords2Vec(myVocabList,postinDoc))
    p0v, p1v, p1 = bayes.trainNB0(trainMat, listClasses)
    print p1
    print p0v
    print p1v

if __name__ == "__main__":
    main()