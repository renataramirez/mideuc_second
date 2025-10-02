import os
import json
import pandas as pd

# Carpeta donde están los JSON
folder = os.path.join("resultados", "06")

# Archivos JSON reales
json_estructura = os.path.join(folder, "a1_estructura.json")
json_intro = os.path.join(folder, "a1_introduccion.json")
json_conc = os.path.join(folder, "a1_conclusion_cierre.json")
json_prog = os.path.join(folder, "a1_progresion_textual.json")

# Cargar JSON
with open(json_estructura, "r", encoding="utf-8") as f:
    estructura = json.load(f)

with open(json_intro, "r", encoding="utf-8") as f:
    intro = json.load(f)

with open(json_conc, "r", encoding="utf-8") as f:
    conc = json.load(f)

with open(json_prog, "r", encoding="utf-8") as f:
    prog = json.load(f)

# Crear lista de filas para DataFrame
filas = []

for item in estructura:
    id_texto = item["id_texto"]

    # Niveles de JSON estructura
    intro_estructura = item["resultado"].get("introduccion", {}).get("nivel", None)
    conc_estructura = item["resultado"].get("conclusion_cierre", {}).get("nivel", None)
    prog_estructura = item["resultado"].get("progresion_textual", {}).get("nivel", None)

    # Niveles de JSON individuales
    intro_ind = next((x["resultado"].get("introduccion", {}).get("nivel", None)
                      for x in intro if x["id_texto"] == id_texto), None)

    conc_ind = next((x["resultado"].get("conclusion_cierre", {}).get("nivel", None)
                     for x in conc if x["id_texto"] == id_texto), None)

    prog_ind = next((x["resultado"].get("progresion_textual", {}).get("nivel", None)
                     for x in prog if x["id_texto"] == id_texto), None)

    filas.append({
        "id": id_texto,
        "introEstructura": intro_estructura,
        "introIndividual": intro_ind,
        "concEstructura": conc_estructura,
        "concIndividual": conc_ind,
        "progEstructura": prog_estructura,
        "progIndividual": prog_ind
    })

# Crear DataFrame
df = pd.DataFrame(filas)

# Guardar a Excel
output_path = os.path.join(folder, "comparacion_puntajes.xlsx")
df.to_excel(output_path, index=False)

print(f"Excel generado en: {output_path}")
print("Comparación de puntajes completada.")