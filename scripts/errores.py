import pandas as pd
import json
from pathlib import Path

def procesar_errores(errores_dict):
    """Procesa un diccionario de errores y los convierte en texto con saltos de línea"""
    if not errores_dict:
        return ""
    
    errores_texto = []
    for key, value in errores_dict.items():
        if isinstance(value, list) and len(value) > 0:
            errores_texto.append(f'{key}: {value[0]}')
        elif isinstance(value, str):
            errores_texto.append(f'{key}: {value}')
    
    return '\n'.join(errores_texto)

def procesar_errores_con_tipo(errores_dict):
    """Procesa la estructura de errores que incluyen tipo de error (precisión, formal, cohesión)"""
    if not errores_dict:
        return ""
    
    errores_texto = []
    for key, value in errores_dict.items():
        if isinstance(value, list) and len(value) >= 2:
            # value[0] es el error, value[1] es el tipo de error
            errores_texto.append(f'{key}: {value[0]} [{value[1]}]')
        elif isinstance(value, list) and len(value) == 1:
            errores_texto.append(f'{key}: {value[0]}')
    
    return '\n'.join(errores_texto)

def procesar_errores_amplitud(errores_dict):
    """Procesa la estructura especial de errores de amplitud"""
    if not errores_dict:
        return ""
    
    errores_texto = []
    for parrafo, palabras in errores_dict.items():
        if isinstance(palabras, dict):
            for palabra, frecuencias in palabras.items():
                if isinstance(frecuencias, list) and len(frecuencias) > 0:
                    errores_texto.append(f'{parrafo} - {palabra}: {frecuencias[0]}')
    
    return '\n'.join(errores_texto)

def cargar_y_procesar_json(ruta_json, tipo_errores, id_minimo=10):
    """Carga un JSON y extrae los errores del tipo especificado, filtrando por id_texto >= id_minimo"""
    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        resultados = {}
        for item in datos:
            id_texto = item['id_texto']
            # Filtrar solo textos con id_texto >= 10
            if id_texto >= id_minimo:
                # Para amplitud, la estructura es diferente
                if tipo_errores == "errores_vocabulario_amplitud":
                    if tipo_errores in item:
                        errores_texto = procesar_errores_amplitud(item[tipo_errores])
                        resultados[id_texto] = errores_texto
                    else:
                        resultados[id_texto] = ""
                # Para precisión, formal y cohesión, usar función con tipo de error
                elif tipo_errores in ["errores_precision", "errores_vocabulario_formal", 
                                    "errores_cohesion_concordancia", "errores_cohesion_conexion",
                                    "errores_cohesion_referencia"]:
                    if 'resultado' in item and tipo_errores in item['resultado']:
                        errores_texto = procesar_errores_con_tipo(item['resultado'][tipo_errores])
                        resultados[id_texto] = errores_texto
                    else:
                        resultados[id_texto] = ""
                else:
                    # Para los otros tipos (acentuales, literal, puntual)
                    if 'resultado' in item and tipo_errores in item['resultado']:
                        errores_texto = procesar_errores(item['resultado'][tipo_errores])
                        resultados[id_texto] = errores_texto
                    else:
                        resultados[id_texto] = ""
        
        return resultados
    
    except Exception as e:
        print(f"❌ Error procesando {ruta_json.name}: {e}")
        return {}
    
