"""UI-independent validation, editing, training and school split operations."""
from copy import deepcopy
from decimal import Decimal
from rules import classify,normalize,rule_id
from money import clp


def effective_rules(seeds,saved):
    result={rule_id(r['match_text'],r.get('amount')):dict(r) for r in seeds}
    for rule in saved:result[rule_id(rule['match_text'],rule.get('amount'))]=dict(rule)
    return [r for r in result.values() if r.get('enabled',True)]


def apply_rules(records,rules,period=None):
    if period:
        rules=[r for r in rules if not r.get('valid_until') or period<=r['valid_until']]
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


def learn_variable_corrections(before, after, saved):
    """Learn only explicit category/owner edits, never machine predictions."""
    import re
    from rules import validate_rule, suggest_pattern
    previous={r.get('_Original',r['Descripción']):r for r in before}
    learned={}; skipped=0
    for row in after:
        original=row.get('_Original',row['Descripción'])
        old=previous.get(original)
        if not old or all(row.get(k)==old.get(k) for k in ['Categoría','Responsable']):continue
        category=str(row.get('Categoría') or '').strip()
        owner=row.get('Responsable')
        if category in ['', 'Por Revisar'] or owner not in ['Personal','Compartido']:continue
        kind='Ingreso' if category=='Ingresos' else ('Ignorar' if category=='Ignorar' else 'Variable')
        # Extract the recipient RUT before removing references and monetary values.
        rut=re.search(r'\btransferencia\s+a\s+Rut\s+([\d.]+-[\dkK])',original,re.I)
        pattern='TRANSFERENCIA A RUT '+rut.group(1) if rut else suggest_pattern(row['Descripción'])
        if len(normalize(pattern).split())<2 and normalize(pattern) in ['TRANSFERENCIA','COMPRA','PAGO','ABONO','RUT']:
            skipped+=1;continue
        try:
            rule=validate_rule(dict(match_text=pattern,category=category,owner=owner,kind=kind,priority=100,enabled=True,
                                    amount=row.get('Monto') if category.startswith('CSFJ') else None))
        except ValueError:
            skipped+=1;continue
        # Friendly display aliases need their original merchant for future matching.
        if normalize(rule['match_text']) not in normalize(original):
            pattern=suggest_pattern(original)
            try:rule=validate_rule(dict(rule,match_text=pattern))
            except ValueError:skipped+=1;continue
        if rule['id'] in learned and any(learned[rule['id']][k]!=rule[k] for k in ['category','owner','kind']):
            raise ValueError('Hay clasificaciones distintas para el mismo comercio. Usa Entrenar gastos para distinguirlas por monto.')
        learned[rule['id']]=rule
    merged={rule_id(r['match_text'],r.get('amount')):r for r in saved}
    merged.update(learned)
    return list(merged.values()),len(learned),skipped
