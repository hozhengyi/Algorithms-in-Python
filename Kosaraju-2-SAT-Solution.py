
'''
My implementation of kosarajus algorithm on a 2-SAT problem. 
The method i learnt is to find SCCs using kosarajus, and then
fail the 2-SAT if a condition and its negation both belong in the same SCC (i.e. a contradiction).

My code below takes input from a text file but can be easily modified to take in inputs from other sources
'''

from time import time
from sys import getsizeof
def implication_graph_maker(pathname):
  f = open(pathname,"r")
  flines = f.readlines()
  number_of_variables = number_of_clauses = int(flines[0])
  del flines[0]
  start = -1 * (number_of_variables+1)
  end = number_of_variables+1
  adj_list = {x: [] for x in range(start,end)} 
  reversed_adj_list = {x: [] for x in range(start,end)}
  for line in flines:
    line = [int(x) for x in line.split()]
    first_x = line[0]
    second_x = line[1]

    adj_list[-first_x].append(second_x)
    adj_list[-second_x].append(first_x)   

    reversed_adj_list[second_x].append(-first_x)
    reversed_adj_list[first_x].append(-second_x)
  f.close()

  return adj_list, reversed_adj_list



def depth_first_search(source,adj_list,append_rtime_stack):
  global dfsed_nodes
  global rtime_stack
  dfs_stack = [source] 
  scc = set([source])
  while dfs_stack:

    current = dfs_stack[-1]
    found_flag = False
    for head in adj_list[current]:
      if head not in dfsed_nodes:
        found_flag = True
        dfs_stack.append(head)
        dfsed_nodes.add(head)
        scc.add(head)

    if not found_flag:
      end = dfs_stack.pop()
      if append_rtime_stack:
        rtime_stack.append(end)
    
  return scc

def kosaraju_scc_algorithm(adj_list,reversed_adj_list):
  #reverse graph order, heads back to tails
  global dfsed_nodes
  global rtime_stack
  stack = []

  #run multiple dfs on the reversed graph to get rtimes for each node
  rtime_stack = []
  dfsed_nodes = set([])
  for node in reversed_adj_list.keys():  
    if node not in dfsed_nodes:

      dfsed_nodes.add(node)
      _ = depth_first_search(node,reversed_adj_list,True)
         
  
  #run dfs from highest to lowest rtime in the orginal graph to collect all the SCCs
  dfsed_nodes = set([])
  rtime_stack_copy = rtime_stack.copy()
  while rtime_stack_copy:
    
    node = rtime_stack_copy.pop()
    if node not in dfsed_nodes:
      dfsed_nodes.add(node)
      scc = depth_first_search(node,adj_list,False)

    #for each scc, if there exists a node with both its positive and negative version inside, then this sat cannot be satisfied
      unsatisfiable = False
      for candidate in scc:
        if candidate == 0:
          continue
        negation = -1 * candidate
        if negation in scc:
          print(candidate,"and",negation,"found")
          unsatisfiable = True
          break
      if unsatisfiable:
        break
  
  if unsatisfiable:
    return "0"
  else:
    return "1"
