"""Conservative BICE email parsing and one-to-one transfer enrichment."""
import re
from datetime import datetime
from rules import normalize
from money import clp,amount as parse_amount


def parse_transfer_email(text, subject=''):
    text=re.sub(r'\s+',' ',text).strip()
    amount=re.search(r'\bMonto\s*:?\s*\$\s*([\d.,]+)',text,re.I)
    # Require the operation date, never substitute the email reception date.
    dated=re.search(r'\bFecha(?:\s+(?:de\s+)?(?:transferencia|operaci[oó]n))?\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}-\d{2}-\d{2})',text,re.I)
    name=re.search(r'\bNombre(?:\s+del?\s+destinatario)?\s*:?\s*(.+?)(?=\s+(?:RUT|Banco|Tipo|N[uú]mero)\b)',text,re.I)
    recipient=text[name.end():] if name else ''
    rut=re.match(r'\s*RUT\s*:?\s*([\d.]+-[\dkK])',recipient,re.I)
    operation=re.search(r'\bOperaci[oó]n\s*(?:N[uú]mero|N[°º])?\s*:?\s*(\d{6,})',text,re.I)
    message=re.search(r'\bMensaje\s*:?\s*(.*?)(?=\s+(?:Operaci[oó]n|Cuenta|Banco|Rut|Tipo)\b|$)',text,re.I)
    if not dated:
        from processor_v3 import MONTHS
        spanish=re.search(r'\bFecha(?:\s+(?:de\s+)?(?:transferencia|operaci[oó]n))?\s*:?\s*(\d{1,2})\s+(?:de\s+)?([A-Za-záéíóú]+)\.?\s+(?:de\s+)?(\d{4})',text,re.I)
        if spanish:
            month=next((i+1 for i,m in enumerate(MONTHS) if m.startswith(spanish[2].lower())),None)
            if month:
                text=text[:spanish.start()]+f'Fecha {spanish[1]}/{month}/{spanish[3]}'+text[spanish.end():]
                return parse_transfer_email(text,subject)
    if not amount or not dated:return None
    value=dated[1].replace('/','-')
    try:
        day=datetime.strptime(value,'%Y-%m-%d' if len(value.split('-')[0])==4 else '%d-%m-%Y').date().isoformat()
        amount_value=clp(parse_amount(amount[1]))
    except ValueError:return None
    if amount_value<=0:return None
    return dict(amount=amount_value,date=day,name=name[1].strip(' :') if name else '',
                rut=normalize(rut[1]) if rut else '',operation=operation[1] if operation else '',
                message=message[1].strip(' :') if message else '',subject=subject)


def enrich_transfers(rows, emails):
    """Leave original text, classification and money unchanged; ambiguity means no match."""
    candidates={};uses={}
    for index,row in enumerate(rows):
        raw=str(row.get('_Original',row['Descripción']))
        if 'TRANSFERENCIA' not in normalize(raw):continue
        dates=re.findall(r'\b\d{4}-\d{2}-\d{2}\b|\b\d{2}/\d{2}/\d{4}\b',raw)
        value=dates[-1] if dates else row.get('Fecha','')
        try:day=datetime.strptime(value,'%Y-%m-%d' if '-' in value else '%d/%m/%Y').date().isoformat()
        except ValueError:continue
        recipient=re.search(r'\b(?:transferencia\s+a|desde\b.*?\ba)\s+(.+?)(?=\s+(?:\d[\d.,]*,\d{2}|Banco|B\.)|$)',raw,re.I)
        recipient_text=normalize(recipient[1]) if recipient else ''
        eligible=[]
        for eid,item in enumerate(emails):
            if item['date']!=day or item['amount']!=row.get('Monto'):continue
            rut=item.get('rut','');name=normalize(item.get('name',''));operation=item.get('operation','')
            identity=(rut and f' {rut} ' in f' {recipient_text} ') or (name and len(name.split())>=2 and f' {name} ' in f' {recipient_text} ')
            if operation and re.search(r'(?<!\d)'+re.escape(operation)+r'(?!\d)',raw):identity=True
            if identity:eligible.append(eid)
        for eid in eligible:uses[eid]=uses.get(eid,0)+1
        if len(eligible)==1:candidates[index]=eligible[0]
    result=[dict(r) for r in rows]
    for index,eid in candidates.items():
        if uses[eid]!=1:continue
        item=emails[eid];message=item.get('message') or item.get('subject')
        if message:
            suffix=' | Mensaje BICE: '+message
            if not result[index]['Descripción'].endswith(suffix):result[index]['Descripción']+=suffix
    return result
