# 📚 Proyecto Evaluación de Textos

Este repositorio contiene el trabajo de evaluación de textos considerando dimensiones de ortografía, vocabulario y cohesión textual.

## 🗂 Estructura de Carpetas

### 📊 `data`

- Contiene dos archivos:
  - `df_ECE` con más de 3000 evaluaciones del Examen de Comunicación Escrita (ECE).
  - Archivo .xlsx con los textos seleccionados por Nico y por mí para ser corregidos por expertos.

### 📓 `notebooks`

- **Primer enfoque:** Corrige cada texto haciendo tres llamadas a la API (una por cada dimensión: ortografía, vocabulario y cohesión).
- **Segundo enfoque:** Realiza correcciones por separado en cada subdimensión de las tres grandes dimensiones.
- Los resultados de ambos enfoques se guardan en la carpeta `resultados`.

### 📁 `resultados`

- Contiene los archivos JSON con los resultados de las correcciones realizadas por los notebooks.

## 📝 Última actualización

- 17 de septiembre de 2025
