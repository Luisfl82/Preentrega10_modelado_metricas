# Preentrega 10 - Modelado y evaluación de clasificación (Churn)

## Problema
Una empresa de telecomunicaciones quiere **predecir qué clientes se van a dar de baja (churn)** para actuar a tiempo. Se entrena una **Regresión Logística** (clasificación binaria) y se evalúa con Accuracy, Precision, Recall, F1 y matriz de confusión.

## Contenido
```
modelado_metricas.ipynb   -> notebook principal (carga, split 80/20, modelo, métricas, matriz de confusión, conclusión)
generar_dataset.py        -> crea data/clientes_churn.csv (dataset simulado)
data/clientes_churn.csv   -> datos
requirements.txt
```

## Cómo ejecutarlo
1. Instalar librerías: `pip install -r requirements.txt`
2. (Opcional) regenerar los datos: `python generar_dataset.py`
3. Abrir el notebook: `jupyter notebook modelado_metricas.ipynb`
4. En el menú: **Kernel → Restart & Run All** (ejecuta todas las celdas).

## Resumen de resultados (conjunto de prueba, 20%)
| Métrica | Valor |
|---|---|
| Accuracy | 0.730 |
| Precision | 0.587 |
| **Recall** | **0.745** |
| F1-Score | 0.657 |

Matriz de confusión: VN=283, FP=109, FN=53, VP=155.

**Conclusión:** en Churn la métrica clave es el **Recall**, porque un falso negativo (cliente que se va sin ser detectado) es mucho más caro que un falso positivo (una oferta de más). El detalle está en la última sección del notebook.

## Datos
Dataset simulado con la estructura de un caso Telco Churn clásico (antigüedad, cargos, contrato, internet, método de pago y soporte). Generado con semilla fija en `generar_dataset.py`.
