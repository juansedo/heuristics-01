import numpy as np
from utils import Excel
import time

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
  path = {}
  for i in range(R):
    path[i] = [0]

  availables = np.full(R, Q)
  t = np.zeros(R)
  total_distances = np.zeros(R)
  actual_truck = 0

  while sum(demands) > 0:
    actual_node = path[actual_truck][-1]
    available = availables[actual_truck]
    return_home = distances[actual_node][0]

    next_node, distance = getShortestPath(distances[actual_node], demands, available)

    if available == 0 or t[actual_truck] + distance + return_home > Th:
      t[actual_truck] = 0
      total_distances[actual_truck] = total_distances[actual_truck] + return_home
      availables[actual_truck] = Q
      path[actual_truck].append(0)
      continue

    t[actual_truck] = t[actual_truck] + distance
    total_distances[actual_truck] = total_distances[actual_truck] + distance
    availables[actual_truck] = available - demands[next_node]
    demands[next_node] = 0
    path[actual_truck].append(next_node)

    actual_truck = (actual_truck + 1) % R

  for actual_truck in range(R):
    actual_node = path[actual_truck][-1]
    return_home = distances[actual_node][0] if actual_node != 0 else 0
    total_distances[actual_truck] = total_distances[actual_truck] + return_home
    path[actual_truck].append(0)

  end = time.time()
  total_time = (end - start) * 1000
  Excel.add_sheet('CONSTRUCTIVO', path, distances, total_time, Th)
  return [path, total_distances, total_time]
