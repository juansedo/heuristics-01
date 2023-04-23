from xlwt import Workbook
import matplotlib.pyplot as plt
import os
import itertools
import math
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = os.getenv('DATA_PATH', './data/')
OUTPUTS_PATH = os.getenv('OUTPUTS_PATH', './outputs/')

def getDistance(n1, n2):
  x1, y1 = n1
  x2, y2 = n2
  return round(math.sqrt((x2-x1)**2 + (y2-y1)**2), 2)

class TestFile:
  def getById(id):
    with open(f'{DATA_PATH}mtVRP{id}.txt') as f:
      lines = [line.rstrip() for line in f]
      lines = [line.split() for line in lines]
      lines = [[int(x) for x in line] for line in lines]
    return lines

class ExcelBook:
  def __init__(self, title):
    self.title = title
    self.wb = Workbook()

  def get_sheet_by_name(self, name):
    try:
      for idx in itertools.count():
        sheet = self.wb.get_sheet(idx)
        if sheet.name == name:
          return sheet
    except IndexError:
      return self.wb.add_sheet(name)

  def add_sheet(self, index, problem_result, Th):
    sheet1 = self.get_sheet_by_name('mtVRP' + str(index))
    paths, distances, total_time = problem_result
    R = len(paths)
    for i in range(0, R):
      size = len(paths[i])
      for j in range(size):
        sheet1.write(i, j, paths[i][j])
      sheet1.write(i, size, '{:.2f}'.format(distances[i]))
      sheet1.write(i, size + 1, 1 if distances[i] > Th else 0)

    sheet1.write(R, 0, '{:.2f}'.format(sum(distances)))
    sheet1.write(R, 1, '{:.2f}'.format(total_time))
    sheet1.write(R, 2, 1)

  def save(self):
    if not os.path.exists(OUTPUTS_PATH):
      os.makedirs(OUTPUTS_PATH)
    self.wb.save(OUTPUTS_PATH + self.title)
    print(f'{self.title} saved!')

class Plot:
  def plotDistances(labels, distances):
    fig, ax = plt.subplots()
    ax.barh(labels, distances)
    ax.invert_yaxis()
    for i in ax.patches:
      plt.text(i.get_width() + 0.2, i.get_y() + 0.5, str(round((i.get_width()), 2)), fontsize = 10, fontweight = 'bold', color = 'grey')
    plt.show()

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