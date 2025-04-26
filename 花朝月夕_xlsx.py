import openpyxl
from openpyxl import load_workbook

wb = load_workbook(filename='승리의 여신 _ NIKKE - 큐브.xlsx',)
ws1 = wb['1버스트']

cub1 = ws1["B1"].value

print('Range("B1"):', cub1)