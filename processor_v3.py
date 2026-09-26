"""Statement extraction with source, currency and transaction provenance.

The compatibility process_data API delegates to the same engine used by the UI.
"""
import io
import json
import re
import hashlib
from collections import Counter
from datetime import datetime
from decimal import Decimal
import pandas as pd
import pdfplumber
from money import amount, clp, exchange
from rules import FIXED, classify, seed_rules

DATE = re.compile(r'(?<!\d)(\d{1,2}/\d{1,2}(?:/(?:\d{4}|\d{2}))?)(?!\d)')
START = re.compile(r'^\s*(?:(?:NaN|SANTIAGO|LAS CONDES|PROVIDENCIA)\s+)?(?:\d{4}\s+)?(?:\d{10,}\s+)?(?:\d{1,2}/\d{1,2}(?:/\d{2,4})?|\d{4}-\d{2}-\d{2}|\d{1,2}\s+[a-záéíóú]{3,10}\s+\d{4})\b',re.I)
MONEY = re.compile(r'(?<![\w.,])(?:(US\$|USD|CLP|EUR|€|\$)\s*)?(-?\d+(?:[.,]\d+)*)(?![\w.,])',re.I)
MONTHS = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
SUMMARY = re.compile(r'^(?:SALDO (?:INICIAL|FINAL|ANTERIOR|NUEVO)|TOTAL\b|PAGAR HASTA|MONTO FACTURADO|PER[IÍ]ODO FACTURADO|P[ÁA]GINA\b)',re.I)


def clean_amount(value):
    try: return float(amount(value))
    except ValueError: return 0.0


def get_dolar_historico(fecha, default_dolar):
    return float(exchange(fecha,default_dolar)[0])


def extract_text_from_pdf(file, password=''):
    import pymupdf
    data = file.getvalue() if hasattr(file,'getvalue') else file.read()
    try:
        with pymupdf.open(stream=data,filetype='pdf') as doc:
            if doc.needs_pass and not doc.authenticate(password or ''):
                raise ValueError('El PDF requiere una contraseña válida. Revisa los ajustes.')
            decrypted = doc.tobytes(encryption=pymupdf.PDF_ENCRYPT_NONE)
        with pdfplumber.open(io.BytesIO(decrypted)) as pdf:
            text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
        if not text.strip():
            raise ValueError('El PDF no contiene texto legible; sube una cartola digital o pega el texto.')
        return text
    except ValueError:
        raise
    except Exception:
        raise ValueError('No se pudo leer el PDF. Comprueba el formato y la contraseña.') from None


def extract_text_from_excel(file,is_csv=False):
    # Preserve every row, including the first in exports without a header.
    frames = [pd.read_csv(file,sep=None,engine='python',header=None)] if is_csv else list(pd.read_excel(file,sheet_name=None,header=None).values())
    lines=[]
    for df in frames:
        for row in df.itertuples(index=False,name=None):
            cells=[]
            for value in row:
                if pd.isna(value): continue
                if isinstance(value,(datetime,pd.Timestamp)): value=value.strftime('%d/%m/%Y')
                cells.append(str(value))
            lines.append(' '.join(cells))
    return '\n'.join(lines)


def extract_all_text(uploaded_files,pasted_text,pdf_password=''):
    docs=[]
    if pasted_text and pasted_text.strip(): docs.append(('Texto pegado',pasted_text))
    for f in uploaded_files or []:
        f.seek(0); ext=f.name.lower().rsplit('.',1)[-1]
        if ext=='pdf': text=extract_text_from_pdf(f,pdf_password)
        elif ext in ['xlsx','xls','csv']: text=extract_text_from_excel(f,ext=='csv')
        else: raise ValueError(f'Formato no admitido: {f.name}. Usa PDF, XLSX, XLS o CSV.')
        if not text.strip(): raise ValueError(f'El archivo {f.name} no contiene movimientos legibles.')
        docs.append((f.name,text))
    return '\n'.join('@@HADITAPP_DOCUMENT '+json.dumps({'name':name},ensure_ascii=False)+'\n'+text for name,text in docs)


def documents(raw):
    source='Texto pegado';lines=[]
    for line in str(raw).splitlines():
        if line.startswith('@@HADITAPP_DOCUMENT '):
            if lines: yield source,'\n'.join(lines)
            source=json.loads(line.split(' ',1)[1])['name'];lines=[]
        else: lines.append(line)
    if lines: yield source,'\n'.join(lines)


