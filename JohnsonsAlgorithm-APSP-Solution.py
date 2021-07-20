'''
My implementation of johnsons algorithm to find all pairs shortest path (APSP) in a graph with cycles (possibly negative) and possible
negative edges. I used a vanilla heap implementation of dijkstra's algorithm to speed up the runtime.
'''


from heapq import heapify
from heapq import heappush
from heapq import heappop
from time import time
from math import inf

#Johnson's APSP Algorithm
'''
revision notes
1. graph could be directed, therefore need to add an entry from 1-2 and 2-1 
2. check that each head for a give node in adj_list is represent (m_cost,v2) rather than (v2, m_cost)
'''
def adjacency_list_creator(pathname):
  #take one path name of file and output adjacency list
  f = open(pathname,"r")
  flines = f.readlines()
  num_vertices = int(flines[0].split()[0]) #first row is [num_vertices, num_edges]
  del flines[0] 

  adj_list = {x: {'in':[],'out':[]} for x in range(1,num_vertices+1)}
  
  for line in flines:
    line = line.split() #each line is [v1, v2, m_cost]
    v1 = int(line[0])
    v2 = int(line[1])
    m_cost = int(line[2])
    adj_list[v1]['out'].append((m_cost, v2)) #each head is represented cost-first then node due to heap implementaion
    adj_list[v2]['in'].append((m_cost,v1))

  f.close()
  return adj_list

def bellmanFord(adj_list,source):
  # adj_list must be the following format -> {node: {'in':[list of incoming tuples (dist,node)], 'out':[list of incoming tuples (dist,node)]}}
  assert adj_list.get(source) != None
  adj_list_len = len(adj_list)
  set_x = set()
  # setting up base case
  dist_dict = [{},{}]
  dist_dict[0] = {x:inf for x in range(1,adj_list_len+1)}
  dist_dict[1] = {x:inf for x in range(1,adj_list_len+1)}
  dist_dict[0][source] = 0
  zero_filled = True

  for allowable_node_length in range(1,adj_list_len+1): 
    changed = False
    #zero_filled is a flag that alternates array to save space
    if zero_filled:
      previous, current = 0,1
      zero_filled = False
    else:
      previous, current = 1,0
      zero_filled = True

    for destination in adj_list.keys():
      #for all w going to v
      min_w = inf
      for w_cost, w in adj_list[destination]['in']:
        if dist_dict[previous][w] + w_cost < min_w:
          min_w = dist_dict[previous][w] + w_cost

      if min_w < dist_dict[previous][destination]:
        changed = True

      dist_dict[current][destination] = min(dist_dict[previous][destination],min_w)

    #early stopping
    if not changed:
      break

    #CHECK FOR NEGATIVE CYCLES
    if allowable_node_length == adj_list_len and changed:
      raise Exception("Negative cycle detected with bellmanford!")
      
  if zero_filled:
    return dist_dict[0]
  else:
    return dist_dict[1]

def dijkstrasHeap(adj_list, source):
  # adj_list must be the following format -> {node: {'in':[list of incoming tuples (dist,node)], 'out':[list of incoming tuples (dist,node)]}}
  assert adj_list.get(source) != None
  adj_list_len = len(adj_list)
  set_x = set()
  dist_dict = {x:inf for x in range(1,adj_list_len+1)}
  dist_dict[source] = 0
  heap = [(0,source)] #all dist set as inf except for source vertex
  heapify(heap) 
  
  while len(heap) != 0:
    #take the lowest greedy score from the heap and add in set_x
    min_elem = heappop(heap)
    choosen_vertex = min_elem[1]
    dist_weight = min_elem[0]
    adjacent_nodes = adj_list[choosen_vertex]['out']
    set_x.add(choosen_vertex)

    #update greedy score values for new frontiers into set_x
    for adjacent_node in adjacent_nodes:
      m_cost = adjacent_node[0]
      v2 = adjacent_node[1]
      # only add node if not in set_x and m_cost is lower than in dist_dict
      if ( dist_dict[v2] > m_cost + dist_weight) and (v2 not in set_x):   
        heappush(heap, (m_cost + dist_weight,v2))
        dist_dict[v2] = m_cost + dist_weight

  return dist_dict


def johnsonsAlgoForAPSP(adj_list):
  # adj_list must be the following format -> {node: {'in':[list of incoming tuples (dist,node)], 'out':[list of incoming tuples (dist,node)]}}
  adj_list_len = len(adj_list)
  johnsons_dict = {x:0 for x in range(1,adj_list_len+1)}

  #modify the adj_list into a purely postive edge graph using bellman-ford by adding an offset to negative edges
  artificial_node_name = adj_list_len + 1
  artificial_node_cost = 0
  adj_list[artificial_node_name] = {'in':[]}
  adj_list[artificial_node_name]['out'] = [(artificial_node_cost,v) for v in range(1,adj_list_len+1)]
  for key in adj_list.keys():
    adj_list[key]['in'].append((artificial_node_cost,artificial_node_name))

  dict_of_offset_values = bellmanFord(adj_list,artificial_node_name)
  modified_adj_list = {x: {'in':[],'out':[]} for x in range(1,adj_list_len+1)}
  del adj_list[artificial_node_name]

  for source in adj_list.keys():
    for old_edge, vertex in adj_list[source]['out']:
      p_u = dict_of_offset_values[source]
      p_v = dict_of_offset_values[vertex]
      new_edge = old_edge + p_u - p_v
      modified_adj_list[source]['out'].append((new_edge,vertex))
 
  #using the modified adj_list, run dijkstras for every single source-destination pair
  #also undos the offset for each djikstra pair result before adding to johnson_dict
  smallest_APSP = inf
  for source in modified_adj_list.keys():
    tmp = dijkstrasHeap(modified_adj_list,source)
    for key in tmp.keys():
      p_u = dict_of_offset_values[source]
      p_v = dict_of_offset_values[key]
      tmp[key] = tmp[key] - p_u + p_v
      
      if tmp[key] < smallest_APSP:
        smallest_APSP = tmp[key]
  

    johnsons_dict[source] = tmp 

  #return johnsons_dict
  return smallest_APSP
