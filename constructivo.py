import numpy as np
import time
from utils import Plot

def getDistance(n1, n2):
  x1, y1 = n1
  x2, y2 = n2
  return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def getShortestPath(distances, demands, available):
  next_node = 0
  value = float('inf')
  for n, distance in enumerate(distances):
    if distance < value and (0 < demands[n] and demands[n] <= available):
      value = distance
      next_node = n
  return [next_node, value]

# n - number of demand nodes
# R - vehicle amount
# Q - vehicle capacity
# Th - maximum distance to travel
# data - "list of lists" with input data (index, x, y, demand)
def run(n, R, Q, Th, data):
  start = time.time()

  # Initialize data
  distances = np.zeros((n + 1, n + 1))
  demands = np.zeros(n + 1)
  for node in data:
    values = [getDistance(node[1:3], node2[1:3]) for node2 in data]
    distances[node[0]] = values
    demands[node[0]] = node[3]

  # Initialize variables
  paths = {}
  for i in range(R):
    paths[i] = [0]

  availables = np.full(R, Q)
  total_distances = np.zeros(R)
  error = False

  while sum(demands) > 0:
    valid = []
    for i in range(R):
      actual_node = paths[i][-1]
      next_node, distance = getShortestPath(distances[actual_node], demands, availables[i])
      if next_node != 0:
        valid.append([i, next_node, distance])
        continue

      if actual_node != 0: # and next_node == 0
        total_distances[i] += distances[actual_node][0] # return to depot
        availables[i] = Q
        paths[i].append(0)

    # Every truck without available capacity
    if len(valid) == 0:
      if error: raise Exception('No solution found!')
      error = True
      continue

    actual_truck, next_node, distance = min(valid, key=lambda x: x[2])
    actual_node = paths[actual_truck][-1]

    total_distances[actual_truck] += distance
    availables[actual_truck] -= demands[next_node]
    demands[next_node] = 0
    paths[actual_truck].append(next_node)

  for actual_truck in range(R):
    actual_node = paths[actual_truck][-1]
    if actual_node != 0:
      total_distances += distances[actual_node][0] # return to depot
      paths[actual_truck].append(0)

  end = time.time()
  total_time = (end - start) * 1000

  Plot.plot(data, paths)
  return [paths, total_distances, total_time]
