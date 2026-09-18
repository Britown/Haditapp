# config.py
# Archivo de configuración central de Hadita Maestra PRO

# 1. Factores de División (Proporcionalidad de ingresos)
FACTORES_DIVISION = {
    "PAPA": 0.6377,
    "MAMA": 0.3623
}

# 2. Valores Base (Suelen cambiar mes a mes por la UF)
# Estos son los valores por defecto que la UI sugerirá.
VALORES_BASE_MES = {
    "uf_colegio": 13.5,
    "valor_uf": 37900.0,
    "mensualidad_mandarino": 472000,
    "beneficio_empleador_por_hijo": 212600,
    "valor_dolar": 950.0  # Valor referencial para conversión de TC Internacional
}

# 3. Muestra del Catálogo de Gastos Fijos (Reglas de negocio)
GASTOS_FIJOS_REGLAS = [
    {
        "id": "agua_andinas",
        "nombre": "AGUA (Huechuraba)",
        "keywords": ["AGUAS ANDINAS", "PAC AGUAS"],
        "dia_esperado": 2,
        "es_opcional": False,
        "monto_fijo": None # Es variable
    },
    {
        "id": "csfj_mensualidad",
        "nombre": "CSFJ Marti Mensualidad",
        "keywords": ["SAN FRANCISCO", "CSFJ"],
        "dia_esperado": 3,
        "es_opcional": False,
        "usa_beneficio": True # Flag para aplicar la resta matemática
    },
    {
        "id": "amz_prime",
        "nombre": "AMZ PRIME VIDEO",
        "keywords": ["AMAZON PRIME", "PRIME VIDEO"],
        "dia_esperado": 25,
        "es_opcional": True, # Si no está en la cartola, se ignora sin alertar
        "monto_fijo": None
    }
    # (Aquí iremos poblando los 22 ítems discutidos)
]
