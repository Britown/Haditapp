# Reglas Consolidadas de Extracción de Cartolas (BICE y Tarjetas)

Este documento consolida los aprendizajes y reglas de negocio descubiertas empíricamente al procesar cartolas del Banco BICE (PDF) y Tarjetas de Crédito (Excel).

## 1. Regla del Monto (El problema `vals[0]` vs `vals[-1]`)
- **Problema histórico:** Se utilizaba `vals[0]` o `vals[-1]` de forma rígida. Esto provocaba que se tomaran números de referencia (al inicio) o saldos contables (al final).
- **Solución implementada:** Se analiza el final del string.
  - Si los últimos **dos tokens** de la línea son montos válidos (ej. `19.900,00 1.433.078,00`), el último es el **Saldo Contable** y el penúltimo es el **Monto del Cargo**.
  - Si solo el último token es un monto, entonces ese es el **Monto del Cargo**.
  - Los números de referencia (al inicio) se ignoran automáticamente porque la lectura se hace desde el final de la línea hacia atrás.

## 2. Regla de Cuotas y Fechas (Falsos Dólares)
- **Problema histórico:** Frases como `1 de 1` o `01/12` eran parseadas como un cargo de `$1`. Si el sistema veía que el monto era `< 200`, asumía que era un cargo internacional en dólares y lo multiplicaba por el valor del dólar (causando el bug de "Amazon Prime $950").
- **Solución implementada:** Se eliminan sistemáticamente mediante Regex las frases tipo `\d+ de \d+` y `\d+/\d+` antes de evaluar los montos, previniendo que los números de cuotas contaminen el valor real.

## 3. Regla del Dólar (Fallback y Caching)
- **Problema histórico:** La API de `mindicador.cl` presentaba caídas (Timeouts), lo que congelaba la aplicación por varios minutos, y ralentizaba el proceso por cada fila internacional.
- **Solución implementada:** 
  1. Se implementó un cache en memoria (`_DOLAR_CACHE`) para solo consultar la API una vez por mes/día.
  2. Se configuró un `timeout=2.0`. Si la API falla, se utiliza silenciosamente el "Dólar de Emergencia" (ingresado por el usuario en Ajustes Dinámicos), evitando que la app se cuelgue.

## 4. Deduplicación de Archivos Solapados
- **Problema histórico:** Subir una cartola mensual junto con un estado de cuenta que abarcaba días similares (ej. `CC junio` y `Cartola_29_05_30_06`) causaba que gastos sumativos (como los pagos a "Andy") se duplicaran (ej. $107.000 -> $214.000).
- **Solución implementada:** Se implementó un set `processed_lines` que bloquea el procesamiento de cualquier línea de texto (folio, fecha, glosa, monto) que ya haya sido leída exactamente igual en otro archivo durante la misma sesión.

## 5. Casos de Borde de Categorías
- **Colegio (CSFJ):** El colegio agrupa los cobros de Colegiatura y Otros Educacionales en un solo monto total (ej. $597.626). El sistema usa el valor UF para calcular la colegiatura base y envía la diferencia matemáticamente exacta a "Extras/Materiales". Además, se ajustó el nombre del colegio a `COLEGIO FCO.JAVIE` porque BICE trunca los nombres largos.
- **GTD:** Buscar la palabra "MANQUEHUE" era peligroso porque las cartolas del BICE incluyen sucursales como "Manquehue Norte 2081", lo que capturaba el número 2081 como si fuera el pago del internet. Se restringió la búsqueda solo a "GTD" o "TELSUR".
