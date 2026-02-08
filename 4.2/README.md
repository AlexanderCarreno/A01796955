# Práctica 4.2 - Pruebas de software y aseguramiento de la calidad

Resumen del proyecto

Este repositorio contiene tres ejercicios (P1, P2 y P3) que implementan pequeñas utilidades de análisis y conversión de datos:

- P1: `computeStatistics.py` — calcula estadísticas descriptivas (media, mediana, moda, varianza, desviación estándar) a partir de un archivo de datos numéricos.
- P2: `convertNumbers.py` — convierte números decimales a binario y hexadecimal (incluye soporte para representaciones en complemento a dos para números negativos, siguiendo la lógica de Excel).
- P3: `wordCount.py` — cuenta palabras y frecuencias en archivos de texto.

Resultados y evidencia

- Todos los resultados generados para los archivos proporcionados por el maestro se encuentran en la carpeta `result` y están nombrados conforme a la hoja de requerimientos (cada resultado corresponde al archivo de entrada asociado).
- Dentro de la misma carpeta `result` hay una foto con la evidencia de la calificación de `pylint`.
- También en `result` se incluye el *log* de la ejecución de todas las pruebas (ejecución secuencial de los casos de prueba).

Estructura relevante

- `4.2/P1/source/computeStatistics.py`  — código fuente P1
- `4.2/P2/source/convertNumbers.py`    — código fuente P2
- `4.2/P3/source/wordCount.py`         — código fuente P3
- `4.2/result/`                        — carpeta con resultados, evidencia de pylint y logs

Cómo ejecutar (ejemplos)

Desde la raíz del proyecto, en Windows (cmd o PowerShell):

```bash
# Ejecutar P1 con un archivo de datos
python ./4.2/P1/source/computeStatistics.py ./4.2/P1/tests/TC1.txt

# Ejecutar P2 con un archivo de datos
python ./4.2/P2/source/convertNumbers.py ./4.2/P2/tests/TC1.txt

# Ejecutar P3 con un archivo de texto
python ./4.2/P3/source/wordCount.py ./4.2/P3/tests/TC1.txt
```

Nota: Tambien se a creado un archivo bat para cada P1 para ejecutar todas las pruebas al mismo tiempo, como ejemplo del batch que se utilizo se deja abajo un ejemplo, en caso de que se desee usarlo cambiar las carpetas como corresponda. Este batch solo funciona sobre systemas operativos Windows

```bash
@echo off
REM Script to run P1 computeStatistics.py with all test files

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo Running computeStatistics.py with all test cases...
echo.

for %%F in (.\4.2\P1\tests\TC*.txt) do (
    echo ========================================
    echo Running with: %%~nxF
    echo ========================================
    python .\4.2\P1\source\computeStatistics.py "%%F"
    echo.
)

echo All tests completed!
pause

```

Requisitos

- Python 3.8+ (se usó codificación UTF-8 para archivos de entrada/salida)