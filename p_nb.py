def main():
  import numpy as np
  import pandas as pd


  import matplotlib.pyplot as plt
  import p2 as p2
  import os
  import p1 as p1  
  import os
  import psutil
  import sys
  import traceback
  from scipy.spatial import distance

  from sklearn.naive_bayes import GaussianNB

  #here is where the emails placed
  m_vector = p2.datacollect('C:/Users/Admin/Desktop/email2')
  final_t = m_vector[1]
  t_vector = final_t[0]
  t_y = final_t[1]
  t_vector = np.array(t_vector)
  #print('len')
  #print(len(t_vector))
  m_vector = m_vector[0]
  m_vectorx = []
  m_vector_1 = m_vector[0]
  m_vector_2 = m_vector[1]
  m_vectorx.extend(m_vector_1)
  m_vectorx.extend(m_vector_2)
  m_vectory = []
  for i in range(len(m_vector_1)):
     m_vectory.extend('0')
  for i in range(len(m_vector_2)):
     m_vectory.extend('1')
  m_vectorx = np.array(m_vectorx)
  m_vectorx_h = np.array(m_vector_1)
  m_vectorx_s = np.array(m_vector_2)
  m_vectory = np.array(m_vectory)
  
  mx = np.vstack((m_vectorx_h,m_vectorx_s))
  my = np.array([0] * len(m_vectorx_h) + [1] * len(m_vectorx_s))
 
  clf = GaussianNB()
  clf.fit(mx,my)
  TP0 = 0
  FP0 = 0
  TN0 = 0
  FN0 = 0
  listy = []

  for i in range(len(t_y)):
    listy = clf.predict([t_vector[i]])
    #print(listy[0])
    #print(t_y[i])
    #print('\n')
    if(listy[0] == 0): 
        if(t_y[i] == 0):
             TP0 += 1
        else:
             FN0 += 1
    else:
        if(t_y[i] == 0):
             FP0 += 1
        else:
             TN0 += 1
  print("TP: "+str(TP0)) 
  print("FP: "+str(FP0)) 
  print("TN: "+str(TN0)) 
  print("FN: "+str(FN0)) 
  acc = (TP0+TN0)/(TP0+TN0+FP0+FN0)*100
  acc = round(acc,2)
  pre = TP0/(TP0+FP0)*100
  pre = round(pre,2)
  rec = TP0/(TP0+FN0)*100
  rec = round(rec,2)
  print("Accuracy: "+str(acc))
  print("Precision: "+str(pre))
  print("Recall: "+str(rec))

main()