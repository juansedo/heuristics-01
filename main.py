#%%
from utils import Excel, TestFile, Plot

import constructivo as Constructivo
import grasp as GRASP
import ruido as Ruido

def runConstructivo():
  paths, distances, time = Constructivo.run(n, R, Q, Th, data)
  Excel.add_sheet('CONSTRUCTIVO', paths, distances, time, Th, verbose = False)

  Plot.plot(data, paths)

  print(f'-----------------')
  print(f'CONSTRUCTIVO Summary')
  print(f'Iterations: 1, Time: {time:.2f} ms')
  print(f'Distance: {sum(distances)}')
  print(f'-----------------')

def runGRASP():
  x = []
  y = []
  times = []
  result_paths = []
  for i in range(iterations):
    paths, distances, time = GRASP.run(n, R, Q, Th, alpha, data)
    y.append(f'{i + 1} ({time:.2f} ms)')
    x.append(sum(distances))
    times.append(time)
    result_paths.append(paths)
    Excel.add_sheet('GRASP', paths, distances, time, Th, offset = i * (R + 2), verbose = False)

  Plot.plotDistances(y, x)

  min_iteration = x.index(min(x))
  Plot.plot(data, result_paths[min_iteration])

  print(f'-----------------')
  print(f'GRASP Summary')
  print(f'Iterations: {iterations}, alpha: {alpha}, Avg. time: {sum(times)/len(times):.2f} ms')
  print(f'Lowest distance: {min(x)}, Highest distance: {max(x)}, Avg. distance: {sum(x)/len(x):.2f}')
  print(f'-----------------')

def runRuido():
  x = []
  y = []
  times = []
  result_paths = []
  for i in range(iterations):
    paths, distances, time = Ruido.run(n, R, Q, Th, data)
    y.append(f'{i + 1} ({time:.2f} ms)')
    x.append(sum(distances))
    times.append(time)
    result_paths.append(paths)
    Excel.add_sheet('Ruido', paths, distances, time, Th, offset = i * (R + 2), verbose = False)

  Plot.plotDistances(y, x)

  min_iteration = x.index(min(x))
  Plot.plot(data, result_paths[min_iteration])

  print(f'-----------------')
  print(f'Ruido Summary')
  print(f'Iterations: {iterations}, Avg. time: {sum(times)/len(times):.2f} ms')
  print(f'Lowest distance: {min(x)}, Highest distance: {max(x)}, Avg. distance: {sum(x)/len(x):.2f}')
  print(f'-----------------')

alpha=0.02
iterations=100
file=12

data = TestFile.getById(file)
n, R, Q, Th = data[0]
data = data[1:]

Excel.start()

runConstructivo()
runGRASP()
runRuido()

Excel.save()
# %%
