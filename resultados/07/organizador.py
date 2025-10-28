import json
import pandas as pd

archivos_json = {
    "Introducción": "a1_introduccion_ref.json",
    "Conclusión y cierre": "a1_conclusion_cierre_ref.json",
    "Progresión textual": "a1_progresion_textual_ref.json"
}

with pd.ExcelWriter("enfoque_07.xlsx", engine="openpyxl") as writer:
    for nombre_hoja, ruta_json in archivos_json.items():
        try:
            with open(ruta_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                try:
                    df = pd.DataFrame.from_dict(data, orient="index").reset_index()
                    df.rename(columns={"index": "criterio"}, inplace=True)
                except:
                    df = pd.DataFrame([data])
            else:
                df = pd.DataFrame([{"contenido": str(data)}])
            df.to_excel(writer, sheet_name=nombre_hoja, index=False)
        except Exception as e:
            print(f"Error en {ruta_json}: {e}")

print("\nArchivo 'enfoque_07.xlsx' generado correctamente.")
