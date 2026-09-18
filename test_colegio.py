from processor2 import process_data
import pdfplumber

def get_text(path):
    text = ''
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            text += p.extract_text() + '\n'
    return text

text1 = get_text('/Users/hernanbrito/Documents/Cartolas/08 Agosto/cuenta corriente.pdf')
text2 = get_text('/Users/hernanbrito/Documents/Cartolas/08 Agosto/Tarjeta de credito.pdf')

raw_text = text1 + '\n' + text2
dolar_val = 950
csfj_base = 13.5 * 37900
manda_base = 200000
beneficio = 0

resultados, fechas, unmatch = process_data(raw_text, dolar_val, csfj_base, manda_base, beneficio)

print('Mensualidad:', resultados['CSFJ (Mensualidad)'])
print('Extras:', resultados['CSFJ (Extras/Materiales)'])
print('Jornada:', resultados['CSFJ (Jornada Extendida)'])
