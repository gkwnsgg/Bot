import openpyxl
from openpyxl import load_workbook

wb = load_workbook(filename='승리의 여신 _ NIKKE - 큐브.xlsx')
ws1 = wb['1버스트']

for sht in ws1
    ws = wb[sht]

#print(ws_list)

# for row in ws1.rows:
#     row_values = [cell.value for cell in row]:=

#     print(row_values)