### ENTREGABLE NÚMERO 3 MAIN FILE###
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_directory, "..")) ### OJO, SOLUCIONAR PROBLEMA

from datetime import date
from datetime import datetime
from package.funcs.functions import get_ufs

last_uf_day_9 = 36607.69  
ipc_day_9 = 0.007  
date_last_uf = datetime(2023, 12, 9)  


valor_uf = get_ufs(date_last_uf, last_uf_day_9, ipc_day_9)
print(valor_uf["09-01-2024"])
