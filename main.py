#%%
from utils import ExcelBook, TestFile, Plot

import constructivo as Constructivo
import grasp as GRASP
import noise as Noise

author = 'JSDIAZO'

def main():
  builderExcel = ExcelBook(f'mtVRP_{author}_Constructivo.xls')
  graspExcel = ExcelBook(f'mtVRP_{author}_GRASP.xls')
  noiseExcel = ExcelBook(f'mtVRP_{author}_Noise.xls')

  for fileId in range(1, 13):
    data = TestFile.getById(fileId)
    n, R, Q, Th = data[0]
    data = data[1:]
    iterations = 20
    alpha = 0.02

    print(f'--> mtVRP{fileId}.txt')

    result = runConstructivo(n, R, Q, Th, data)
    builderExcel.add_sheet(str(fileId), result, Th)
    #Plot.plot(data, result[0])

    result = runGRASP(n, R, Q, Th, data, iterations, alpha)
    graspExcel.add_sheet(str(fileId), result, Th)
    #Plot.plot(data, result[0])

    result = runNoise(n, R, Q, Th, data, iterations)
    noiseExcel.add_sheet(str(fileId), result, Th)
    #Plot.plot(data, result[0])

  builderExcel.save()
  graspExcel.save()
  noiseExcel.save()

def runConstructivo(n, R, Q, Th, data):
  paths, distances, time = Constructivo.run(n, R, Q, Th, data)

  print(f'-----------------')
  print(f'CONSTRUCTIVO Summary')
  print(f'Iterations: 1')
  print(f'Distance: {sum(distances):.2f} m ({time:.2f} ms)')
  print(f'-----------------\n')
  return [paths, distances, time]

def runGRASP(n, R, Q, Th, data, iterations, alpha):
  times = []
  result_paths = []

  best = [None, None, None]

  for i in range(iterations):
    paths, distances, time = GRASP.run(n, R, Q, Th, alpha, data)
    times.append(time)
    result_paths.append(paths)

    if best[1] is None or sum(distances) < sum(best[1]):
      best[0] = paths
      best[1] = distances
      best[2] = time

  print(f'-----------------')
  print(f'GRASP Summary')
  print(f'Iterations: {iterations}, alpha: {alpha}')
  print(f'Best distance: {sum(best[1]):.2f} m ({best[2]:.2f} ms)')
  print(f'-----------------\n')
  return best

def runNoise(n, R, Q, Th, data, iterations):
  times = []
  result_paths = []

  best = [None, None, None]

  for i in range(iterations):
    paths, distances, time = Noise.run(n, R, Q, Th, data)
    times.append(time)
    result_paths.append(paths)

    if best[1] is None or sum(distances) < sum(best[1]):
      best[0] = paths
      best[1] = distances
      best[2] = time

  print(f'-----------------')
  print(f'Noise Summary')
  print(f'Iterations: {iterations}')
  print(f'Best distance: {sum(best[1]):.2f} m ({best[2]:.2f} ms)')
  print(f'-----------------\n')
  return best

if __name__ == '__main__':
  main()

# %%
