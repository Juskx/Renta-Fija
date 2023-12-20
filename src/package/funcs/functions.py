from datetime import datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta
import locale

def get_ufs(date_last_uf, last_uf_day_9, ipc_day_9):

    if date_last_uf.day != 9:
        raise ValueError("Error: La función solo admite el día 9 del mes.")

    ultimo_dia_mes_actual = date_last_uf.replace(day=1) + timedelta(days=calendar.monthrange(date_last_uf.year, date_last_uf.month)[1])

    dias_en_mes = calendar.monthrange(date_last_uf.year, date_last_uf.month)[1]

    diferencia_dias = (ultimo_dia_mes_actual.replace(day=9) - date_last_uf.replace(day=9)).days

    uf_values = {}

    for i in range(0, diferencia_dias + 1):
        fecha_actual = date_last_uf + timedelta(days=i)
        valor_uf_objetivo = round(last_uf_day_9 * (1 + ipc_day_9) ** (i / dias_en_mes), 2)
        uf_values[fecha_actual.strftime('%d-%m-%Y')] = valor_uf_objetivo

    return uf_values