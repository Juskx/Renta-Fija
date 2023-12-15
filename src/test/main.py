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

# Crear instancias de FixedCoupon con fechas de inicio y fin
coupon1 = FixedCoupon(amortizacion=0.0, interes=0.01, saldo_residual=100.0,fecha_ini=date(2022,10,1),fecha_fin=date(2023,10,1))
coupon2 = FixedCoupon(amortizacion=100.0, interes=0.01, saldo_residual=0.0, fecha_ini=date(2023, 10, 1), fecha_fin=date(2024, 10, 1))

# Crear lista de cupones fijos
fixed_coupons_list = [coupon1, coupon2]

# Crear instancia de CLBond
cl_bond = CLBond(fixed_coupons = fixed_coupons_list)

# Imprimir el valor de la "tera"
print("Tera:", cl_bond.tera)

# Imprimir el valor del bono para un notional, tasa y fecha dados
notional_value = 1000000.0
interest_rate = 0.05
valuation_date = date(2023, 1, 1)

bond_value = cl_bond.get_value(notional_value, interest_rate,valuation_date)
print("Valor del bono:", bond_value)