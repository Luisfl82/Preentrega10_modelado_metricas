"""Genera data/clientes_churn.csv (dataset simulado tipo 'Telco Churn')."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(10)
n = 3000
antig = rng.integers(1, 73, n)
contrato = rng.choice(["Mensual", "Anual", "Bianual"], n, p=[0.55, 0.25, 0.20])
internet = rng.choice(["DSL", "Fibra", "Ninguno"], n, p=[0.35, 0.45, 0.20])
pago = rng.choice(["Tarjeta", "Transferencia", "Cheque", "Debito"], n)
soporte = rng.choice(["Si", "No"], n, p=[0.4, 0.6])
cargo = (30 + 25 * (internet == "Fibra") + 12 * (internet == "DSL") + rng.normal(0, 8, n)).round(2)
total = (cargo * antig + rng.normal(0, 40, n)).clip(20).round(2)
logit = (-0.6 - 0.045 * antig + 0.018 * cargo + 1.3 * (contrato == "Mensual")
         - 0.8 * (contrato == "Bianual") + 0.5 * (pago == "Cheque") - 0.5 * (soporte == "Si"))
churn = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
df = pd.DataFrame({"antiguedad_meses": antig, "cargo_mensual": cargo, "cargos_totales": total,
                   "tipo_contrato": contrato, "servicio_internet": internet, "metodo_pago": pago,
                   "soporte_tecnico": soporte, "churn": churn})
df.to_csv("data/clientes_churn.csv", index=False)
print("Creado data/clientes_churn.csv", df.shape, "| tasa de churn:", round(churn.mean(), 3))
