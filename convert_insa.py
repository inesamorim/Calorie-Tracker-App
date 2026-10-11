"""Convert the INSA food composition table (xlsx) to the CSV the Nutri app imports.

Usage: python convert_insa.py insa_tca.xlsx foods_insa.csv
Source: Base de Dados da Composição de Alimentos, INSA v 7.1 - 2026.
Values are per 100 g of edible part (per 100 ml for alcoholic beverages).
"""
import re
import sys

import pandas as pd

SRC = sys.argv[1] if len(sys.argv) > 1 else "data/insa_tca.xlsx"
OUT = sys.argv[2] if len(sys.argv) > 2 else "data/foods_insa.csv"

# your column name  <-  INSA column (line breaks collapsed)
MAP = {
    "Alimento": "Nome do alimento",
    "Valor Calórico": "Energia [kcal]",
    "Gordura": "Lípidos [g]",
    "Gorduras Saturadas": "Ácidos gordos saturados [g]",
    "Gordura MonoSaturada": "Ácidos gordos monoinsaturados [g]",
    "Gorduras Poliinsaturadas": "Ácidos gordos polinsaturados [g]",
    "Hidratos de Carbono": "Hidratos de carbono [g]",
    "Açúcares": "Açúcares [g]",
    "Proteína": "Proteínas [g]",
    "Fibra": "Fibra [g]",
    "Colesterol": "Colesterol [mg]",
    "Potássio": "Potássio [mg]",
    "Água": "Água [g]",
    "Vitamina A": "Vitamina A [µg]",
    "Vitamina B1": "Tiamina [mg]",
    "Vitamina B2": "Riboflavina [mg]",
    "Vitamina B3": "Niacina [mg]",
    "Vitamina B6": "Vitamina B6 [mg]",
    "Vitamina B12": "Vitamina B12 [µg]",
    "Vitamina C": "Vitamina C [mg]",
    "Vitamina D": "Vitamina D [µg]",
    "Vitamina E": "α-tocoferol [mg]",
    "Cálcio": "Cálcio [mg]",
    "Ferro": "Ferro [mg]",
    "Magnésio": "Magnésio [mg]",
    "Fósforo": "Fósforo [mg]",
    "Selénio": "Selénio [µg]",
    "Zinco": "Zinco [mg]",
    # extra columns that INSA has and your old dataset did not
    "Sal": "Sal [g]",
    "Sódio": "Sódio [mg]",
    "Folatos": "Folatos [µg]",
    "Iodo": "Iodo [µg]",
    "Ácidos gordos trans": "Ácidos gordos trans [g]",
    "Álcool": "Álcool [g]",
}

df = pd.read_excel(SRC, sheet_name=0, header=1)
df.columns = [re.sub(r"\s+", " ", str(c)).strip() for c in df.columns]

out = pd.DataFrame({new: df[old] for new, old in MAP.items()})
out["Alimento"] = out["Alimento"].astype(str).str.strip()
for c in out.columns.drop("Alimento"):
    out[c] = pd.to_numeric(out[c], errors="coerce")

out = out.drop_duplicates("Alimento").sort_values("Alimento").reset_index(drop=True)
out.to_csv(OUT, index=False, encoding="utf-8")
print(f"{len(out)} foods, {out.shape[1]} columns -> {OUT}")
