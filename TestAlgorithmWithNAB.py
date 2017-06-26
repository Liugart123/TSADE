import csv
import datetime
import time
import matplotlib.pyplot as plt
from matplotlib import pyplot
import numpy
import mlpy

timeSeriesOriginal = []
file = open("TravelTime_387.csv", "r")
reader = csv.reader(file)
boolean = False
for line in reader:
    if boolean == True:
        timeStamp = time.mktime(datetime.datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S").timetuple())
        temp = []
        temp.append(float(line[1]))
        temp.append(int(timeStamp))
        timeSeriesOriginal.append(temp)
    else:
        boolean = True

#####################################################################################################

def PlotGraph(firstList, secondList):
    x1 = []
    y1 = []
    for i in range(0, len(firstList)):
        x1.append(firstList[i][0])
        y1.append(firstList[i][1])
    fig1 = pyplot.figure()
    ax = fig1.add_subplot(111)
    ax.set_ylim(0, 3200)
    pyplot.plot(y1, x1)

    x2 = []
    y2 = []
    for i in range(0, len(secondList)):
        x2.append(secondList[i][0])
        y2.append(secondList[i][1])
    fig2 = pyplot.figure()
    ax2 = fig2.add_subplot(111)
    ax2.set_ylim(0, 3200)
    pyplot.plot(y2, x2)
    plt.show()

#####################################################################################################

def GetSubList(t,i,j):
    temp = []
    for index in range(i,j+1):
        temp.append(t[index])
    return temp

#####################################################################################################

def reduceTimeSeries(n):

    m = len(timeSeriesOriginal) - 1

    counter = 1
    i = 1
    j = n

    key = []
    key.append(0)

    flag = "true"
    while flag == "true":
        if j < m:

            temp = GetSubList(timeSeriesOriginal, i, j)

            tempMax = max(temp)
            tempMin = min(temp)

            if tempMin >= timeSeriesOriginal[key[counter-1]]:
                counter += 1
                key.append(timeSeriesOriginal.index(tempMax))
            elif tempMax <= timeSeriesOriginal[key[counter-1]]:
                counter += 1
                key.append(timeSeriesOriginal.index(tempMin))
            else:
                index = int(key[counter-1])
                if (timeSeriesOriginal[index][0] - tempMin[0]) >= (tempMax[0] - timeSeriesOriginal[index][0]):
                    counter += 1
                    key.append(timeSeriesOriginal.index(tempMin))
                else:
                    counter += 1
                    key.append(timeSeriesOriginal.index(tempMax))
        else:
            flag = "false"

        i += n
        j += n

    counter += 1
    key.append(m)

    key_counter = 1
    key_points = []
    key_points.append(0)

    for i in range(0,(counter-2)):
        firstComp = (timeSeriesOriginal[key[i+1]][0]) - (timeSeriesOriginal[key[i]][0])
        seconComp = (timeSeriesOriginal[key[i+2]][0]) - (timeSeriesOriginal[key[i+1]][0])
        if ( firstComp * seconComp )<0:
            key_counter += 1
            key_points.append(key[i+1])

    key_counter += 1
    key_points.append(m)

    for j in range(0, len(key_points)):
        seriesRepresented.append(timeSeriesOriginal[key_points[j]])

    #PlotGraph(timeSeriesOriginal,seriesRepresented)

#####################################################################################################

def GetOnlyOneAxis(list,axisNumber):
    newList = []
    for index in range(0, len(list)):
        newList.append(list[index][axisNumber])
    return newList

#####################################################################################################

def GetShortList(list,start,leng):
    newList = []
    for index in range(start, start+leng):
        if index < len(list):
            newList.append(list[index])
    if (index + 1) == (len(list) - 1):
        newList.append(list[index+1])
    return newList

#####################################################################################################

def GetShortListOfPatterns(list,start,end):
    newList = []
    for index in range(start, end):
            newList.append(list[index])
    return newList

#####################################################################################################

def SolveRegresionFunction(a,b,c,time):
    return c + (b*time) + (a*(pow(time,2)))

#####################################################################################################

def GetAbsoluteValue(value):
    if (value <= 0):
        return value * -1
    else:
        return value

#####################################################################################################

def PlotOnlyOneGraph(firstList, anomalies):
    x1 = []
    y1 = []
    for i in range(0, len(firstList)):
        x1.append(firstList[i][0])
        y1.append(firstList[i][1])
    fig1 = pyplot.figure()
    ax = fig1.add_subplot(111)
    maxi = max(firstList)
    ax.set_ylim(0, maxi[0])
    pyplot.plot(y1, x1)
    index = 0
    for i, j in zip(y1, x1):
        if i == anomalies[index][1]:
            ax.annotate(str("A"), xy=(i, j))
            if index < len(anomalies)-1:
                index += 1
    plt.show()

#####################################################################################################

def FindNextStartAndEndPointOnPattern(m,eCounter,sCounter):
    sumExpressionAbsolute = -1
    l = 4
    while(sumExpressionAbsolute < e1):
        shortList = GetShortList(seriesRepresented, sList[sCounter], l)
        x = GetOnlyOneAxis(shortList, 0)
        y = GetOnlyOneAxis(shortList, 1)
        if len(x) <= 3 or len(y) <= 3:
            m = n
            return m,eCounter,sCounter
        regressionConstants = numpy.polyfit(x, y, 2)
        a = regressionConstants[0]
        b = regressionConstants[1]
        c = regressionConstants[2]

        sumExpression = 0
        for i in range(0, l):
            if i < len(shortList):
                functionSolved = SolveRegresionFunction(a, b, c, shortList[i][0])
                expressionFormula = pow((functionSolved - shortList[i][0]), 2)
                sumExpression += expressionFormula
        sumExpressionAbsolute = GetAbsoluteValue(sumExpression)

        if (sumExpressionAbsolute < e1):
            l += 1
        else:
            eList.append(sList[sCounter]+l)
            eCounter += 1
            i = 1
            flag2 = "true"
            while flag2 == "true":
                firstList = GetShortList(seriesRepresented, sList[sCounter], eList[eCounter])
                secondList = GetShortList(seriesRepresented, (sList[sCounter]) + i, (eList[eCounter]) + i)
                firstAxis = GetOnlyOneAxis(firstList, 0)
                secondAxis = GetOnlyOneAxis(secondList, 0)
                dist, cost, path = mlpy.dtw_std(firstAxis, secondAxis, dist_only=False)
                if (dist <= e2):
                    i += 1
                if (i >= (eList[eCounter] - sList[sCounter])) or (dist > e2):
                    flag2 = "false"
            sList.append(eList[eCounter] + i)
            sCounter += 1
            m = sList[sCounter]
            return m,eCounter,sCounter

#####################################################################################################

e1 = 2
e2 = 1000
eAnomalyPattern = 1200
n = 40

seriesRepresented = []
reduceTimeSeries(n)

n = len(seriesRepresented) - 1
sList = [0]
sCounter = 0
eList = []
eCounter = -1
m = sList[sCounter]

while m < n:
    m,eCounter,sCounter = FindNextStartAndEndPointOnPattern(m,eCounter,sCounter)

if len(sList) != len(eList):
    sList.pop()
    sCounter -= 1
    eList.pop()
    eList.append(n)

listOfPatterns = []
for index in range(0, len(sList)):
    temp = GetShortListOfPatterns(seriesRepresented,sList[index],eList[index])
    listOfPatterns.append(temp)

listOfSimilar = []
for index1 in range(0, len(listOfPatterns)):
    sum = 0
    firstPatternAxis = GetOnlyOneAxis(listOfPatterns[index1], 0)
    for index2 in range(0, len(listOfPatterns)):
        secondPatternAxis = GetOnlyOneAxis(listOfPatterns[index2], 0)
        dist, cost, path = mlpy.dtw_std(firstPatternAxis, secondPatternAxis, dist_only=False)
        if dist <= eAnomalyPattern:
            numberDifference = sList[index1] - eList[index1]
            numberDifferenceAbsoluteValue = GetAbsoluteValue(numberDifference)
            if numberDifferenceAbsoluteValue <= n or numberDifferenceAbsoluteValue <= m:
                sum += 1
    listOfSimilar.append(sum)

sum = 0
for index in range(0, len(listOfSimilar)):
    sum += listOfSimilar[index]

similarAverage = float(sum)/float(len(listOfSimilar))

anomalyScore = []
for index in range(0, len(listOfSimilar)):
    a = float(similarAverage) / float(listOfSimilar[index])
    anomalyScore.append(float(a))

anomalyScoreSum = 0
for index in range(0, len(anomalyScore)):
    anomalyScoreSum += anomalyScore[index]

anomalyScoreAvg = float(anomalyScoreSum) / float(len(anomalyScore))

listOfAnomalies = []
listOfScoreAnomalies = []
for index in range(0, len(listOfPatterns)):
    if anomalyScore[index] >= anomalyScoreAvg:
        listOfAnomalies.append(listOfPatterns[index][-1])
        listOfScoreAnomalies.append(anomalyScore[index])

for index in range(0, len(listOfAnomalies)):
    dateAsDate = datetime.datetime.fromtimestamp(int(listOfAnomalies[index][1])).strftime("%Y-%m-%d %H:%M:%S")
    print "Anomaly " + str(index+1) + ": " + str(dateAsDate) + " with score :" + str(listOfScoreAnomalies[index])

PlotOnlyOneGraph(seriesRepresented,listOfAnomalies)