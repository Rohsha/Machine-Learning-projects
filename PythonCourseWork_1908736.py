# Registration No - 1908736

import os
import csv
import numpy as np
import random
 
 
def load_from_csv(path):
 
    "List to store the original data matrix from csv"
 
    Data_Matrix = []
 
    " Search for the csv file in the root folder / directory, and get the absolute path of the csv file "
    for root, dirs, files in os.walk(r'/Users/shankar/Desktop/Rohini/Python Coursework'):
        for name in files:
            if name == path:
                path = os.path.abspath(os.path.join(root, name))
    " Open the csv file found in the path "        
    f=open(os.path.abspath(path),'r')
    readCSV = csv.reader(f,delimiter=',')
    " Read the content of the csv file, add each row of the csv file as a list,"
    " assuming all values are numeric values "
    for line in readCSV:
        line=list(map(float, filter(None, line)))
        ind_list=list(line)
        Data_Matrix.append(ind_list)
    return Data_Matrix
 
def get_max(Data_Matrix,colNumber):
 
    " Get the maximum value from a specific column of the data matrix"
    maxValue=float(Data_Matrix[0][colNumber])
    for i in Data_Matrix:
        if float(i[colNumber]) > float(maxValue):   
            maxValue = i[colNumber]
    return(float(maxValue))
 
def get_min(Data_Matrix,colNumber):
 
    " Get the minimum value from a specific column of the data matrix"
    minValue=(Data_Matrix[0][colNumber])
    for i in Data_Matrix:
        if float(minValue)>float(i[colNumber]):
            minValue=i[colNumber]
            
    return float(minValue)
 
def get_avg(Data_Matrix,colNumber):
    " Get the average value from a specific column of the data matrix"
    len_matrix=len(Data_Matrix)
    (sum)=0
    for i in Data_Matrix:
       sum=sum+i[colNumber]
       avg=(sum/len_matrix)
    return(float(avg))
  
def get_standardised_matrix(Data_Matrix):
 
    " Get Standardised Data Matrix from the original data matrix."
    " The Standardised Data Matrix will be used for further manipulation / analysis of data"
 
    " List to store the transient data matrix for data manipulation"
    Data_Matrix1 = []
    for i in Data_Matrix:
        row_Matrix=[]
        for j in range(len(i)): 
            mini=get_min(Data_Matrix,j)
            maxi=get_max(Data_Matrix,j)
            avg=get_avg(Data_Matrix,j)
            std_value=(i[j]-avg)/(maxi-mini)
            row_Matrix.append(std_value) 
        Data_Matrix1.append(row_Matrix)
        
        "Round the value of Standardadised data matrix to 4 decimal places"
        "using numpy array"
    std_Data_Matrix=np.around(np.array(Data_Matrix1),4)
    return std_Data_Matrix
 
def get_median(Data_Matrix1,col_num):
 
    "Get the median value of a particular column in Data Matrix"
    sor_col=[]
    for i in (Data_Matrix1):
        sor_col.append(i[col_num])
    sor_col.sort()
    len_sorcol=len(sor_col)
    "Check if the number of items is odd or even, and calculate median accordingly"
    if (len_sorcol%2)==0:
        ind=int(len_sorcol/2)
        median=(sor_col[ind-1]+sor_col[ind])/2
        return median
    else:
        ind=int((len_sorcol+1)/2)
        median=sor_col[(ind-1)]
        return median        
        
def get_groups(Data_Matrix1,k):
 
    "This function implements the clustering algorithm based on the given data matrix and a postive value K (that means K no of clusters)"
    ran_matrix=[]
    S=[]
    "Select K different rows from the data matrix at random"
    ran_matrix=(random.sample(Data_Matrix1,k))
    #[]
    #keys=range(k)
    #for i in keys:
    #    c.append(ran_matrix[i])
    "Calculate manhatten distance between the standardized data matrix"
    distance=get_distance(Data_Matrix1,ran_matrix)
    "Create a list to assign the respective clusters with the index having nearest distance "
    "between the standardised data matrix and random matrix chosen based on positive value K"
    S=getMinIndex(distance)
    "Get the centroids based on the Data Matrix and the list with the cluster classification obtained in the previous step (Step 6 of the algorithm)"
    get_centroids(Data_Matrix1,S,k)
 
def get_distance(Data_Matrix1,ran_matrix):
 
    "Get the manhattan distance between the standardised data matrix and the random data matrix created with the no of K rows"
    distance=[]
    indDiffs=[]
    
    for i in Data_Matrix1: 
       indDiffs=[] 
       for keys in ran_matrix:
          sumValue=sum(abs(np.subtract(keys,i)));
          indDiffs.append(sumValue)
#       p=min(indDiffs)
#       min_index=indDiffs.index(p)
       distance.append(indDiffs)
#       distance.append(min_index)  
    return distance  
def getMinIndex(distance):
    "This function is written to calculate the nearest distance and get the list S for each step."
    "This function can be called for the initial formation of cluster list and also for subsequent execution."
    S=[]
    for i in distance:
        minValue = min(i)
        minIndex = i.index(minValue)
        S.append(minIndex)    
    return S
def get_centroids(Data_Matrix1,S,k):
    #c=[]
    "List to store the clustered entities based on the S list created in previous step"
    masterGroup=[]
    "List to store the new centroid"
    newCentroid=[]
    for j in range(k):
       ind_group=[]
       for i in (range(len(S))):
            if S[i]==j:
                ind_group.append(Data_Matrix1[i])
       columns=len(Data_Matrix1[i])         
       masterGroup.append(ind_group)
       centroidIndList=[]
       "Calculate median of each column based on the clustered entities"
       for l in range(columns):
           med=get_median(ind_group,l)
           centroidIndList.append(med)
       newCentroid.append(centroidIndList)
    "Calculate Manhanttan distance with the original matrix and the new Centroid"
    distance=get_distance(Data_Matrix1,newCentroid)
    "Create a list to assign the respective clusters with the index having nearest distance "
    "between the standardised data matrix and random matrix chosen based on positive value K"
    newCenterPoints_S=getMinIndex(distance)
    "Repeat the steps until the list S doesnt change"
    if newCenterPoints_S!=S:
       get_centroids(Data_Matrix1,newCenterPoints_S,k)
    else:   
       for i in range(k):
           print("Group no "+str(i+1) +".  No of entities in "+"Group no "+str(i+1)+" is  "+ str( len(masterGroup[i])))
           print(masterGroup[i])
           print('finished')
           
def run_test1():
    Data_Matrix=load_from_csv("Wines_statistics.csv")
    std_Data_Matrix_Main=get_standardised_matrix(Data_Matrix)
    for k in range(2,7):
        get_groups(std_Data_Matrix_Main.tolist(),k)
 
run_test1();
