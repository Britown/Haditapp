"""Compatibility API using the shared deterministic rule engine."""
import pandas as pd
from rules import seed_rules, classify, suggest_pattern
COLUMNS=['Fecha','Descripción','Categoría','Responsable','Monto','_Original','Tipo']

def load_rules():return seed_rules()
def clean_fallback(desc):return suggest_pattern(desc).title()
def categorize_with_ai(descriptions):
    # Classification must remain reproducible without a remote model or API key.
    return {}

def classify_variable(glosa,monto):
    kind,cat,owner=classify(glosa,rules=load_rules())
    return cat,owner,None

def process_unmatched_to_df(unmatched_list):
    rows=[]
    for item in unmatched_list:
        desc=item.get('_Original',item['Descripción'])
        kind,cat,owner=(item['Tipo'],item['Categoría'],item['Responsable']) if 'Tipo' in item else classify(desc,rules=load_rules())
        rows.append({'Fecha':item['Fecha'],'Descripción':item['Descripción'],'Monto':item['Monto'],
                     'Categoría':cat,'Responsable':owner,'_Original':desc,'Tipo':kind})
    return pd.DataFrame(rows,columns=COLUMNS)
