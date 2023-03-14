#%%
from matplotlib.axes import Axes
import os
from dotenv import load_dotenv
from utils import Excel

import constructivo as Constructivo
import grasp as GRASP
# import ruido

load_dotenv()

DATA_PATH = os.getenv('DATA_PATH', './data')

def readTestFile(id):
  with open(f'{DATA_PATH}mtVRP{id}.txt') as f:
    lines = [line.rstrip() for line in f]
    lines = [line.split() for line in lines]
    lines = [[int(x) for x in line] for line in lines]
  return lines

nsol=100
alpha=0.5
K=5
r=5

for id in range(1,2):
  data = readTestFile(0)
  n, R, Q, Th = data[0]
  data = data[1:]

  Excel.start()

  #Constructivo.run(n, R, Q, Th, data)
  GRASP.run(n, R, Q, Th, alpha, data)

  Excel.save()