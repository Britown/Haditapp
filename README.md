# Haditapp

Conciliación de gastos familiares en Streamlit. Python 3.12 recomendado.

```sh
pip install -r requirements.txt
python -m unittest discover -s tests -v
streamlit run app.py
```

## Entrenamiento

Procesa una cartola y abre **Entrenar gastos**. Selecciona un movimiento, revisa el texto estable del comercio/destinatario, el tipo (Fijo/Variable/Ingreso/Ignorar), concepto y responsable. **Guardar regla y aplicar** guarda en Firebase y actualiza los resultados de esta sesión. Las reglas se pueden corregir o desactivar. Las reglas guardadas prevalecen sobre las reglas base; las correcciones manuales de movimientos no se sobrescriben al reaplicar reglas.

Cuando la glosa del colegio no indica el concepto, usa el comprobante para asignarlo. Puedes limitar una regla a un monto concreto para distinguir cobros con la misma glosa; un importe distinto queda para revisión. Un pago combinado se puede desglosar en mensualidad, jornada, materiales y centro de padres; la suma debe coincidir exactamente. El beneficio se descuenta una sola vez por hijo del concepto mensual correspondiente.

**Guardar conciliación e historial** conserva los movimientos y el desglose en Firebase. El guardado de variables es explícito; aplica/guarda las ediciones antes de cambiar de sección. No se confirman guardados cuando falla la base de datos.

## Configuración existente

Usa los secretos de Streamlit, nunca los subas a Git: `firebase` (cuenta de servicio), `gmail.email`, `gmail.app_password` (contraseña de aplicación), `gcp_service_account` y su `master_sheet_url`. La clasificación determinista y las reglas no requieren IA ni clave de Gemini.

Las reglas nuevas se almacenan en `haditapp_config/rules`, con revisión para detectar cambios concurrentes. Los meses se conservan en `conciliaciones` y las colecciones anteriores de historial. El CSV existente sigue siendo la fuente de reglas base; se evitan patrones históricos que mezclaron varias transacciones.

Gmail examina todos los adjuntos PDF únicos en un intervalo amplio, incluyendo el mes solicitado; selecciona por el inicio del período facturado cuando existe, o por el mes predominante de las transacciones. Si un PDF candidato no se puede leer, pide contraseña/carga manual en vez de entregar un resultado parcial silencioso.

Los tipos de cambio exitosos se cachean por fecha. Un fallo usa el dólar de respaldo y se informa en la interfaz; se reintenta en siguientes consultas. La moneda procede del documento o del monto, nunca del tamaño del gasto.

## Límites explícitos

Un documento con glosa ambigua no permite deducir conceptos solo por su monto. Los movimientos desconocidos quedan visibles para entrenarlos. Los PDF escaneados sin texto requieren un archivo digital o texto pegado. La comprobación local simula Gmail y Firebase; su disponibilidad y las credenciales del despliegue deben verificarse en Streamlit.

Los casos de prueba son sintéticos. No publiques cartolas, claves ni dumps de diagnóstico. Las pruebas automáticas ejercitan el mismo motor importado por la aplicación.
