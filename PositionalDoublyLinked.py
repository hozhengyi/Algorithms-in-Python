class _DoublyLinkedBase:
  class _Node:
    '''lightweight nonpublic class for representing a doubly linked node'''
    __slots__ = '_value', '_prev', '_next'
    def __init__(self,val,prev,next):
      self._value = val
      self._prev = prev
      self._next = next
  def __init__(self):
    '''creates empty ddlist with header and trailer'''
    self._header = self._Node(None,None,None)
    self._trailer = self._Node(None,None,None)
    self._header._next = self._trailer
    self._trailer._prev = self._header
    self._size = 0

  def __len__(self):
    return self._size
  
  def is_empty(self):
    return self._size == 0
  
  def _insert_between(self,val,prev,next):
    insertee = self._Node(val,prev,next)
    prev._next = insertee
    next._prev = insertee
    self._size += 1
    return insertee

  def _delete_node(self,node):
    before = node._prev
    after = node._next
    before._next = after
    after._prev = before
    deleted_val = node._value
    del node
    self._size -= 1
    return deleted_val

class PositionalList(_DoublyLinkedBase):
  class Position:
    def __init__(self,container,node):
      '''constructor should not be invoked by user'''
      self._container = container
      self._node = node
    
    def value(self):
      return self._node._value

    def __eq__(self,other):
      return type(other) is type(self) and other._node is self._node
    
    def __ne__(self,other):
      return not (self==other)

  def _validate(self,p):
    '''return position's node or raise error if invalid'''
    if not isinstance(p,self.Position):
      raise TypeError("p must be a proper Position type")
    if p._container is not self:
      raise TypeError("p does not belong to this container")
    if p._node._next is None:
      raise ValueError("p is no longer valid")
    return p._node
  
  def _make_position(self,node):
    """creates and return a Position instance for a given node(or None if sentinel node)"""
    if (node is self._header) or (node is self._trailer):
      return None
    else:
      return self.Position(self,node)
  
  def first(self):
    return self._make_position(self._header._next)
  
  def last(self):
    return self._make_position(self._trailer._prev)

  def before(self,p):
    '''move cursor backward'''
    node = self._validate(p)
    return self._make_position(node._prev)
  
  def after(self,p):
    '''move cursor forward'''
    node = self._validate(p)
    return self._make_position(node._next)

  def __iter__(self):
    cursor = self.first()
    while cursor is not None:
      yield cursor.value()
      cursor = self.after(cursor)

  def _insert_betwen(self,val,prev,next):
    '''insert in arbitrary position and return cursor at position'''
    node = super()._insert_between(val,prev,next)
    return self._make_position(node)
  
  def add_first(self,e):
    '''insert new first and return cursor at first'''
    return self._insert_between(e,self._header,self._header._next)

  def add_last(self,e):
    '''insert new last and return cursor at last'''
    return self._insert_between(e,self._trailer._prev,self._trailer)
  
  def add_before(self, prev, val):
    '''insert element after prev and mvoe cursor ther'''
    prev_node = prev._validate(prev)
    return self._insert_between(val,prev_node._prev,prev_node)

  def add_after(self, prev, val):
    '''insert element after prev and mvoe cursor ther'''
    prev_node = prev._validate(prev)
    return self._insert_between(val,prev_node,prev_node._next)
  
  def delete(self,p):
    '''remove cursor and returns the element at cursor'''
    og = self._validate(p)
    return self._delete_node(og)
  
  def replace(self, p, e):
    '''replace the element at p with new elem and return former elem'''
    og = self._validate(p)
    old_val = og._value
    og._value = e
    return old_val
  
  def find_max(self):
    iter_list = iter(self)
    max_val = next(iter_list)
    for i in iter_list:
      if i > max_val:
        max_val = i
    return max_val

  def find(self, query):
    start = self.first()
    for _ in range(self._size):
      if start.value() == query:
        return start
      start = self.after(start)
    return None
  
  def find_recursive(self,query, p):
    start = p
    if start is None:
      return None 
    if start.value() == query:
      return start
    found = self.find_recursive(query, self.after(p))
    return found
  
  def __reversed__(self):
    start = self.last()
    for _ in range(len(self)):
      yield start.value()
      start = self.before(start)