def main():
    # Configuración de rutas
    script_dir = Path(__file__).parent  # Carpeta scripts
    resultados_dir = script_dir.parent / "resultados" / "02"
    output_dir = script_dir.parent / "output_combinado"
    output_dir.mkdir(exist_ok=True)

    # Rutas de los archivos JSON
    ruta_acentuales = resultados_dir / "ort_acentual.json" 
    ruta_ortografia_literal = resultados_dir / "ort_literal.json"
    ruta_ort_puntual = resultados_dir / "ort_puntual.json"
    ruta_voc_amplitud = resultados_dir / "voc_amplitud.json"
    ruta_voc_precision = resultados_dir / "voc_precision.json"
    ruta_voc_formal = resultados_dir / "voc_formal.json"
    ruta_coh_concordancia = resultados_dir / "coh_concordancia.json"
    ruta_coh_conexion = resultados_dir / "coh_conexion.json"  # Nuevo archivo
    ruta_coh_referencias = resultados_dir / "coh_referencias.json"  # Nuevo archivo

    # ID mínimo a considerar
    ID_MINIMO = 10

    print(f"🔍 Filtrando textos con id_texto >= {ID_MINIMO}")

    # Verificar que existen los archivos
    archivos_existen = True
    for ruta, nombre in [
        (ruta_acentuales, "ort_acentual.json"),
        (ruta_ortografia_literal, "ort_literal.json"), 
        (ruta_ort_puntual, "ort_puntual.json"),
        (ruta_voc_amplitud, "voc_amplitud.json"),
        (ruta_voc_precision, "voc_precision.json"),
        (ruta_voc_formal, "voc_formal.json"),
        (ruta_coh_concordancia, "coh_concordancia.json"),
        (ruta_coh_conexion, "coh_conexion.json"),  # Nuevo archivo
        (ruta_coh_referencias, "coh_referencias.json")  # Nuevo archivo
    ]:
        if not ruta.exists():
            print(f"❌ No se encontró: {ruta}")
            archivos_existen = False
        else:
            print(f"✅ Encontrado: {nombre}")

    # Procesar archivos si todos existen
    if archivos_existen:
        print(f"\n🔄 Procesando archivos (id_texto >= {ID_MINIMO})...")
        
        # Cargar errores acentuales
        acentuales_dict = cargar_y_procesar_json(ruta_acentuales, "errores_acentuales", ID_MINIMO)
        print(f"📊 Errores acentuales: {len(acentuales_dict)} textos procesados")
        
        # Cargar errores de ortografía literal
        ortografia_dict = cargar_y_procesar_json(ruta_ortografia_literal, "errores_ortografia_literal", ID_MINIMO)
        print(f"📊 Errores ortografía literal: {len(ortografia_dict)} textos procesados")

        # Cargar errores de ortografía puntual
        ort_puntual_dict = cargar_y_procesar_json(ruta_ort_puntual, "errores_ortografia_puntual", ID_MINIMO)
        print(f"📊 Errores ortografía puntual: {len(ort_puntual_dict)} textos procesados")
        
        # Cargar errores de vocabulario amplitud
        voc_amplitud_dict = cargar_y_procesar_json(ruta_voc_amplitud, "errores_vocabulario_amplitud", ID_MINIMO)
        print(f"📊 Errores vocabulario amplitud: {len(voc_amplitud_dict)} textos procesados")
        
        # Cargar errores de vocabulario precisión
        voc_precision_dict = cargar_y_procesar_json(ruta_voc_precision, "errores_precision", ID_MINIMO)
        print(f"📊 Errores vocabulario precisión: {len(voc_precision_dict)} textos procesados")
        
        # Cargar errores de vocabulario formal
        voc_formal_dict = cargar_y_procesar_json(ruta_voc_formal, "errores_vocabulario_formal", ID_MINIMO)
        print(f"📊 Errores vocabulario formal: {len(voc_formal_dict)} textos procesados")
        
        # Cargar errores de cohesión y concordancia
        coh_concordancia_dict = cargar_y_procesar_json(ruta_coh_concordancia, "errores_cohesion_concordancia", ID_MINIMO)
        print(f"📊 Errores cohesión y concordancia: {len(coh_concordancia_dict)} textos procesados")
        
        # Cargar errores de cohesión y conexión (NUEVO)
        coh_conexion_dict = cargar_y_procesar_json(ruta_coh_conexion, "errores_cohesion_conexion", ID_MINIMO)
        print(f"📊 Errores cohesión y conexión: {len(coh_conexion_dict)} textos procesados")
        
        # Cargar errores de cohesión y referencias (NUEVO)
        coh_referencias_dict = cargar_y_procesar_json(ruta_coh_referencias, "errores_cohesion_referencia", ID_MINIMO)
        print(f"📊 Errores cohesión y referencias: {len(coh_referencias_dict)} textos procesados")
        
        # Combinar en un DataFrame
        filas = []
        
        # Usar todos los IDs encontrados (a partir de id_texto >= 10)
        todos_ids = (set(acentuales_dict.keys()) | set(ortografia_dict.keys()) | 
                    set(ort_puntual_dict.keys()) | set(voc_amplitud_dict.keys()) | 
                    set(voc_precision_dict.keys()) | set(voc_formal_dict.keys()) | 
                    set(coh_concordancia_dict.keys()) | set(coh_conexion_dict.keys()) | 
                    set(coh_referencias_dict.keys()))
        
        # Ordenar IDs y asegurarse de que sean >= 10
        ids_filtrados = sorted([id_texto for id_texto in todos_ids if id_texto >= ID_MINIMO])
        
        print(f"📊 IDs únicos encontrados: {ids_filtrados}")
        
        for id_texto in ids_filtrados:
            fila = {
                'id_texto': id_texto,
                'errores_ortografia_literal': ortografia_dict.get(id_texto, ""),
                'errores_acentuales': acentuales_dict.get(id_texto, ""),
                'errores_ortografia_puntual': ort_puntual_dict.get(id_texto, ""),
                'errores_vocabulario_amplitud': voc_amplitud_dict.get(id_texto, ""),
                'errores_vocabulario_precision': voc_precision_dict.get(id_texto, ""),
                'errores_vocabulario_formal': voc_formal_dict.get(id_texto, ""),
                'errores_cohesion_concordancia': coh_concordancia_dict.get(id_texto, ""),
                'errores_cohesion_conexion': coh_conexion_dict.get(id_texto, ""), 
                'errores_cohesion_referencia': coh_referencias_dict.get(id_texto, "") 
            }
            filas.append(fila)
        
        # Crear DataFrame
        df = pd.DataFrame(filas)
        
        # Guardar en Excel con formato
        nombre_salida = "errores_combinados.xlsx"
        ruta_excel = output_dir / nombre_salida
        
        try:
            with pd.ExcelWriter(ruta_excel, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Errores', index=False)
                
                # Formato para saltos de línea
                workbook = writer.book
                worksheet = writer.sheets['Errores']
                wrap_format = workbook.add_format({'text_wrap': True})
                
                # Aplicar formato a las columnas de errores (ahora son 10 columnas)
                worksheet.set_column('B:K', 50, wrap_format)  # Columnas B a K
                
            print(f"💾 Excel guardado: {ruta_excel}")
        except ModuleNotFoundError:
            print("⚠️  xlsxwriter no está instalado, guardando solo CSV")
        
        # Guardar en CSV
        ruta_csv = output_dir / "errores_combinados.csv"
        df.to_csv(ruta_csv, index=False, encoding='utf-8')
        
        print(f"\n✅ Resultados combinados:")
        print(f"   📊 Total de textos (id >= {ID_MINIMO}): {len(df)}")
        print(f"   📊 Columnas: {list(df.columns)}")
        print(f"   💾 CSV guardado: {ruta_csv}")
        
        # Mostrar preview con más detalle
        print(f"\n📋 Vista previa (primeras filas):")
        for i, row in df.head().iterrows():
            print(f"\nID: {row['id_texto']}")
            print(f"Acentuales: {len(row['errores_acentuales'])} chars")
            print(f"Literal: {len(row['errores_ortografia_literal'])} chars") 
            print(f"Puntual: {len(row['errores_ortografia_puntual'])} chars")
            print(f"Amplitud: {len(row['errores_vocabulario_amplitud'])} chars")
            print(f"Precisión: {len(row['errores_vocabulario_precision'])} chars")
            print(f"Formal: {len(row['errores_vocabulario_formal'])} chars")
            print(f"Cohesión Concordancia: {len(row['errores_cohesion_concordancia'])} chars")
            print(f"Cohesión Conexión: {len(row['errores_cohesion_conexion'])} chars")
            print(f"Cohesión Referencia: {len(row['errores_cohesion_referencia'])} chars")
            if row['errores_cohesion_conexion']:
                print(f"  Ejemplo conexión: {row['errores_cohesion_conexion'][:100]}...")
            if row['errores_cohesion_referencia']:
                print(f"  Ejemplo referencia: {row['errores_cohesion_referencia'][:100]}...")

    else:
        print("\n❌ No se pueden procesar los archivos. Verifica los nombres.")
        


if __name__ == "__main__":
    main()
