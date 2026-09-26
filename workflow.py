"""UI-independent validation, editing, training and school split operations."""
from copy import deepcopy
from decimal import Decimal
from rules import classify,normalize,rule_id
from money import clp


def effective_rules(seeds,saved):
    result={rule_id(r['match_text']):dict(r) for r in seeds}
    for rule in saved:result[rule_id(rule['match_text'],rule.get('amount'))]=dict(rule)
    return [r for r in result.values() if r.get('enabled',True)]


def apply_rules(records,rules):
    result=deepcopy(records)
    for row in result:
        if row.get('Revisado') or row.get('parent_id'):continue
        credit=row['Tipo']=='Ingreso'
        kind,cat,owner=classify(row['_Original'],credit,rules,row['Monto'])
        row.update(Tipo=kind,Categoría=cat,Responsable=owner)
        if row['Monto'] is None:row['Tipo']='Revisar'
    return result


def validate_records(records,final=False):
    ids=set()
    for row in records:
        if row['id'] in ids:raise ValueError('Identificadores de movimiento duplicados')
        ids.add(row['id'])
        if row.get('Monto') is not None:
            if not Decimal(str(row['Monto'])).is_finite():raise ValueError('Monto no válido')
            if Decimal(str(row['Monto']))!=clp(row['Monto']):raise ValueError('Los montos CLP deben ser enteros')
        if row['Tipo'] not in ['Fijo','Variable','Ingreso','Ignorar','Revisar']:raise ValueError('Tipo inválido')
        if row['Responsable'] not in ['Compartido','Personal','Por Revisar']:raise ValueError('Responsable inválido')
        if final and row['Tipo']!='Ignorar':
            if row['Monto'] is None or row['Tipo']=='Revisar' or row['Responsable']=='Por Revisar':raise ValueError('Quedan movimientos por revisar')
            if not row.get('Período confirmado',False):raise ValueError('Confirma los movimientos fuera del mes o márcalos como Ignorar')
            if not str(row.get('Categoría','')).strip() or row['Fecha']=='N/A':raise ValueError('Falta categoría o fecha válida')


def merge_edits(records,edited):
    result=deepcopy(records);byid={r['id']:r for r in result}
    editable=['Tipo','Categoría','Responsable','Monto','Descripción','Período confirmado']
    for row in edited:
        target=byid[row['id']]
        changed=False
        for key in editable:
            value=row[key]
            if key=='Monto' and value is not None:value=clp(value)
            if target.get(key)!=value:target[key]=value;changed=True
        if changed:target['Revisado']=True
    validate_records(result)
    return result


def split_school(records,identifier,allocations):
    original=next(r for r in records if r['id']==identifier)
    if original['Monto'] is None or original['Monto']<=0:raise ValueError('Primero confirma el importe CLP del pago')
    if any(Decimal(str(v))<0 for v in allocations.values()):raise ValueError('Los conceptos no pueden ser negativos')
    if sum(Decimal(str(v)) for v in allocations.values())!=Decimal(str(original['Monto'])):
        raise ValueError('El desglose debe sumar exactamente el pago original')
    children=[]
    for index,(cat,value) in enumerate(allocations.items()):
        if value:
            row=deepcopy(original)
            row.update(id=f'{identifier}:{index}',parent_id=identifier,Tipo='Fijo',Categoría=cat,
                       Responsable='Compartido',Monto=clp(value),Revisado=True)
            row['Descripción']=f'{original["Descripción"]} — {cat}'
            # Original foreign amount is attached to the parent, not duplicated as a child amount.
            row['Pago original CLP']=original['Monto'];row['Monto original']=None
            children.append(row)
    return [r for r in records if r['id']!=identifier]+children
