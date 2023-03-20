#%%
from utils import ExcelBook, TestFile, Plot
import sys

import constructivo as Constructivo
import grasp as GRASP
import noise as Noise

def runConstructivo():
  paths, distances, time = Constructivo.run(n, R, Q, Th, data)
  excel = ExcelBook(f'mtVRP_{author}_Constructivo.xls')
  excel.add_sheet('0', paths, distances, time, Th, verbose = False)

  Plot.plot(data, paths)

  print(f'-----------------')
  print(f'CONSTRUCTIVO Summary')
  print(f'Iterations: 1, Time: {time:.2f} ms')
  print(f'Distance: {sum(distances):.2f} m')
  excel.save()
  print(f'-----------------\n')

def runGRASP():
  x = []
  y = []
  times = []
  result_paths = []
  excel = ExcelBook(f'mtVRP_{author}_GRASP.xls')

  for i in range(iterations):
    paths, distances, time = GRASP.run(n, R, Q, Th, alpha, data)
    y.append(f'{i + 1} ({time:.2f} ms)')
    x.append(sum(distances))
    times.append(time)
    result_paths.append(paths)
    excel.add_sheet(str(i), paths, distances, time, Th, verbose = False)

  Plot.plotDistances(y, x)

  min_iteration = x.index(min(x))
  Plot.plot(data, result_paths[min_iteration])

  print(f'-----------------')
  print(f'GRASP Summary')
  print(f'Iterations: {iterations}, alpha: {alpha}')
  print(f'Avg. distance: {sum(x)/len(x):.2f} m, Avg. time: {sum(times)/len(times):.2f} ms')
  print(f'Lowest distance: ({min(x):.2f} m, {times[min_iteration]:.2f} ms)')
  excel.save()
  print(f'-----------------\n')

def runNoise():
  x = []
  y = []
  times = []
  result_paths = []
  excel = ExcelBook(f'mtVRP_{author}_Noise.xls')

  for i in range(iterations):
    paths, distances, time = Noise.run(n, R, Q, Th, data)
    y.append(f'{i + 1} ({time:.2f} ms)')
    x.append(sum(distances))
    times.append(time)
    result_paths.append(paths)
    excel.add_sheet(str(i), paths, distances, time, Th, verbose = False)

  Plot.plotDistances(y, x)

  min_iteration = x.index(min(x))
  Plot.plot(data, result_paths[min_iteration])

  print(f'-----------------')
  print(f'Noise Summary')
  print(f'Iterations: {iterations}, Distribution: Uniform')
  print(f'Avg. distance: {sum(x)/len(x):.2f} m, Avg. time: {sum(times)/len(times):.2f} ms')
  print(f'Lowest distance: ({min(x):.2f} m, {times[min_iteration]:.2f} ms)')
  excel.save()
  print(f'-----------------\n')

if __name__ == '__main__':
  author = 'JSDIAZO'
  file = 0
  iterations = 1
  alpha = 1

  if len(sys.argv) == 2 and sys.argv[1] == '--default':
    file = 12
    iterations = 100
    alpha = 0.02
  elif len(sys.argv) == 4:
    file = int(sys.argv[1])
    iterations = int(sys.argv[2])
    alpha = float(sys.argv[3])
  else:
    print(f'main.py: missing arguments, try: \'python3 main.py FILE_ID ITERATIONS ALPHA\'\n')
    exit()

  data = TestFile.getById(file)
  n, R, Q, Th = data[0]
  data = data[1:]

  print(f'--> mtVRP{file}.txt')
  print(f'--> Iterations: {iterations}, alpha for GRASP: {alpha}\n')

  runConstructivo()
  runGRASP()
  runNoise()

# %%
