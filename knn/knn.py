#-*- coding: utf-8 -*-
import numpy
import operator
import time
from os import listdir
import PIL.Image




'''图片预处理函数
'''
def pretreatment(file):
    ima = PIL.Image.open(file)#打开图片
    ima = ima.convert('L')  #把图片转换成灰阶模式
    im = numpy.array(ima)  #把像素点保存到一个二维数组
    #set_printoptions(threshold=100000)
    '''下面开始把图片的开始和结束的空白部分去掉
    '''
    startingRow = 0 #去掉空白部分后的开始行
    startingCol = 0 #去掉空白部分后的开始列
    for startingRow in range(0,im.shape[0]): #从第一行开始循环，直到找到非空白行
    	if any(im[startingRow,:]<128):  #非空白行的条件是至少有一个像素点灰阶<128 (256/2)，灰阶0=全黑，255=全白，128代表黑和白的中间点。
    		break;

    for startingCol in range(0,im.shape[1]):#用同样的方法找到第一个非空白列
    	#print(j,im[:,j])
    	if any(im[:,startingCol]<128):    		
    		break;

    endRow=im.shape[0]-1 #去掉空白部分后的结束行,从最后一行开始找
    endCol=im.shape[1]-1 #去掉空白部分后的结束列,从最后一列开始找
    while(endRow>-1): 
    	if any(im[endRow,:]<128): #非空白行的条件是至少有一个像素点灰阶<128 (256/2)，灰阶0=全黑，255=全白，128代表黑和白的中间点。
    		break;
    	else:
    		endRow = endRow-1    
    while(endCol>-1):
    	if any(im[:,endCol]<128):    		
    		break;
    	else:
    		endCol=endCol-1

    box = (startingCol,startingRow,endCol,endRow) #切割图片，把开始部分和结束部分的空白行/列切掉，切割完后
    newima = ima.crop(box).resize((32,32))#把切割后图片等比例转换成32*32像素图片
    names = file.split('/')
    newima.save("temp/"+names[len(names)-1]) #保存一个临时文件以用来检查处理后的图片是否正确
    im = numpy.array(newima) #重新用二维数组保存图片像素
    returnV =[] # 最终函数返回值是一个1024（32*32）位的一维数组，就是把图片像素按行展开来。每个元素值是0或1。
    for i in im:
    	for x in i:
    		f = lambda x:1 if x<128 else 0 #灰阶转换成0/1值 - 灰阶<128 (256/2) 为1。灰阶0=全黑，255=全白，128代表黑和白的中间点。
    		returnV.append(f(x))
    return returnV

'''分类函数
inputPoint - 代表待分类图片的1024位一维数组
dataSet - 代表训练集的二维数组
labels - 已分好的类别
k - knn算法的k
'''
def classify(inputPoint,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]     #已知分类的数据集（训练集）的行数    
    tileInput = numpy.tile(inputPoint,(dataSetSize,1)) #将输入点拓展成与训练集相同维数的数组，就是把就是把一维数组扩展成二维，每一行的值都是inputPoint
    diffMat = tileInput - dataSet  #样本与训练集的差值矩阵
    sqDiffMat = diffMat ** 2                    #差值矩阵平方
    sqDistances = sqDiffMat.sum(axis=1)         #计算每一行上元素的和
    distances = sqDistances ** 0.5              #开方得到欧拉距离矩阵
    sortedDistIndicies = distances.argsort()    #按distances中元素进行升序排序后得到的对应下标的列表
    #选择距离最小的k个点
    classCount = {}
    for i in range(k):
        voteIlabel = labels[ sortedDistIndicies[i] ]
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1
    #按classCount字典的第2个元素（即类别出现的次数）从大到小排序
    sortedClassCount = sorted(classCount.items(), key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

#文本向量化 32x32 -> 1x1024
def img2vector(filename):
    returnVect = []
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect.append(int(lineStr[j]))
    return returnVect

#从文件名中解析分类数字
def classnumCut(fileName):
    fileStr = fileName.split('.')[0]
    classNumStr = int(fileStr.split('_')[0])
    return classNumStr

'''从文件名中解析分类数字
规则是0-1.png，0代表数字分类，1代表第1个样本
'''
def classnumCut1(fileName):
    fileStr = fileName.split('.')[0]
    classNumStr = int(fileStr.split('-')[0])
    return classNumStr


#构建训练集数据向量，及对应分类标签向量
def trainingDataSet():
    t1 = time.time()	
    hwLabels = [] #用来输出分类列表
    trainingFileList = listdir('test')           #从这个目录里读取已分好类的训练图片
    m = len(trainingFileList)
    trainingMat = numpy.zeros((m,1024))                          #m*1024个数据的训练集，每个元素初始化为0
    for i in range(m):
        fileNameStr = trainingFileList[i]
        hwLabels.append(classnumCut1(fileNameStr))#hwLabels记录了每个文件代表的数字分类
        trainingMat[i,:] = pretreatment('test/%s' % fileNameStr)#trainingMat的每一行保存了0/1代表的处理后的一张图片
    t2 = time.time()
    print("Training time: %.2fmin, %.4fs."%((t2-t1)//60,(t2-t1)%60))      #训练耗时

    return hwLabels,trainingMat #返回分类列表 及训练集特征数组

#测试函数
def test():
    hwLabels,trainingMat = trainingDataSet()    #构建训练集
    testFileList = listdir('tt')    #从这个目录里读取要测试的图片
    errorCount = 0.0                            #用来记录错误的次数
    mTest = len(testFileList)                   #用来记录测试的次数
    t1 = time.time()							#用来记录测试时间
    for i in range(mTest):						
        fileNameStr = testFileList[i]
        classNumStr = classnumCut1(fileNameStr)	#测试集也是预先分好类的
        vectorUnderTest = pretreatment('tt/%s' % fileNameStr) #预处理图片        
        classifierResult = classify(vectorUnderTest, trainingMat, hwLabels, 3)#调用knn算法进行分类
        #打印分类结果
        print("the test result is: %d, the actual number is: %d %s" % (classifierResult, classNumStr, classifierResult==classNumStr))
        if (classifierResult != classNumStr): errorCount += 1.0 #记录错误
    print("\nthe total number of tests is: %d" % mTest)               #输出测试总样本数
    print("the total number of errors is: %d" % errorCount)           #输出测试错误样本数
    print("the total error rate is: %f" % (errorCount/float(mTest)))  #输出错误率
    t2 = time.time()
    print("Test time: %.2fmin, %.4fs."%((t2-t1)//60,(t2-t1)%60))      #测试耗时

test()


