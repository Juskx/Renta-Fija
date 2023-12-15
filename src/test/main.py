### ENTREGABLE NÚMERO 3 MAIN FILE###
from datetime import date
from datetime import datetime
from package.funcs.functions import get_ufs

last_uf_day_9 = 36607.69  
ipc_day_9 = 0.007  
date_last_uf = datetime(2023, 12, 9)  


valor_uf = get_ufs(date_last_uf, last_uf_day_9, ipc_day_9)
print(valor_uf["09-01-2024"])

### ENTREGABLE NÚMERO 4 MAIN ###
from package.fixedincome.classes import CLBond
from package.fixedincome.classes import FixedCoupon
from datetime import date

coupon1 = FixedCoupon(amortizacion=0.0, interes=0.01, saldo_residual=100.0,fecha_ini=date(2022,10,1),fecha_fin=date(2023,10,1))
coupon2 = FixedCoupon(amortizacion=100.0, interes=0.01, saldo_residual=0.0, fecha_ini=date(2023, 10, 1), fecha_fin=date(2024, 10, 1))

lista = [coupon1, coupon2]

bono = CLBond(fixed_coupons = lista)

# Imprimir el valor de la "tera"
print("Tera:", bono.tera)

# Imprimir el valor del bono para un notional, tasa y fecha dados
nocional = 1000000.0
tasa = 0.05
fecha = date(2023, 1, 1)

bond_value = bono.get_value(nocional, tasa,fecha)
print("Valor del bono:", bond_value)