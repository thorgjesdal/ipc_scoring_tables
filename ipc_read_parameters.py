import sys
from openpyxl import load_workbook

gender = { 'Men' : 'M', 'Women' : 'F'}
event_codes = { '100m' : '100', '200 m' : '200', '400 m': '400', '800 m' :'800', '1500 m' : '1500', '5000 m' : '5000', '10000 m':'10000', 'Shot Put' : 'SP', 'Discus' : 'DT', 'Javelin' : 'JT', 'High Jump' : 'HJ', 'Long Jump' : 'LJ' }

def ipc_read_parameters(f):
    wb = load_workbook(filename=f)
    ws = wb["Parameters"]
    params = {}
    for value in ws.iter_rows(min_row=2,min_col=1, max_col=6, values_only=True):
        print(value)

   

infile = sys.argv[1]
ipc_read_parameters(infile)
