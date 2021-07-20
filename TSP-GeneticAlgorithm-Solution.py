'''
My implementation of solving a small TSP instance (maybe around 30-40) cities using my custom implementation
of genetic algorithm. I admit my genetic algorithm implementation may need further optimizing, but the runtime is far
superior to other methods such as using dynamic programming (80seconds versus 720 seconds)
'''


import numpy as np
from random import sample
from random import random
from random import shuffle
from time import time
import operator
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt
from math import hypot

class City:
  def __init__(self,x,y):
    self.x = x
    self.y = y
 
  def distance(self,target):
    return hypot(self.x - target.x, self.y - target.y)

  def __repr__(self):
    return "(" + str(self.x) + "," + str(self.y) + ")"

class Fitness:
  def __init__ (self, route):
    self.route = route
    self.distance = 0
    self.fitness = 0.0

  def routeDistance(self): 
    pathDistance = 0
    route_len = len(self.route)
    for i in range(0, route_len):
      fromCity = self.route[i]
      if i+1 < route_len:
        toCity = self.route[i+1]
      else:
        toCity = self.route[0]
      pathDistance += fromCity.distance(toCity)
       
    self.distance = pathDistance
    
    return self.distance
  
  def routeFitness(self):
    if self.fitness == 0:
      self.fitness = 1 / float(self.routeDistance())
    return self.fitness

def createRoute(cityList):
  route = sample(cityList, len(cityList))
  return route

def initialisePopulation(popSize, cityList):
  population = []
  for i in range(0,popSize):
    population.append(createRoute(cityList))
  return population


def rankRoutes(population):
  fitnessResults = {}
  for idx, route in enumerate(population):
    fitnessResults[idx] = Fitness(route).routeFitness()
  return sorted(fitnessResults.items(), key = lambda x: x[1], reverse = True)

#revision needed: why use cumlative sum?
def selection(popSorted, eliteSize):
  selectionResults = []
  df = pd.DataFrame(np.array(popSorted), columns = ["Index", "Fitness"])
  df["cumulative_sum"] = df.Fitness.cumsum()
  df["cumulative_percentage"] = 100 * (df.cumulative_sum / df.Fitness.sum() ) 

  for i in range(0, eliteSize):
    selectionResults.append(popSorted[i][0])
  for i in range(0, len(popSorted) - eliteSize):
    pick = 100 * random()
    for i in range(0, len(popSorted) ):
      if pick <= df.iat[i,3]:
        selectionResults.append(popSorted[i][0])
        break

  return selectionResults

def matingPool(population, selectionResults):
  matingpool = []
  for i in range(0, len(selectionResults)):
    idx = selectionResults[i]
    matingpool.append(population[idx])
  return matingpool

#due to the tsp problem, breeding has to occur via ordered crossover
def breed(parent1,parent2):
  
  childP1_set = set([])
  childP2 = []
  childP1= []

  geneA = int(random() * len(parent1))
  geneB = int(random() * len(parent1))

  startGene = min(geneA,geneB)
  endGene = max(geneA,geneB)

  for i in range(startGene,endGene):
    childP1_set.add(parent1[i])
    childP1.append(parent1[i])

  childP2 = [x for x in parent2 if x not in childP1_set] 

  return childP1 + childP2

def breedPopulation(matingpool,eliteSize):
  children = []
  len_matingpool = len(matingpool)
  shuffled_pool = sample(matingpool, len_matingpool)

  for i in range(0, eliteSize):
    children.append(matingpool[i])

  #revision needed: instead of breeding first and last ones, maybe try breeding adjacent mates
  for i in range(0, len_matingpool-eliteSize):
    child = breed(shuffled_pool[i], shuffled_pool[len_matingpool-i-1])
    children.append(child)
  
  return children

#revision needed: alter how to randomly pick cities to mutate
def mutate(route,mutationRate):
  for idx_1 in range(len(route)):
    if (random() < mutationRate):
      idx_2 = int(random() * len(route))

      route[idx_1], route[idx_2] =  route[idx_2], route[idx_1]
  
  return route

def mutatePopulation(population, mutationRate):
  return [mutate(route,mutationRate) for route in population]

def nextGeneration(currentGen, eliteSize, mutationRate):

  popSortedByFitness = rankRoutes(currentGen)
  
  selectionResults = selection(popSortedByFitness, eliteSize)

  matingpool = matingPool(currentGen,selectionResults)

  children = breedPopulation(matingpool, eliteSize)

  nextGeneration = mutatePopulation(children,mutationRate)

  return nextGeneration

def geneticAlgorithm(cityList,populationSize, eliteSize, mutationRate, generations):
  population = initialisePopulation(populationSize, cityList)
  

  for i in range(1,generations+1):
    if (i % 20 == 0) or (i == 1):
      print("Best distance of generation",i,":", str(1/rankRoutes(population)[0][1]))
    population = nextGeneration(population, eliteSize, mutationRate)
  
  bestRouteIndex = rankRoutes(population)[0][0]
  print("The Best Route is:")
  print(population[bestRouteIndex])

  


f = open("/content/drive/MyDrive/tsp.txt","r")
flines = f.readlines()
num_of_nodes = int(flines[0])
del flines[0]
flines = [tuple(x.split()) for x in flines]
cityList = []
for i in range(num_of_nodes):
  cityList.append( City(x = float(flines[i][0]),y = float(flines[i][1])) )

s = time()
geneticAlgorithm(cityList,100,20,0.01,500)
e = time()
print('TOTAL TIME TAKEN:',e-s)
