# Algorithms In Python
A repository containing algorithms that I have implemented with python3 to solve a mix of NP and P problems such as the TSP, 2-SAT, Minimum Cut, All Pairs Shortest Paths and many more..


# Files
This repo contains my python implementation of many famous problems and data structures. The README below will describe in more detail the approach i used, the shortcomings of my code, and quirks. All solution files assumes input to be from a text file, the output is formatted based on the problem i was solving. The input and output part will probably throw errors, but the algorithmic implementation is correct. 

# Quick search 
-> [Go to Algorithms Section](##-Algorithms)

-> [Go to Data Structures Section](##-Data-Structures)

## Algorithms

- `HuffmanEncoding-Solution.py` is the greedy solution to building a huffman encoding tree that minimises the average bits needed per character during encoding. 
- `TSP-GeneticAlgorithm-Solution.py` is the genetic algorithmic (GA) solution to the travelling salesman problem (TSP). My GA solution has to has its population and mutation carefully tuned to minimised getting stuck in local optimas. I choose to use a simple ordered crossover during breeding to maintain TSP invariants, and a routelette wheel selection with a swap mutation (cities are swapped). My GA solution has runtime far superior to dyanamic prgramming approaches (~80 seconds versus 720+ seconds).
- `Inversion-Couting-Mergesort.py` A simple alteration to mergesort to use it to count inversions between two arrays
- `JohnsonsAlgorithm-APSP-Solution.py` An algorithm that basically find all shortest paths from all sources to all destinations, also known as the all pairs shortest path problem (APSP). Has time O(n^2 log(n) + nm ).
- `Kargers-Min-Cut-Solution.py` Also known as the random contraction algorithm. Randomly merges two nodes in a graph to find the minimum number of cuts in a given graph, has a small chance of returning the wrong answer. I ran this algorithm 200 times just in case. Has time O(n^2) 
- `Kosaraju-2-SAT-Solution.py` solving the 2-SAT problem by find strongly-connected components. I first build an implication graph given the contraints, then run kosarajus algorithm. If a variable and its negation belongs in the same SCC, then that particular 2-SAT in infeasible. This algorithm does not actually output the answer, but rather determines feasbility.
- `Kruskals-UnionFind-MST.py` Tried to speed up kruskals minimum spanning tree (MST) algorith with my very own implementation of union-find, but im pretty sure i botched it, especially on the union operation, still the algorithm works, just that im not sure if its fast. I did not implement union-by-rank, rather i used the naive unionFind structure.
- `MWIS-DPP-Solution.py` finding the maximum weight indepedant set in a path graph using dynamic programming with a bottom-up tabulation approach. Instead of maintaining a full 2D array, i used a python dictionary to save only the previous results, thereby significantly speeding up my algorithm and saving space.

## Data Structures
-`PositionalDoublyLinkedList.py` is my python implementation of a doubly linked list with a positional wrapper around for arbitrary insertion and deletion anywhere in O(1) time
