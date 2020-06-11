import email
import email.policy
import email.parser
import p1 as pa
import numpy as np
from sklearn.model_selection import train_test_split
import os
import re
from html import unescape
import time
import gc
import os
import psutil
import sys
import traceback
PROCESS = psutil.Process(os.getpid())
MEGA = 10 ** 6
MEGA_STR = ' ' * MEGA
     
 
def load_email(is_spam, filename, path):
    directory = "spam" if is_spam else "ham"
    with open(os.path.join(path, directory, filename), "rb") as f:
        return email.parser.BytesParser(policy=email.policy.default).parse(f)
 
def html_to_plain_text(html):
    text = re.sub('<head.*?>.*?</head>', '', html, flags=re.M | re.S | re.I)
    text = re.sub('<a\s.*?>', ' HYPERLINK ', text, flags=re.M | re.S | re.I)
    text = re.sub('<.*?>', '', text, flags=re.M | re.S)
    text = re.sub(r'(\s*\n)+', '\n', text, flags=re.M | re.S)
    return unescape(text)

def email_to_text(email):
    html = None
    for part in email.walk():
        ctype = part.get_content_type()
        if not ctype in ("text/plain", "text/html"):
            continue
        try:
            content = part.get_content()
        except: # in case of encoding issues
            content = str(part.get_payload())
        if ctype == "text/plain":
            return content
        else:
            html = content
    if html:
        return html_to_plain_text(html)


def datacollect(Path):
  thred = 0.3
  thred2 = 20
  m_type = []
  m_word = [] # all words
  m_data = [] # different file store in different element: for train
  m_vector_h = [] 
  m_vector_s = []
  m_otherword = []
  path_h = Path + '/ham'
  path_s = Path + '/spam'

  files = os.listdir(path_h)
  ham_emails = [load_email(is_spam=False, filename=name, path=Path) for name in files]
  
  files = os.listdir(path_s)
  spam_emails = [load_email(is_spam=True, filename=name, path=Path) for name in files]
  #print(ham_emails[4].get_content().strip())
  #print('\n')
  str1 = email_to_text(ham_emails[4])
  #print(str1)
  #print('\n')
  #print(pa.hsparser(str1))
  #print(spam_emails[5].get_content().strip()) 
  #print(email_to_text(spam_emails[5]))

  st = time.clock()
  X = []
  y = []
  #X_c = np.array(ham_emails + spam_emails)

  ######
  X_c = np.array(ham_emails[:800] + spam_emails)

  ######
  i = 0
  N = len(X_c)
  for XX in X_c:
    strtmp = pa.hsparser(email_to_text(XX))
    X.append(strtmp)
    p = round((i + 1) * 100 / N)
    duration = round(time.clock() - st, 2)
    remaining = round(duration * 100 / (0.01 + p) - duration, 2)
    print("parsing:{0}%,time spent:{1}s,time needed:{2}s".format(p, duration, remaining), end="\r")
    time.sleep(0.01)
    i = i+1
  #print(X)
  X = np.array(X)
  #y = np.array([0] * len(ham_emails) + [1] * len(spam_emails))
 
  #####
  y = np.array([0] * 800 + [1] * len(spam_emails))
 
  #####
  

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  gc.collect()

  #print(X_train) 
  X_temp = []
  for xt in X_train:
     X_temp.extend(xt)
  X_temp = np.array(X_temp)
  m_set = set(list(np.unique(X_temp)))
  m_vocab = list(m_set)
  #print(m_vocab)
  #print(len(X_train))
  NN = len(X_train)
  stt = time.clock()
  #print('training'+str(X_train))
  #print('m_set'+str(m_set))
  for i in range(len(X_train)):
    tmparray = [0] * len(m_set)
    tmp = X_train[i]
    for word in tmp:
       if word in m_set:  
          tmparray[m_vocab.index(word)] += 1
    if y_train[i] == 0:
      m_vector_h.append(tmparray)
    else:
      m_vector_s.append(tmparray)
    p = round((i + 1) * 100 / NN)
    duration = round(time.clock() - stt, 2)
    remaining = round(duration * 100 / (0.01 + p) - duration, 2)
    print("bag-of-words:{0}%,time spent:{1}s,time needed:{2}s".format(p, duration, remaining), end="\r")
    time.sleep(0.01)
  mve = m_vector_h + m_vector_s
  tmpmv = np.array(mve)
  m_vector_h = np.array(m_vector_h)
  m_vector_s = np.array(m_vector_s)
  time.sleep(0.1)
  print("\n")
  print("num of h_samples: "+str(len(m_vector_h)))
  print("num of s_samples: "+str(len(m_vector_s)))
  print("num of dimensions: "+str(len(m_vector_h[0])))
  si1 = len(m_vector_h[0])
  numofs = len(tmpmv)
  st1 = si1
  stt = time.clock()
  ii = 0
  ii2 = 0
  thred_all = np.sum(tmpmv,axis = 0)
  thred_h = np.sum(m_vector_h,axis = 0)
  thred_s = np.sum(m_vector_s,axis = 0)
  print_memory_usage()

 

  for m_tt in range(len(m_vector_h)):
     if(sum(m_vector_h[m_tt]) <= thred2):
       np.delete(m_vector_h,m_tt,0)
  for m_tt in range(len(m_vector_s)):
     if(sum(m_vector_s[m_tt]) <= thred2):
       np.delete(m_vector_s,m_tt,0)
  m_vector = [list(m_vector_h),list(m_vector_s)]
  time.sleep(0.1)
  print("\n")
  #print(len(m_vector_h))
  #print("num of dimensions after: "+str(len(m_vector_h[0])))
  
  

  t_vector = []
  for i in range(len(X_test)):
    tmparray = [0] * len(m_vocab)
    tmp = X_test[i]
    for word in tmp:
       if word in m_vocab:
          tmparray[m_vocab.index(word)] += 1
    t_vector.append(tmparray)
  for m_tt in range(len(t_vector)):
     if(sum(t_vector[m_tt]) <= thred2):
       np.delete(t_vector,m_tt,0)
  #print(t_vector)
  final_t = [t_vector,y_test]
  m_vector = [m_vector,final_t]
  return m_vector
  

def print_memory_usage():
    total, available, percent, used, free = psutil.virtual_memory()
    total, available, used, free = total / MEGA, available / MEGA, used / MEGA, free / MEGA
    proc = PROCESS.memory_info()[1] / MEGA
    print('process = %s total = %s available = %s used = %s free = %s percent = %s'
          % (proc, total, available, used, free, percent))

def log_exception(exception: BaseException, expected: bool = True):
    output = "[{}] {}: {}".format('EXPECTED' if expected else 'UNEXPECTED', type(exception).__name__, exception)
    print(output)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback)