def date_from_line(line,year=None,month=None):
    iso=re.search(r'\b(\d{4})-(\d{2})-(\d{2})\b',line)
    if iso: date=f'{iso[3]}/{iso[2]}/{iso[1]}'
    else:
        m=DATE.search(line)
        if m:
            parts=m[1].split('/');parts[0]=parts[0].zfill(2);parts[1]=parts[1].zfill(2)
            if len(parts)==3:
                if len(parts[2])==2: parts[2]='20'+parts[2]
            elif year:
                inferred=year - 1 if month==1 and int(parts[1])==12 else year
                parts.append(str(inferred))
            date='/'.join(parts)
        else:
            m=re.search(r'\b(\d{1,2})\s+([a-záéíóú]+)\s+(\d{4})\b',line,re.I)
            if not m:return 'N/A'
            mn=next((i+1 for i,x in enumerate(MONTHS) if x.startswith(m[2].lower()[:3])),None)
            if not mn:return 'N/A'
            date=f'{int(m[1]):02}/{mn:02}/{m[3]}'
    try:datetime.strptime(date,'%d/%m/%Y' if len(date.split('/'))==3 else '%d/%m')
    except ValueError:return 'N/A'
    return date


class StatementLine(str):
    def __new__(cls,text,currency=None):
        value=super().__new__(cls,text);value.currency=currency;return value


def transaction_lines(text):
    current=None;currency=None
    for line in text.splitlines():
        line=line.strip()
        if not line:continue
        if re.search(r'ESTADO DE CUENTA (?:INTERNACIONAL|NACIONAL)',line,re.I):
            if current:yield StatementLine(current,currency);current=None
            currency='USD' if 'INTERNACIONAL' in line.upper() else 'CLP'
            continue
        if SUMMARY.search(line) or re.search(r'^(?:[IVX]+\. |COMPROBANTE|COMISIONES,|[1234]\. ?(?:PRODUCTOS|CARGOS)|DEUDA TOTAL)',line,re.I):
            if current:yield StatementLine(current,currency);current=None
            continue
        if START.search(line) and not re.match(r'^\d{2}/\d{2}/\d{4}\s+a las',line,re.I):
            if current:yield StatementLine(current,currency)
            current=None if re.search(r'SALDO (?:INICIAL|FINAL|ANTERIOR)',line,re.I) else line
        elif current:
            if re.search(r'Cargo por|Abono por|Transferencia|Cheque',current,re.I) and not re.search(r'CUPO TOTAL|FECHA DESCRIPCI|FECHA TRANSACCI|INFORMACI[OÓ]N DE PAGO',line,re.I):
                current+=' '+line
            else:
                yield StatementLine(current,currency);current=None
    if current:yield StatementLine(current,currency)


def parse_amount(line,currency='CLP'):
    working=re.split(r'\s+\d{2}/\d{2}/\d{4}\s+a las',line,maxsplit=1,flags=re.I)[0]
    working=re.sub(r'\b\d{4}-\d{2}-\d{2}\b',' ',working)
    working=DATE.sub(' ',working)
    working=re.sub(r'\b\d{1,2}\s+[a-záéíóú]{3,10}\s+\d{4}\b',' ',working,flags=re.I)
    working=re.sub(r'\b\d[\d.]*-[\dkK]\b|\b\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?\b',' ',working)
    working=re.sub(r'\b\d+\s+de\s+\d+\b|\b(?:Nro\.?|N°|N\.Ref:)\s*\d+\b',' ',working,flags=re.I)
    matches=list(MONEY.finditer(working))
    # Pure integer references before the merchant/transaction text are never amounts.
    first_letter=re.search(r'[A-Za-zÁÉÍÓÚáéíóú]',working)
    candidates=[m for m in matches if not (not m[1] and first_letter and m.start()<first_letter.start())
                and not (not m[1] and m[2].lstrip('-').isdigit() and len(m[2].replace('-',''))>=10)]
    if not candidates:raise ValueError('No se reconoce el importe del movimiento')
    # Ignore numbers in continuation metadata after the charge/saldo columns.
    useful=[m for m in candidates if m[1] or '.' in m[2] or ',' in m[2]]
    if not useful:useful=candidates
    quota=bool(re.search(r'\b\d{1,2}/\d{1,2}\s+\$?\s*-?[\d.,]+\s*$',line)) or bool(re.search(r'\b\d+\s+de\s+\d+',line,re.I))
    # Explicit currency belongs to each amount; CC conversion notes must not override its CLP debit.
    is_cc=bool(re.search(r'Cargo por|Abono por|Transferencia',line,re.I))
    if is_cc:
        suffix=re.search(r'\b(?:por US\$|al tipo de|Neto\s*\$)',working,re.I)
        if suffix:useful=[m for m in useful if m.start()<suffix.start()] or useful
    end_values=[]
    for m in useful:
        # Formatted monetary pairs separated only by whitespace are cargo + saldo.
        if end_values and working[end_values[-1].end():m.start()].strip():end_values=[]
        end_values.append(m)
    selected=useful[-1]
    if len(end_values)>=2 and not quota and (is_cc or currency=='CLP'):
        selected=end_values[-2]
    cur={'US$':'USD','USD':'USD','CLP':'CLP','EUR':'EUR','€':'EUR','$':'CLP'}.get((selected[1] or '').upper(),currency)
    return amount(selected[2]),cur


