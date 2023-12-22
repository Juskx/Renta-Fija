from datetime import date
from typing import List
from scipy.optimize import minimize
import numpy as np

class FixedCoupon:
    def _init_(self, amortizacion: float, interes: float, saldo_residual: float, fecha_ini: date, fecha_fin: date):
        
        if not isinstance(amortizacion, float) or not (0 < amortizacion < 100):
            raise ValueError("Amortizacion debe estar en el rango de 0 a 100.")
        self.amortizacion = float(amortizacion)

        if not isinstance(interes, float) or not (0 < interes < 100):
            raise ValueError("Interes debe estar en el rango de 0 a 100.")
        self.interes = float(interes)

        if not isinstance(saldo_residual, float) or not (0 < saldo_residual < 100):
            raise ValueError("Saldo_residual debe estar en el rango de 0 a 100.")
        self.saldo_residual = float(saldo_residual)

        self.fecha_ini = fecha_ini
        self.fecha_fin = fecha_fin

        self.flow = self.amortizacion + self.interes

class CLBond:
    def __init__(self, fixed_coupons: List[dict], tera=None):
        self.fixed_coupons = fixed_coupons
        self.tera = tera if tera is not None else self.get_tera()
        self.fecha_emision = self.fixed_coupons[0].fecha_ini

    def get_fraccion_tiempo(self, fecha_ini: date, fecha_fin: date) -> float:
        return (fecha_fin - fecha_ini).days / 360
    
    def objective_function(self, tasa):
        return sum(cupon.flow / (1 + tasa) ** self.get_fraccion_tiempo(self.fecha_emision, cupon.fecha_fin) for cupon in self.fixed_coupons) - 1

    def get_tera(self):
        initial_guess = 0.05
        result = minimize(self.objective_function, initial_guess, method='BFGS')
        tera = result.x[0] 
        if tera != self.tera:
            self.tera = tera
        return tera
    
    def get_valor_par(self, date: date) -> float:
        c_actual = None

        for c in self.fixed_coupons:
            if c.fecha_ini <= date <= c.fecha_fin:
                c_actual = c
                break

        if c_actual is not None:
            dias_maturity = (c_actual.fecha_fin - date).days
            df = (1 / ((1 + self.tera) ** (dias_maturity / 360)))
            valor_par = round(c_actual.saldo_residual * df)
            return valor_par
        else:
            return None
        
    def get_pv(self, date: date, tera: float) -> float:
        pv = 0
        for cupon in self.fixed_coupons:
            if cupon.fecha_fin > date:
                days_to_maturity = (cupon.fecha_fin - date).days
                df = 1 / ((1 + tera) ** (days_to_maturity / 360))
                pv += cupon.flow * df
        return pv

    def get_dv01(self) -> float:
        vp = self.get_pv(self.fecha_emision, self.tera)
        vp_01 = self.get_pv(self.fecha_emision, self.tera + 0.0001)
        return vp_01 - vp
    
    def get_valor(self, date: date) ->float:
        precio = 100 * self.get_pv(date)/self.get_valor_par(date)   
        valor_par = self.get_valor_par(date)
        return precio * valor_par / 10_000
