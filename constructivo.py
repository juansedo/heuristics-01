import numpy as np
import matplotlib.pyplot as plt
import time
from utils import Excel

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
def run(n, R, Q, Th, data, factibility = False):
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

  invalids = set({})
  availables = np.full(R, Q)
  total_distances = np.zeros(R)

  while sum(demands) > 0 and (not factibility or len(invalids) != R):
    valid = []
    for i in range(R):
      actual_node = path[i][-1]
      next_node, distance = getShortestPath(distances[actual_node], demands, availables[i])
      if next_node == 0:
        return_home = distances[actual_node][0]
        total_distances[i] += return_home
        availables[i] = Q
        if actual_node != 0: path[i].append(0)
      else:
        valid.append([i, next_node, distance])

    # Every truck without available capacity
    if len(valid) == 0:
      continue

    actual_truck, next_node, distance = min(valid, key=lambda x: x[2])
    actual_node = path[actual_truck][-1]
    return_home = distances[actual_node][0]

    if availables[actual_truck] == 0:
      total_distances[actual_truck] += return_home
      availables[actual_truck] = Q
      path[actual_truck].append(0)
      if total_distances[actual_truck] > Th: invalids.add(actual_truck)
      continue

    if factibility and total_distances[actual_truck] + distance + distances[next_node][0] > Th:
      invalids.add(actual_truck)
      total_distances[actual_truck] += return_home
      availables[actual_truck] = 0
      if actual_node != 0: path[actual_truck].append(0)
      continue

    total_distances[actual_truck] += distance
    availables[actual_truck] -= demands[next_node]
    demands[next_node] = 0
    path[actual_truck].append(next_node)

  for actual_truck in range(R):
    actual_node = path[actual_truck][-1]
    if actual_node != 0:
      return_home = distances[actual_node][0]
      total_distances += return_home
      path[actual_truck].append(0)

  end = time.time()
  total_time = (end - start) * 1000

  fig, ax = plt.subplots()
  x = []
  y = []

  for node in data:
    x.append(node[1])
    y.append(node[2])

  ax.plot(x, y, 'o', label='Nodos')

  # Plot paths
  for p in path:
    x = []
    y = []
    for node in path[p]:
      x.append(data[node][1])
      y.append(data[node][2])
    ax.plot(x, y, '-', label=f'Camión {p+1}')
    #ax.legend()

  plt.show()

  Excel.add_sheet('CONSTRUCTIVO', path, total_distances, total_time, Th)
  return [path, total_distances, total_time]
