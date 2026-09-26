"""Shared fixed/variable rules, portable seeds and persistent user overrides."""
import csv
import re
import unicodedata
from pathlib import Path
from hashlib import sha256

FIXED = ['AGUA (Aguas Andinas)', 'LUZ (Enel)', 'GAS (Metrogas)', 'INTERNET (GTD)',
         'SEGURO CASA (Consorcio)', 'ZAPPING', 'AMAZON PRIME', 'HBO MAX',
         'YOUTUBE PREMIUM', 'SPOTIFY DUO', 'ASEO', 'GASTOS COMUNES (Khipu)',
         'PISCINA (Andy)', 'JARDINERO', 'MANDARINO', 'MANDARINO (Matrícula)',
         'CSFJ (Mensualidad)', 'CSFJ (Jornada Extendida)', 'CSFJ (Extras/Materiales)',
         'CSFJ (Centro de Padres)', 'CONTRIBUCIONES (SII)']


def normalize(text):
    text = ''.join(c for c in unicodedata.normalize('NFKD', str(text)) if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', re.sub(r'[^A-Z0-9]+', ' ', text.upper())).strip()


def suggest_pattern(description):
    text = str(description)
    merchant = re.search(r'\bCompra\s+en\s+(.+?)(?=\s+El\s+(?:\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})\b)', text, re.I)
    if merchant:
        return normalize(merchant.group(1))
    # Use the recipient rather than the sender when the bank gives both.
    recipient = re.search(r'\bdesde\b.*?\ba\s+(.+?)(?:\s+Rut\b|\s+a Cuenta\b|$)', text, re.I)
    if recipient:
        text = recipient.group(1)
    text = re.sub(r'\b\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?\b|\b\d{4}-\d{2}-\d{2}\b', ' ', text)
    text = re.sub(r'\b\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?\b', ' ', text)
    text = re.sub(r'\b\d[\d.,]*-[\dkK]\b', ' ', text)
    text = re.sub(r'(?i)\b(?:el|a las|monto|tasa int|periodo facturado)\b.*$', '', text)
    text = re.sub(r'(?i)(?:US\$|\$)\s*-?[\d.,]+|\b\d[\d.,]*\b', ' ', text)
    text = re.sub(r'(?i)\b(?:NaN|cargo por compra en|cargo por transferencia a|abono por transferencia de|transferencia de|cargo por pago|rut|nro|santiago|las condes|providencia)\b', ' ', text)
    return normalize(text)


def rule_id(pattern, value=None):
    return sha256((normalize(pattern)+(f'|{float(value):g}' if value is not None else '')).encode()).hexdigest()[:24]


def validate_rule(rule):
    rule = dict(rule)
    rule['match_text'] = normalize(rule.get('match_text', ''))
    if len(rule['match_text']) < 4 or not re.search(r'[A-Z]{3}', rule['match_text']):
        raise ValueError('La regla necesita un comercio o destinatario específico (al menos 4 caracteres).')
    if rule.get('kind') not in ['Fijo', 'Variable', 'Ingreso', 'Ignorar', 'Revisar']:
        raise ValueError('Tipo de regla inválido')
    if not str(rule.get('category', '')).strip():
        raise ValueError('Indica una categoría o concepto fijo')
    if rule.get('owner') not in ['Compartido', 'Personal', 'Por Revisar']:
        raise ValueError('Responsable inválido')
    rule['priority'] = int(rule.get('priority', 100))
    rule['id'] = rule_id(rule['match_text'],rule.get('amount'))
    return rule


DEFAULTS = [
 ('AGUAS ANDINAS', FIXED[0]), ('ENEL', FIXED[1]), ('METROGAS', FIXED[2]),
 ('GTD', FIXED[3]), ('TELSUR', FIXED[3]), ('CONSORCIO VIDA', FIXED[4]),
 ('ZAPPING', 'ZAPPING'), ('PRIME VIDEO', 'AMAZON PRIME'), ('AMAZON PRIME', 'AMAZON PRIME'),
 ('HBO', 'HBO MAX'), ('MERPAGO MAX', 'HBO MAX'), ('MP MAX', 'HBO MAX'),
 ('YOUTUBE', 'YOUTUBE PREMIUM'), ('SPOTIFY', 'SPOTIFY DUO'),
 ('MARISEL', 'ASEO'), ('CAROLINA MENDOZA', 'ASEO'), ('CRISTINA CAISALUISA', 'ASEO'),
 ('A CAROLA MILLALEN', 'ASEO'),
 ('ANDY', 'PISCINA (Andy)'), ('17.766.248-8', 'PISCINA (Andy)'), ('LUIS MIGUEL CRUCES', 'JARDINERO'),
 ('KHIPU', 'GASTOS COMUNES (Khipu)'), ('MANDARINO', 'MANDARINO'),
 ('MANDARINO MATRICULA', 'MANDARINO (Matrícula)'),
 ('PAGO SII', 'CONTRIBUCIONES (SII)'), ('CONTRIBUCIONES', 'CONTRIBUCIONES (SII)')]


def seed_rules():
    rules = [dict(match_text=k, category=c, kind='Fijo', owner='Compartido', priority=20, clean_name=c) for k,c in DEFAULTS]
    # Confirmed by the owner: August tuition and extended-day installment plan.
    rules.extend([
        dict(match_text='COLEGIO FCO JAVIER',amount=551405,category='CSFJ (Mensualidad)',kind='Fijo',owner='Compartido',priority=100),
        dict(match_text='COLEGIO FCO JAVIER',amount=123630,category='CSFJ (Jornada Extendida)',kind='Fijo',owner='Compartido',priority=100,valid_until='2026-12'),
    ])
    path = Path(__file__).with_name('reglas_variables.csv')
    if path.exists():
        with path.open(encoding='utf-8') as f:
            for r in csv.DictReader(f):
                # Historical "manual" rows contain accidental multi-transaction matches.
                # Keep stable curated seeds; retain original CSV for explicit migration.
                if len(re.findall(r'\d{1,2}/\d{1,2}', r['match_text']))>1:
                    continue
                if 'manual' in r.get('notes','').lower():
                    r['match_text']=suggest_pattern(r['match_text'])
                if len(r['match_text'])<4:continue
                cat = r['category']
                if cat == 'Gastos fijos':
                    continue  # Covered by explicit defaults, otherwise remains reviewable.
                owner = r['owner'] if r['owner'] in ['Personal','Compartido'] else 'Por Revisar'
                kind = 'Ingreso' if cat == 'Ingresos' else ('Ignorar' if cat == 'Ignorar' else 'Variable')
                rules.append(dict(match_text=normalize(r['match_text']),category=cat,owner=owner,kind=kind,
                                  priority=int(r.get('priority') or 1),clean_name=r.get('clean_name','')))
    for pattern in ['MONTO CANCELADO','IMPUESTO DECRETO LEY 3475','ABONO PAGO DE TARJETA DE CREDITO']:
        rules.append(dict(match_text=pattern,category='Gastos bancarios',kind='Variable',owner='Personal',priority=200))
    rules.append(dict(match_text='TUU 369 BARBER ST',category='Barbería',kind='Variable',owner='Personal',priority=200))
    rules.append(dict(match_text='A TIARE GONZALEZ',category='Verdulería',kind='Variable',owner='Compartido',priority=200))
    rules.append(dict(match_text='COLINA DEPORTES EL 19 09 2026',amount=11000,category='Entretenimiento',kind='Variable',owner='Personal',priority=200,display_name='Fonda Colina — Entretenimiento'))
    rules.append(dict(match_text='DONDE COLOMBA EL 19 09 2026 A LAS 15 34 54',amount=14000,category='Gustitos',kind='Variable',owner='Personal',priority=200,description_suffix='2x anticuchos'))
    rules.append(dict(match_text='PARDESHI TADKA CO EL 10 09 2026 A LAS 13 51 01',amount=11000,category='Almuerzo trabajo',kind='Variable',owner='Personal',priority=200))
    return rules


def match_rule(description, rules, value=None):
    text = normalize(description)
    gardener_transfer = bool(re.search(r'\bTRANSFERENCIA\b', text) and
                             re.search(r'\bA LUIS MIGUEL CRUCES\b', text))
    candidates = [r for r in rules if r.get('enabled',True) and normalize(r.get('match_text',''))
                  and (normalize(r.get('category','')) != 'JARDINERO' or gardener_transfer)
                  and f" {normalize(r['match_text'])} " in f' {text} '
                  and (r.get('amount') is None or value is not None and float(r['amount'])==float(value))]
    return max(candidates, key=lambda r:(int(r.get('priority',0)),len(normalize(r['match_text']))),default=None)


def classify(description, is_credit=False, rules=None, value=None):
    text = normalize(description)
    rules = seed_rules() if rules is None else rules
    matched = match_rule(description, rules, value)
    # Explicit saved overrides win; bank credit/debit direction wins over legacy seeds.
    if matched and int(matched.get('priority',0)) >= 100:
        return matched['kind'], matched['category'], matched['owner']
    if is_credit:
        return 'Ingreso', 'Ingresos', 'Personal'
    if 'COLEGIO' in text or 'CSFJ' in text or 'SAN FRANCISCO JAVIER' in text:
        concepts = []
        for words, category in [(['CENTRO DE PADRES','CENTRO PADRES','CPADRES'],'CSFJ (Centro de Padres)'),
                                (['JORNADA','EXTENDIDA'],'CSFJ (Jornada Extendida)'),
                                (['MATERIAL','MATERIALES','UTILES','SEGURO ESCOLAR'],'CSFJ (Extras/Materiales)'),
                                (['MENSUALIDAD','COLEGIATURA'],'CSFJ (Mensualidad)')]:
            if any(w in text for w in words): concepts.append(category)
        if len(concepts)==1:
            return 'Fijo', concepts[0], 'Compartido'
        return 'Revisar', 'CSFJ (Por desglosar)', 'Por Revisar'
    if 'MANDARINO' in text and ('MATRICULA' in text or 'MATERIALES' in text):
        return 'Fijo', 'MANDARINO (Matrícula)', 'Compartido'
    if matched and matched['kind']=='Ingreso' and 'CARGO' in text:
        return 'Revisar','Por Revisar','Por Revisar'
    if matched:
        return matched['kind'], matched['category'], matched['owner']
    return 'Revisar','Por Revisar','Por Revisar'
