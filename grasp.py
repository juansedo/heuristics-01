import numpy as np
import time
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
  paths = {i: [0] for i in range(R)}
  availables = np.full(R, Q)
  total_distances = np.zeros(R)

  i = 0

  while sum(demands) > 0:
    actual_node = paths[i][-1]
    candidates = {}
    for j in range(n+1):
      if 0 < demands[j] and demands[j] <= availables[i]:
        candidates[j] = distances[actual_node][j]

    if len(candidates) == 0:
      total_distances[i] += distances[actual_node][0]
      availables[i] = Q
      paths[i].append(0)
      #i = (i + 1) % R
      continue

    c_min = min(candidates.values())
    c_max = max(candidates.values())

    upper_bound = c_min + alpha * (c_max - c_min)
    rcl = list(filter(lambda x: distances[actual_node][x] <= upper_bound, candidates))
    next_node = random.choice(rcl)

    total_distances[i] += distances[actual_node][next_node]
    availables[i] -= demands[next_node]
    demands[next_node] = 0
    paths[i].append(next_node)

    i = (i + 1) % R

  for actual_truck in range(R):
    actual_node = paths[actual_truck][-1]
    if actual_node != 0:
      total_distances[actual_truck] += distances[actual_node][0] # return to depot
      paths[actual_truck].append(0)

  end = time.time()
  total_time = (end - start) * 1000

  return [paths, total_distances, total_time]
