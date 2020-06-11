#from wordsegment import load, segment
#load()
def hsparser(Filecontent):
 if Filecontent:
  import wordsegment
  import re
  import urlextract
  ue = urlextract.URLExtract()
  #print(Filecontent)
  urls = ue.find_urls(Filecontent)
  for yu in urls:
    Filecontent = Filecontent.replace(yu,'url')
  listofchar = ['_','"' ,'\'','“','”','’', '/','\\' ,  '-' ,  ',' , '`'  , '.','>','<','?','!','#','%','&','(',')','=','+','|',';',':','~',']','[','{','}','*','^']
  for lis in listofchar:
    Filecontent = Filecontent.replace(lis,'')
  listofmoney = ['$','£','€']
  for lis in listofmoney:
    Filecontent = Filecontent.replace(lis,' msign')
  s1  = Filecontent.split()
  brange = len(s1)
  b = 0
  while(b<brange):
    s1[b] = s1[b].lower()
    if(re.match(r"\S+@\S+",s1[b])):
      s1[b] = 'emailaddress'
    elif(re.match(r"http",s1[b])):
      s1[b] = 'url'
    elif(re.match(r"^msign[0-9]+$",s1[b])):
      #print("money")
      #print(s1[b])
      s1[b] = 'mamount'
    elif(re.match(r"^[0-9]+$",s1[b])):
      if(len(s1[b])== 10):
       #print("phone")
       #print(s1[b])
       s1[b] = 'pno'
      else:
       s1.pop(b)
       b = b - 1
       brange = brange -1
    elif(not re.match(r"^[0-9a-zA-Z]+$",s1[b])):
      #print("not english")
      #print(s1[b])
      s1.pop(b)
      b = b - 1
      brange = brange -1
    elif(len(s1[b])>=20):
      #print("too long")
      #print(s1[b])
      s1[b] = 'emessage'
    b = b + 1
  result = ''
  i = 0
  i2 = 1
  #while i <= lent-1:
   # str = s1[i] + ' ' + s1[i+1] 
    #try:
     #if wordsegment.BIGRAMS[str]>=1:
      #s1[i] = str
      #lent = lent - 1
     # s1.pop(i+1)
    #except Exception as inst:
    #  pass
   # i = i + 1
 #print(s1)
  #s1.extend(s2)
  return s1 
 else:
  return []