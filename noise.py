import numpy as np
import time
import random
from utils import getDistance

def initialize(n, R, Q, data):
  availables = np.full(R, Q)
  total_distances = np.zeros(R)
  distances = np.zeros((n + 1, n + 1))
  demands = np.zeros(n + 1)
  for node in data:
    values = [getDistance(node[1:3], node2[1:3]) for node2 in data]
    distances[node[0]] = values
    demands[node[0]] = node[3]

  return [distances, demands, availables, total_distances]

def run(n, R, Q, Th, data):
  start = time.time()

  # Initialize data
  distances, demands, availables, total_distances = initialize(n, R, Q, data)
  paths = {i: [0] for i in range(R)}
  i = 0
  error = False

  while sum(demands) > 0:
    candidates = []
    for i in range(R):
      actual_node = paths[i][-1]
      some_trip = False
      for j in range(n+1):
        if 0 < demands[j] and demands[j] <= availables[i]:
          some_trip = True
          candidates.append([i, j, distances[actual_node][j]])

      if not some_trip:
        total_distances[i] += distances[actual_node][0]
        availables[i] = Q
        paths[i].append(0)

    if len(candidates) == 0:
      if error: raise Exception('No solution found!')
      error = True
      continue

    def generateNoise(x):
      rand_value = random.random() * x[2]
      return [x[0], x[1], x[2] + rand_value]

    rcl = list(map(generateNoise, candidates))
    actual_truck, next_node, _ = min(rcl, key=lambda x: x[2])
    actual_node = paths[actual_truck][-1]

    total_distances[actual_truck] += distances[actual_node][next_node]
    availables[actual_truck] -= demands[next_node]
    demands[next_node] = 0
    paths[actual_truck].append(next_node)

  for actual_truck in range(R):
    actual_node = paths[actual_truck][-1]
    if actual_node != 0:
      total_distances[actual_truck] += distances[actual_node][0] # return to depot
      paths[actual_truck].append(0)

  end = time.time()
  total_time = (end - start) * 1000

  return [paths, total_distances, total_time]
