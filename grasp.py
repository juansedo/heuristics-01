import numpy as np
import time
from utils import Excel
import random

def getDistance(n1, n2):
  x1, y1 = n1
  x2, y2 = n2
  return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def run(n, R, Q, Th, alpha, data):
  start = time.time()

  # Initialize data
  distances = np.zeros((n + 1, n + 1))
  demands = np.zeros(n + 1)
  for node in data:
    values = [getDistance(node[1:3], node2[1:3]) for node2 in data]
    distances[node[0]] = values
    demands[node[0]] = node[3]

  # Initialize variables
  path = {}
  for i in range(R):
    path[i] = [0]

  class Truck:
    max_capacity = Q

    def __init__(self, id):
      self.id = id
      self.path = [0]
      self.total_traveled = 0
      self.last_traveled = 0
      self.available_capacity = Truck.max_capacity

    def goTo(self, next_node):
      actual_node = self.path[-1]
      self.path.append(next_node)
      self.total_traveled += distances[actual_node][next_node]
      self.last_traveled += distances[actual_node][next_node]
      self.available_capacity -= demands[next_node]

    def returnHome(self):
      actual_node = self.path[-1]
      self.path.append(0)
      self.total_traveled += distances[actual_node][0]
      self.last_traveled = 0
      self.available_capacity = Truck.max_capacity

  trucks = [Truck(i) for i in range(R)]
  i = 0

  while sum(demands) > 0:
    actual_node = trucks[i].path[-1]
    candidates = {}
    for j in range(n+1):
      if 0 < demands[j] and demands[j] <= trucks[i].available_capacity:
        candidates[j] = distances[actual_node][j]

    if len(candidates) == 0:
      trucks[i].returnHome()
      continue

    c_min = min(candidates.values())
    c_max = max(candidates.values())

    rcl = list(filter(lambda x: distances[actual_node][x] <= c_min + alpha * (c_max - c_min), candidates))
    c = random.choice(rcl)

    trucks[i].goTo(c)
    demands[c] = 0

    i = (i + 1) % R

  for k in range(R):
    trucks[k].returnHome()

  end = time.time()
  total_time = (end - start) * 1000
  paths = list(map(lambda x: x.path, trucks))
  dist = list(map(lambda x: x.total_traveled, trucks))
  Excel.add_sheet('GRASP', paths, dist, total_time, Th)
  return [paths, dist, total_time]
