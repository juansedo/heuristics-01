#%%
from xlwt import Workbook
import os
from dotenv import load_dotenv

import constructivo as Constructivo
# import grasp
# import ruido

load_dotenv()

OUTPUTS_PATH = os.getenv('OUTPUTS_PATH', './outputs')
DATA_PATH = os.getenv('DATA_PATH', './data')

def readTestFile(id):
  with open(f'{DATA_PATH}mtVRP{id}.txt') as f:
    lines = [line.rstrip() for line in f]
    lines = [line.split() for line in lines]
    lines = [[int(x) for x in line] for line in lines]
  return lines

wb = Workbook()
sheet1 = wb.add_sheet('PRUEBA')

nsol=100
alpha=0.5
K=5
r=5

for id in range(1,2):
  data = readTestFile(1)
  n, R, Q, Th = data[0]
  data = data[1:]

  path, distances, total_time = Constructivo.run(n, R, Q, Th, data)

  print('-----------------')
  sheet1.write(0, 0, 'Hola mundo')
  for i in range(0, R):
    size = len(path[i])
    for j in range(size):
      sheet1.write(i + 1, j, path[i][j])
      print(path[i][j], end=' ')
    sheet1.write(i + 1, size, distances[i])
    sheet1.write(i + 1, size + 1, 1 if distances[i] > Th else 0)
    print(f'({distances[i]}, {1 if distances[i] > Th else 0})')
  sheet1.write(R + 1, 1, sum(distances))
  sheet1.write(R + 1, 2, total_time)
  sheet1.write(R + 1, 3, 1)
  print(f'[{sum(distances)}, {total_time}, {1}]')
  print('-----------------')

  wb.save(OUTPUTS_PATH + 'result.xls')