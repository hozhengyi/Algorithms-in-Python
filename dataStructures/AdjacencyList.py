class Graph:
  '''an adajacency list representation of a graph. uses vertex and edges objects'''


  class Vertex:
  '''a vertex object that stores an value'''
  __slots__ = '_value'
  def __init__(self,x):
    self._value = x
  
  def get_value(self):
    '''the value attribute is read-only, making the hash function stable'''
    return self._value
  
  def __hash__(self):
    '''allows Vertex object to be hashed using python dicts'''
    return hash(self._value)
#------------------------------------------------------

  class Edge:
    '''an edge object that store endpoints and the edges weight'''
    __slots__ = '_u' , '_v', '_cost'
    def __init__(self,u,v,cost = 1):
      self._u = u
      self._v = v
      self._cost = cost
    
    def get_cost(self):
      ''' the cost attribute is read-only, making the hash function stable'''
      return self._cost

    def endpoints(self):
      return self._u, self._v

    def opposite(self,query):
      '''returns None if query is not the endpoints of this edge, else return the other endpoint'''
      if (query is not self._u) and (query is not self._v):
        return None
      elif query is not self._u:
        return self._v
      else:
        return self._u
    
    def __hash__(self):
      '''allows Edge object to be hashed using python dicts'''
      hash(self.endpoints())
#------------------------------------------------------ 

  def __init__(self, directed = False):
    '''the Graph is made out of two dictionary of vertexes if directed, else one only'''
    self._outgoing = {}
    self._incoming = {} if directed else self._outgoing
    self._directed = directed
    self._vertex_count = 0
    self._edge_count = 0

  def vertices_view(self):
    '''creates a view of all vertex objects in this graph'''
    return self._outgoing.keys():
  
  def edges_view(self):
    '''creates a view of all edge objects in this graph (including parallel edges)'''
    result = set()
    if self._directed: #directed case
      for head in self._outgoing.values():
        result.update(head.values())
      for head in self._incoming.values(): #incoming edges are differnet objeects
        result.update(head.values())
    else: #non directed case
      for head in self._outgoing.values(): #outgoing edges have duplicates because assigned twice
        result.update(head.values())
    
    return result

  def edge_count(self):
    return self._vertex_count

  def vertex_count(self):
    return self._edge_count
  
  def insert_vertex(self,value):
  '''inserts Vertex object into graph and returns said object'''
    v = self.Vertex(value)
    self._outgoing[v] = {}
    if self._directed:
      self._incoming[v] = {}
    return v

  def degree(self, v, report_outgoing = True):
    '''return number of edges for a given vertex in this graph'''
    edges = self._outgoing[v] if report_outgoing else self._incoming[v] #report_outgoing doesnt make a different if graph is undirected
    return len(edges)

  def incident_edges(self,v,report_outgoing = True):
    '''return iterator of incident edges for a given vertex in this graph'''
    edges = self._outgoing[v] if report_outgoing else self._incoming[v] #report_outgoing doesnt make a different if graph is undirected
    for edge in edges.values():
      yield edge

  def insert_edge(self,tail,head,cost):
    e = self.Edge(tail,head,cost)
    #error checks
    if (not isinstance(tail,self.Vertex) )and (not isinstance(head,self.Vertex)): raise TypeError("tail and head must be a Vertex object")
    if not isinstance(cost,(int,float)): raise TypeError("cost must be int or float type")
    if tail is head: raise ValueError("Self referencing edges not allowed!")

    self._outgoing[tail][head] = cost
    self._incoming[head][tail] = cost