def display_description(line):
    """Remove statement metadata for display only; keep the original for matching."""
    text = re.sub(r'\s+', ' ', str(line)).strip()
    if re.search(r'\bONECLICK\s+RECURRENTE\s+PCS\s*SANTIAGO\b', text, re.I):
        return 'Entel plan celular'
    text = re.sub(r'\bCargo\s+por\s+', '', text, flags=re.I)
    international = re.match(r'^\d{4}\s+\d{10,}\s+\d{2}/\d{2}/(?:\d{4}|\d{2})\s+(.+)$', text)
    if international:
        merchant = re.split(r'\s+(?:US\$|\$|\d[\d.]*,\d{2}\b)', international.group(1), maxsplit=1)[0]
        merchant = re.sub(r'\s+\d{7,}\s+[A-Z]{2}\s*$', '', merchant).strip()
        return merchant
    timestamp = re.search(r'\bel\s+((?:\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}))\s+a las\s+(\d{1,2}:\d{2})(\s*hrs\.?)?', text, re.I)
    if re.search(r'\btransferencia\b', text, re.I):
        recipient = re.search(r"\ba\s+([A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ '’-]+?)\s+Rut\b", text, re.I)
        rut = re.search(r'\btransferencia\s+a\s+(Rut\s+[\d.]+-[\dkK])', text, re.I)
        if recipient or rut:
            name = ' '.join(recipient.group(1).split()[:2]) if recipient else rut.group(1)
            label = f'Transferencia a {name}'
            if timestamp:
                label += f' el {timestamp.group(1)} a las {timestamp.group(2)}'
                if timestamp.group(3):
                    label += ' hrs.'
            return label
    purchase = re.search(r'\b(?:Cargo\s+por\s+)?Compra\s+en\s+(.+?)(?=\s+El\s+(?:\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})\b)', text, re.I)
    if purchase:
        merchant = purchase.group(1).strip()
        # Bank exports may insert the amount between "a" and "las".
        clock = re.search(r'\blas\s+(\d{1,2}:\d{2}(?::\d{2})?)\b', text[purchase.end():], re.I)
        date = re.search(r'\bEl\s+(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})\b', text[purchase.end():], re.I)
        return f'Compra en {merchant} El {date.group(1)}' + (f' a las {clock.group(1)}' if clock else '')
    fee = re.search(r'\bCOMISI[ÓO]N\b.*?(?=\s+(?:US\$|\$|\d[\d.,]*(?:\s|$))|$)', text, re.I)
    if fee:
        return fee.group(0).strip()
    card = re.match(r'^(?:[A-Za-zÁÉÍÓÚÜÑáéíóúüñ .-]+\s+)?\d{2}/\d{2}/(?:\d{4}|\d{2})\s+\d{4}\s+\d{6,}\s+(.+?)\s+(?:US\$|\$)', text)
    if card:
        return card.group(1).strip()
    # Only strip recognizable metadata, never bare numbers that may identify a merchant.
    text = re.sub(r'^\d{2}/\d{2}(?:/\d{2,4})?\s+(?:\d{6,}\s+)?', '', text)
    text = re.sub(r'(?<![\w.-])(?:\$\s*\d[\d.,]*|\d{1,3}(?:\.\d{3})*,\d{2})(?![\w.-])', '', text)
    text = re.sub(r'[,.;]*\s*\bMonto\s*:?\s*(?:US\$|\$)?\s*[\d.,]+', '', text, flags=re.I)
    text = re.sub(r'[,.;]*\s*\bMonto\s*:?\s*$', '', text, flags=re.I)
    return re.sub(r'\s+', ' ', text).strip(' ,.;')


