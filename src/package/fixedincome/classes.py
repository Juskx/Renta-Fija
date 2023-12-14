from datetime import date
from typing import List
from scipy.optimize import newton

class FixedCoupon:
    def __init__(self, amortizacion: float, interes: float, saldo_residual: float, fecha_ini: date, fecha_fin: date):
        self._validate_value("amortizacion", amortizacion)
        self._validate_value("interes", interes)
        self._validate_value("saldo_residual", saldo_residual)

        self.amortizacion = float(amortizacion)
        self.interes = float(interes)
        self.saldo_residual = float(saldo_residual)
        self.fecha_ini = fecha_ini
        self.fecha_fin = fecha_fin
        self.cupon = self.get_cupon()

    def _validate_value(self, name: str, value: float):
        if not isinstance(value, float) or not 0 <= value <= 100:
            raise ValueError(f"{name.capitalize()} debe ser un número entre 0 y 100.")

    def get_cupon(self):
        return self.amortizacion + self.interes

    def get_amortization_and_interest(self):
        return self.amortizacion, self.interes

    def get_fecha_ini(self):
        return self.fecha_ini

    def get_fecha_fin(self):
        return self.fecha_fin

class CLBond:
    def __init__(self, fixed_coupons: List[dict], tera=None):
        self.fixed_coupons = fixed_coupons
        self.tera = tera if tera is not None else self.get_tera()

    def get_tera(self):
        initial_guess = sum(cupon['amortizacion'] + cupon['interes'] for cupon in self.fixed_coupons) / len(self.fixed_coupons)
        tera = newton(lambda tasa: sum((cupon['amortizacion'] + cupon['interes']) / ((1 + tasa) ** self.get_fraccion_tiempo(cupon['fecha_ini'], cupon['fecha_fin'])) for cupon in self.fixed_coupons) - 1, x0=initial_guess)
        return tera

    def set_tera(self): 
        nuevo_tera = self.get_tera()
        if nuevo_tera != self.tera:
            self.tera = nuevo_tera

    def get_value(self, notional: float, tasa: float, fecha: date) -> float:
        return notional * sum((cupon['amortizacion'] + cupon['interes']) / ((1 + tasa) ** ((cupon['fecha_fin'] - fecha).days / 360)) for cupon in self.fixed_coupons)

    def get_dv01(self, notional: float) -> float:
        return notional * sum((cupon['amortizacion'] + cupon['interes']) * ((cupon['fecha_fin'] - cupon['fecha_ini']).days / 360) / ((1 + self.tera) ** ((cupon['fecha_fin'] - cupon['fecha_ini']).days / 360 + 1)) for cupon in self.fixed_coupons)

    def get_wf(self, rate: float, fecha_ini: date, fecha_fin: date) -> float:
        time_fraction = (fecha_fin - fecha_ini).days / 360
        return (1 + rate) ** time_fraction
    
    def get_wf_compounded(self, rate_value: float, fecha_ini: date, fecha_fin: date) -> float:
        time_fraction = (fecha_fin - fecha_ini).days / 360
        return (1 + rate_value) ** time_fraction

    def get_fraccion_tiempo(self, fecha_ini: date, fecha_fin: date) -> float:
        return (fecha_fin - fecha_ini).days / 360

    def get_npv_derivative(self, rate, cupon):
        return -cupon['amortizacion'] * ((cupon['fecha_fin'] - cupon['fecha_ini']).days / 360) * (1 + rate) ** (((cupon['fecha_fin'] - cupon['fecha_ini']).days / 360) - 1)

