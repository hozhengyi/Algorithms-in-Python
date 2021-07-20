'''
Find the maximum weight iindepedant set in a given path graph. 
'''

def MWIS_with_dynamicprogramming():
  #read file
  f = open("/content/drive/MyDrive/mwis.txt","r")
  path_graph = [int(x) for x in f.readlines()]
  len_graph = path_graph[0]
  path_graph[0] = 0
  mwis_arr = []
  answer_arr = []
  #forward pass
  for i in range(len_graph+1):
    #base case
    w_i = path_graph[i]
    if i == 0:
      mwis_arr.append(w_i)
      continue
    elif i == 1:
      mwis_arr.append(w_i)
      continue

    mwis_arr.append(max(mwis_arr[i-1],mwis_arr[i-2]+w_i))
    
  #backprop
  i = 1000
  while i > 0:
    #case 1, vertex not included
    if mwis_arr[i-1] >= (mwis_arr[i-2] + path_graph[i]):
      i -= 1
    #case 2, vertex included
    else:
      answer_arr.append(i)
      i -= 2

  for query in [1, 2, 3, 4, 17, 117, 517, 997]:
    if query in answer_arr:
      print("1",end="")
    else:
      print("0",end="")
