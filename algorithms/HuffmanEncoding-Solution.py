'''
My implementation of building a huffman tree to encode a range of inputs with the least bits per character as possible

'''


def HuffmanCodingTwoQueue():
  from queue import Queue
  from binarytree import Node
  QUEUE_SIZE = 1001
  NUM_OF_SYMBOLS = 1000 

  #read file
  f = open("/content/drive/MyDrive/huffman.txt","r")
  flines = f.readlines()
  del flines[0]
  weight_list = [int(x) for x in flines]
  weight_list.sort() #least weights get deepest leaf nodes

  #instantiate empty queue
  queue_1 = Queue(maxsize = QUEUE_SIZE)
  queue_2 = Queue(maxsize = QUEUE_SIZE)

  #the four variables below are a workaround to peek at queue values in constant time for comparisons later without actually dequeing
  #q1_idx and q1_idx will be bumped by 1 whenvee q1 or q2 is dequeued so that the index pointer is at the right place during ocmparisons
  q1_compare = []
  q2_compare = []
  q1_idx = 0
  q2_idx = 0

  #fill up first queue only (for now)
  for weight in weight_list:
    queue_1.put( Node(weight) ) 
    q1_compare.append(weight)
  # while huffman tree not formed yet
  while True:
    selected = []
    
    #draw the two lowest weights from the queues to conjoin into one tree
    for i in range(2):
      if not queue_1.empty() and queue_2.empty():
        selected.append(queue_1.get())
        q1_idx += 1
      elif queue_1.empty() and not queue_2.empty():
        selected.append(queue_2.get())
        q2_idx += 1
      else:
        #peek at queue without dequeuing using the workaround mentioned above
        q1 = q1_compare[q1_idx]
        q2 = q2_compare[q2_idx]
        if q1 < q2:
          selected.append(queue_1.get())
          q1_idx += 1
        else:
          selected.append(queue_2.get())
          q2_idx += 1

    #tree conjoining process
    meta_weight = selected[0].value + selected[1].value
    root = Node(meta_weight)
    root.left = selected[0]
    root.right = selected[1]
    queue_2.put(root)
    q2_compare.append(meta_weight)
    #break if tree is fully formed
    if queue_2.qsize() == 1 and queue_1.empty():
      break

  #traversing completed tree to get height and value info of leaf
  #multiple those together and add it to a running sum to get average encoding bits per symbol
  completed_tree = queue_2.get()
  level_list = completed_tree 

  print("MIN BIT =",completed_tree.min_leaf_depth)
  print("MAX BIT =",completed_tree.max_leaf_depth)
