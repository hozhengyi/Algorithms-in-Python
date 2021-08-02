'''
My implemntation of kruskals using a unionfind data structure to speed it up. This returns an MST of a given graph.
'''

from time import time
from math import inf

def union(a,b):
  global unionFind
  a_leader = unionFind[a]
  b_leader = unionFind[b]
  #rewire all nodes pointing to a to point to b
  for key in unionFind.keys():
    if unionFind[key] == a_leader:
      unionFind[key] = b_leader
def kruskalsAlgorithmWithUnionFind():
  #read graph and form adjacency list
  greedy_algo = {}
  f = open('/content/drive/MyDrive/clustering1.txt','r')
  MAX_NODE = 500
  MIN_CLUSTER = 4
  flines = f.readlines()
  for line in flines:
    line = line.split()
    try:
      greedy_algo[int(line[2])].append((int(line[0]),int(line[1])))
    except:
      greedy_algo[int(line[2])] = [(int(line[0]),int(line[1]))]

  #initialise disjoint sets of objects
  unionFind  = {p:p for p in range(1,MAX_NODE+1)}

  #sort by decreasing order of edge length
  greedyPickingOrder = sorted(greedy_algo.keys())
  cluster_count = len(unionFind)

  #kruskals
  for idx,edge in enumerate(greedyPickingOrder):
    for node in greedy_algo[edge]:
      node_1 = node[0]
      node_2 = node[1]
    #both nodes of the edge mut be in different sets else discard
      if unionFind[node_1] != unionFind[node_2]:
        union(node_1,node_2)
        cluster_count -= 1
        if cluster_count == MIN_CLUSTER:
          break
      elif unionFind[node_1] == unionFind[node_2]:
        continue

    if cluster_count == MIN_CLUSTER:
      break
      
  #find the max spacing by finding the smallest edge crossing any four sets
  max_dist = inf
  num_of_cross_edges = 0
  for edge in greedyPickingOrder:
    for node in greedy_algo[edge]:
      node_1 = node[0]
      node_2 = node[1]
    if unionFind[node_1] != unionFind[node_2]:
      num_of_cross_edges += 1
      if edge < max_dist:
        max_dist = edge
  print(max_dist)