def reconcile(raw,dolar_val=950,year=None,month=None,rules=None,currency_override='Auto',rate_lookup=None):
    records=[];warnings=[];previous=Counter();rules=seed_rules() if rules is None else rules
    if year:
        period=f'{year:04}-{month or 12:02}'
        rules=[r for r in rules if not r.get('valid_until') or period<=r['valid_until']]
    for source,text in documents(raw):
        # Currency context is preserved per statement, not guessed from the size of charges.
        currency='USD' if re.search(r'internacional|\bTCI\b',source+' '+text[:1200],re.I) else 'CLP'
        if currency_override!='Auto':currency=currency_override
        in_document=Counter()
        for index,line in enumerate(transaction_lines(text)):
            date=date_from_line(line,year,month)
            status='';raw_amount=None;converted=None;rate=None;fallback=False
            try:
                raw_amount,cur=parse_amount(line,getattr(line,'currency',None) or currency)
                if cur=='USD':
                    rate,fallback=(rate_lookup or exchange)(date,dolar_val)
                    converted=clp(raw_amount*Decimal(str(rate)))
                    if fallback:status='Dólar de respaldo; verifica el tipo de cambio'
                elif cur=='CLP':converted=clp(raw_amount)
                else:status='Moneda sin tipo de cambio: ingresa el monto CLP';converted=None
            except ValueError as e:
                cur=currency;status=str(e)
            # Stable exact movement identity includes raw text to avoid collapsing legitimate equal charges.
            canonical=re.sub(r'\s+',' ',line.upper()).strip()
            fingerprint=hashlib.sha256((date+'|'+canonical+'|'+cur).encode()).hexdigest()
            in_document[fingerprint]+=1
            if in_document[fingerprint]<=previous[fingerprint]:continue
            credit=bool(re.search(r'\bABONO(?:S)?\b|\bREMUNERACION|\bSUELDO\b',line,re.I)) and not bool(re.search(r'\bCARGO\b',line,re.I))
            kind,cat,owner=classify(line,credit,rules,converted)
            if kind=='Revisar' and 'CHEQUE DE CANJE' in line.upper() and converted==472000:
                kind,cat,owner='Fijo','MANDARINO','Compartido'
            if date=='N/A': status='Fecha inválida; revisa el movimiento'
            if date!='N/A' and month and year:
                dt=datetime.strptime(date,'%d/%m/%Y')
                if (dt.month,dt.year)!=(month,year):status=(status+'; ' if status else '')+'Fuera del mes seleccionado: confirmar período'
            if converted is None or date=='N/A':kind='Revisar'
            identifier=hashlib.sha256(f'{fingerprint}:{in_document[fingerprint]}'.encode()).hexdigest()[:24]
            records.append({'id':identifier,'Fecha':date,'Descripción':display_description(line),'Tipo':kind,'Categoría':cat,'Responsable':owner,
                            'Monto':abs(converted) if credit and converted is not None else converted,
                            'Moneda':cur,'Monto original':float(raw_amount) if raw_amount is not None else None,
                            'Tipo de cambio':float(rate) if rate is not None else None,'Fuente':source,'Estado':status,
                            '_Original':line,'Período confirmado':not ('Fuera del mes' in status),'Revisado':False})
        previous |= in_document
    if not records:raise ValueError('No se detectaron movimientos con fecha. Revisa el archivo o pega filas con fecha, descripción y monto.')
    return records


def summarize(records,beneficio=0):
    values={k:0 for k in FIXED};dates={k:'N/A' for k in FIXED}
    for row in records:
        if row['Tipo']!='Fijo' or row.get('Monto') is None or not row.get('Período confirmado',True):continue
        cat=row['Categoría'];values[cat]=values.get(cat,0)+clp(row['Monto'])
        dates[cat]=', '.join(dict.fromkeys(([dates[cat]] if dates.get(cat,'N/A')!='N/A' else [])+[row['Fecha']]))
    for category in ['MANDARINO','CSFJ (Mensualidad)']:
        values[category]=max(0,values.get(category,0)-clp(beneficio))
    return values,dates


def process_data(raw_text,dolar_val,csfj_base,manda_base,beneficio,manda_mat_val=220000,year=None,month=None,rules=None):
    records=reconcile(raw_text,dolar_val,year,month,rules,rate_lookup=lambda date,default:(get_dolar_historico(date,default),False))
    results,dates=summarize(records,beneficio)
    unmatched=[dict(r) for r in records if r['Tipo']!='Fijo']
    return results,dates,unmatched
