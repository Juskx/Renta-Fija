class FixedIncome:
    def __init__(self, nocional, tasa_interes, plazo):
        self.nocional = nocional
        self.tasa_interes = tasa_interes
        self.plazo = plazo
        self.amortizacion = []

    def generar_tabla(self):
        saldo_pendiente = self.nocional

        for periodo in range(1, self.plazo + 1):
            if periodo < self.plazo:
               interes = saldo_pendiente * self.tasa_interes
               amortizacion = 0
            else:
                interes = saldo_pendiente * self.tasa_interes
                amortizacion = saldo_pendiente

            saldo_pendiente -= amortizacion
            # Almacenar los valores en la tabla de amortización
            self.amortizacion.append({
                'Periodo': periodo,
                'Interes': interes,
                'Amortizacion': amortizacion,
                'Saldo Residual': saldo_pendiente
            })
    def imprimir_tabla(self):
        # Imprimir la tabla de amortización
        print("Tabla Fixed Income")
        print("{:<10} {:<15} {:<15} {:<20}".format("Periodo", "Interes", "Amortizacion", "Saldo Residual"))
        for row in self.amortizacion:
            print("{:<10} {:<15.2f} {:<15.2f} {:<20.2f}".format(
                row['Periodo'], row['Interes'], row['Amortizacion'], row['Saldo Residual']))