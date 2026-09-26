"""Parsing and conversion of amounts without inferring currency from merchants."""
import re
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from functools import lru_cache
import requests


def amount(value):
    text = re.sub(r'(?:US\$|CLP|USD|EUR|\$|\s)', '', str(value), flags=re.I)
    negative = text.startswith('-') or (text.startswith('(') and text.endswith(')'))
    text = text.strip('-+()')
    if not re.fullmatch(r'\d+(?:[.,]\d+)*', text):
        raise ValueError('Monto inválido')
    if '.' in text and ',' in text:
        decimal = '.' if text.rfind('.') > text.rfind(',') else ','
        text = text.replace(',' if decimal == '.' else '.', '').replace(decimal, '.')
    elif '.' in text or ',' in text:
        sep = '.' if '.' in text else ','
        parts = text.split(sep)
        if all(len(p) == 3 for p in parts[1:]):
            text = ''.join(parts)
        elif len(parts) == 2 and len(parts[-1]) in (1, 2):
            text = text.replace(sep, '.')
        else:
            raise ValueError('Separadores ambiguos en monto')
    return Decimal(text) * (-1 if negative else 1)


def clp(value):
    return int(Decimal(str(value)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


@lru_cache(maxsize=512)
def historical_rate(date, currency='dolar'):
    """Only successful rates are cached. Failures can be retried."""
    datetime.strptime(date, '%d/%m/%Y')
    response = requests.get(f'https://mindicador.cl/api/{currency}/{date.replace("/", "-")}', timeout=3)
    response.raise_for_status()
    series = response.json().get('serie', [])
    if not series:
        raise ValueError('No hay indicador para esa fecha')
    value = Decimal(str(series[0]['valor']))
    if value <= 0:
        raise ValueError('Indicador inválido')
    return value


def exchange(date, fallback):
    try:
        return historical_rate(date), False
    except (requests.RequestException, ValueError, KeyError, TypeError):
        if Decimal(str(fallback)) <= 0:
            raise ValueError('Ingresa un dólar de respaldo mayor que cero')
        return Decimal(str(fallback)), True
