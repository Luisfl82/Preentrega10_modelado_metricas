"""Verificación automática de la Preentrega 10.

Comprueba, uno por uno, los 5 criterios de la consigna y muestra OK / FALLA con la evidencia.
Uso (desde la carpeta del repositorio):   python verificar_entrega.py
No necesita instalar nada: usa solo la biblioteca estándar de Python.
"""
import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
resultados = []


def chequear(criterio, condicion, evidencia):
    resultados.append((criterio, bool(condicion), evidencia))


def leer_notebook():
    ruta = RAIZ / "modelado_metricas.ipynb"
    if not ruta.exists():
        return None
    return json.loads(ruta.read_text(encoding="utf-8"))


nb = leer_notebook()
codigo = md = ""
hay_error = True
con_salida = 0
if nb:
    celdas_codigo = [c for c in nb["cells"] if c["cell_type"] == "code"]
    codigo = "\n".join("".join(c["source"]) for c in celdas_codigo)
    md = "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown")
    hay_error = any(o.get("output_type") == "error" for c in celdas_codigo for o in c.get("outputs", []))
    con_salida = sum(1 for c in celdas_codigo if c.get("outputs"))

readme = (RAIZ / "README.md").read_text(encoding="utf-8") if (RAIZ / "README.md").exists() else ""
gitignore = (RAIZ / ".gitignore").read_text(encoding="utf-8") if (RAIZ / ".gitignore").exists() else ""

# Archivos y configuración
for archivo in ["modelado_metricas.ipynb", "README.md", "requirements.txt", ".gitignore",
                "data/clientes_churn.csv", "resultados/metricas.csv", "resultados/matriz_confusion.png"]:
    chequear(f"Existe {archivo}", (RAIZ / archivo).exists(), archivo)
chequear(".gitignore es de Python", "__pycache__" in gitignore and ".ipynb_checkpoints" in gitignore,
         "contiene __pycache__ y .ipynb_checkpoints")

# Criterio 1
chequear("1. Notebook con división Train/Test 80/20",
         "train_test_split" in codigo and ("test_size=0.20" in codigo or "test_size=0.2" in codigo),
         "train_test_split(test_size=0.20)")
chequear("1. Notebook sin errores y con resultados visibles", nb is not None and not hay_error and con_salida > 0,
         f"{con_salida} celdas de código con salida, sin errores")
chequear("1. Modelo Logistic Regression", "LogisticRegression" in codigo, "LogisticRegression")

# Criterio 2
for metrica in ["accuracy_score", "precision_score", "recall_score", "f1_score"]:
    chequear(f"2. Métrica {metrica}", metrica in codigo, metrica)
ruta_m = RAIZ / "resultados" / "metricas.csv"
filas = list(csv.reader(ruta_m.open(encoding="utf-8")))[1:] if ruta_m.exists() else []
chequear("2. resultados/metricas.csv con 4 métricas", len(filas) >= 4, f"{len(filas)} filas: " + ", ".join(f[0] for f in filas))

# Criterio 3
chequear("3. Matriz de confusión con mapa de calor", "confusion_matrix" in codigo and "heatmap" in codigo,
         "confusion_matrix + sns.heatmap")

# Criterio 4
chequear("4. README con descripción del problema", "Descripción del problema" in readme, "sección 1 del README")
chequear("4. README con instrucciones de ejecución", "Instrucciones de ejecución" in readme and "pip install -r requirements.txt" in readme,
         "sección 3 del README")
chequear("4. README sin textos pendientes de completar", "<tu-usuario>" not in readme and "<nombre-del-repositorio>" not in readme,
         "comandos de clonado completos")

# Criterio 5
chequear("5. Conclusión en Markdown sobre Recall y falsos negativos",
         "Recall" in md and "falso negativo" in md.lower() and "Churn" in md, "sección 7 del notebook")

ancho = max(len(c) for c, _, _ in resultados)
for criterio, ok, evidencia in resultados:
    print(f"[{'OK   ' if ok else 'FALLA'}] {criterio.ljust(ancho)}  ->  {evidencia}")
fallas = [r for r in resultados if not r[1]]
print(f"\nResultado: {len(resultados) - len(fallas)} de {len(resultados)} comprobaciones correctas.")
sys.exit(1 if fallas else 0)
