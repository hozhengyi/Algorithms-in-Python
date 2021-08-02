'''
My implemntation of karger's to find the minimum cut in a given graph.
'''

def kargersMinimumCutAlgorithm():
  import pickle
  from secrets import choice
  from sys import maxsize
  with open('/content/drive/MyDrive/adj_list.pkl','rb') as f:  # Python 3: open(..., 'rb')
      CONST_adj_list = pickle.load(f)
  n = 200

  min_cut = maxsize
  for o in range(200*200):
    adj_list = CONST_adj_list.copy()
    for _ in range(198):
      #random edge pick
      v1 = choice(list(adj_list.keys()))
      v2 = choice(adj_list[v1])
      #merge v1,v2 into [v1,v2] in adj_list
      if type(v1) == tuple and type(v2) == str:
        new_key = (*v1,v2) 
      elif type(v2) == tuple and type(v1) == str:
        new_key = (v1,*v2) 
      elif type(v2) == tuple and type(v1) == tuple:
        new_key = v1+v2 
      else:
        new_key = (v1,v2)
      adj_list[new_key] = []
      #merge all vertice reference in other vertices
      #remove self loops and delete merged vertices
      for k in (v1,v2): 
        adj_list[new_key] = adj_list[new_key] + [x for x in adj_list[k] if x not in (v1,v2)]
        del adj_list[k]
      for key in adj_list.keys():
        adj_list[key] = [y if (y!=v1) and (y!=v2) else new_key for y in adj_list[key] ]
    for v in adj_list.values():
      candidate_min_cut = len(v)
    if candidate_min_cut < min_cut:
      min_cut = candidate_min_cut
      print(min_cut)
      print(o)
  print()
  print("THE MINCUT IS :", min_cut)
