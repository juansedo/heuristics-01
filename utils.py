from xlwt import Workbook
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

OUTPUTS_PATH = os.getenv('OUTPUTS_PATH', './outputs')

class Excel:
  wb = None

  def start():
    Excel.wb = Workbook()

  def add_sheet(title, paths, distances, total_time, Th):
    print('-----------------' + title)
    sheet1 = Excel.wb.add_sheet(title)
    R = len(paths)
    for i in range(0, R):
      size = len(paths[i])
      for j in range(size):
        sheet1.write(i + 1, j, paths[i][j])
        print(paths[i][j], end=' ')
      sheet1.write(i + 1, size, distances[i])
      sheet1.write(i + 1, size + 1, 1 if distances[i] > Th else 0)
      print(f'({distances[i]}, {1 if distances[i] > Th else 0})')
    sheet1.write(R + 1, 1, sum(distances))
    sheet1.write(R + 1, 2, total_time)
    sheet1.write(R + 1, 3, 1)
    print(f'[{sum(distances)}, {total_time}, {1}]')
    print('-----------------')

  def save():
    print('saved!')
    Excel.wb.save(OUTPUTS_PATH + 'result.xls')

class Plot:
  def plot(data, paths):
    fig, ax = plt.subplots()
    x = []
    y = []

    for node in data:
      x.append(node[1])
      y.append(node[2])

    ax.plot(x, y, 'o', label='Nodos')

    # Plot paths
    for p in paths:
      x = []
      y = []
      for node in paths[p]:
        x.append(data[node][1])
        y.append(data[node][2])
      ax.plot(x, y, '-', label=f'Camión {p+1}')

    plt.show()