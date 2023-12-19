from datetime import date
from typing import List
from scipy.optimize import newton
import numpy as np

#DV01 es VP(r+0,01%)-VP(r) o bien -VP*duracion/10000

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

        self.flow = self.amortizacion + self.interes

    def _validate_value(self, name: str, value: float):
        if not isinstance (value, float) or (0 < value < 100):
            raise ValueError(f"{name.capitalize()} debe estar en el rango de 0 a 100.")



class CLBond:
    def __init__(self, fixed_coupons: List[dict], tera=None):
        self.fixed_coupons = fixed_coupons
        self.tera = tera if tera is not None else self.get_tera()
        self.fecha_emision = self.fixed_coupons[0].fecha_ini

    def get_tera(self):
        initial_guess = 0.05
        tera = newton(
            lambda tasa: sum(
                (cupon.flow) / ((1 + tasa) ** self.get_fraccion_tiempo(self.fecha_emision, cupon.fecha_fin)) for cupon in self.fixed_coupons) - 1,
            x0=initial_guess,
        )
        return tera

    def set_tera(self): 
        nuevo_tera = self.get_tera()
        if nuevo_tera != self.tera:
            self.tera = nuevo_tera

    def get_value(self, notional: float, tasa: float, fecha: date) -> float:
        return notional * sum((cupon.amortizacion + cupon.interes) / ((1 + tasa) ** ((cupon.fecha_fin - fecha).days / 360)) for cupon in self.fixed_coupons)
    
    def get_dv01(self, notional: float) -> float:
        return notional * sum((cupon['amortizacion'] + cupon['interes']) * ((cupon['fecha_fin'] - cupon['fecha_ini']).days / 360) / ((1 + self.tera) ** ((cupon['fecha_fin'] - cupon['fecha_ini']).days / 360 + 1)) for cupon in self.fixed_coupons)

    def get_fraccion_tiempo(self, fecha_ini: date, fecha_fin: date) -> float:
        return (fecha_fin - fecha_ini).days / 360
    
    def get_valor_par(self, date: date) -> float:
        current_coupon = self.get_cupon_actual(date)
        days_to_maturity = (current_coupon.fecha_fin - date).days
        discount_factor = 1 / ((1 + self.tera) ** (days_to_maturity / 360))
        par_value = current_coupon.saldo_residual * discount_factor
        return round(par_value)
    
    def get_cupon_actual(self, date: date) -> FixedCoupon:
        for c in self.fixed_coupons:
            if c.fecha_ini <= date and c.fecha_fin > date:
                return c
        return None
    
    def get_pv(self, date: date, tera: float) -> float:
        present_value = 0
        for cupon in self.fixed_coupons:
            if cupon.fecha_fin > date:
                days_to_maturity = (cupon.fecha_fin - date).days
                discount_factor = 1 / ((1 + tera) ** (days_to_maturity / 360))
                present_value += cupon.flow * discount_factor
        return present_value
    
    def get_price(self, date: date) -> float:
        vp = self.get_pv(date)
        valor_par = self.get_valor_par(date)
        precio = 100.0 * vp/valor_par
        return precio
    
    def get_dv01(self) -> float:

        vp_r = self.get_pv(self.fecha_emision, self.tera)

        r_01 = self.tera + 0.0001 
        vp_r_plus_01 = self.get_pv(self.fecha_emision,r_01)

        dv01 = (vp_r_plus_01 - vp_r)

        return dv01
    
    def get_valor(self, date: date) ->float:
        precio = self.get_price(date)
        valor_par = self.get_valor_par(date)
        return precio * valor_par / 10_000

        
        