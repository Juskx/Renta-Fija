import datetime
from dateutil.relativedelta import relativedelta
import calendar
from datetime import timedelta

def get_ufs(last_uf_known_date, last_uf_value, new_ipc):
    if last_uf_known_date.day != 9:
        print("Fecha incorrecta, ingresar fecha con dia 9")
        return None 
    else:
        d=calendar.monthrange(last_uf_known_date.year, last_uf_known_date.month)[1]
        next_month_date = last_uf_known_date + relativedelta(months=1, day=9)
        days_until= (next_month_date - last_uf_known_date).days
        
        initial_date=last_uf_known_date.strftime('%Y-%m-%d')
        result_dict={initial_date : last_uf_value}
        for i in range(1,days_until+1):
            last_uf_known_date = last_uf_known_date + timedelta(days=1)
            uf_value = round( ( last_uf_value * (1+new_ipc) ** (i/d) ),2)
            result_dict[last_uf_known_date.strftime('%Y-%m-%d')] = uf_value
        return result_dict
