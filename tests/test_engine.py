import io
import unittest
from decimal import Decimal
from unittest.mock import patch
from processor_v3 import reconcile,process_data,extract_all_text,extract_text_from_pdf,summarize,parse_amount
from money import amount,exchange,historical_rate
from rules import classify,seed_rules,suggest_pattern,validate_rule
from workflow import effective_rules,apply_rules,split_school,validate_records,merge_edits

class EngineTests(unittest.TestCase):
    def parse(self,text,**kw):return reconcile(text,rate_lookup=lambda *args:(Decimal('950'),False),**kw)
    def test_formats(self):
        for raw,expected in [('19.900,00','19900'),('10.99','10.99'),('12,99','12.99'),('1,234.56','1234.56'),('861,268','861268'),('-3,390','-3390')]:
            with self.subTest(raw=raw):self.assertEqual(amount(raw),Decimal(expected))
    def test_usd(self):
        for merchant,value,expected in [('YOUTUBE','10.99',10441),('SPOTIFY','12.99',12341),('YOUTUBE','250,00',237500)]:
            with self.subTest(merchant=merchant,value=value):
                row=self.parse(f'01/08 {merchant} US${value}')[0];self.assertEqual(row['Monto'],expected);self.assertEqual(row['Moneda'],'USD')
    def test_context_currency(self):
        row=self.parse('@@HADITAPP_DOCUMENT {"name":"TC Internacional.pdf"}\n01/08 GOOGLE YOUTUBE 0.00 10.99')[0]
        self.assertEqual(row['Monto'],10441)
    def test_small_clp_not_dollars(self):self.assertEqual(self.parse('01/08 SPOTIFY $150')[0]['Monto'],150)
    def test_folio(self):self.assertEqual(self.parse('01/08 123456 Transferencia a ANDY 27.000,00')[0]['Monto'],27000)
    def test_cargo_saldo(self):self.assertEqual(self.parse('01/08 Cargo por Compra en ZAPPING 19.900,00 1.433.078,00')[0]['Monto'],19900)
    def test_full_dates(self):
        rows=self.parse('01/08/2026 AGUAS ANDINAS 10.000,00\n02/08/2026 ENEL 20.000,00')
        self.assertEqual([r['Monto'] for r in rows],[10000,20000]);self.assertEqual(len(rows),2)
    def test_short_date_context(self):self.assertEqual(self.parse('01/08 ENEL 20.000',year=2024,month=8)[0]['Fecha'],'01/08/2024')
    def test_no_year_invented(self):self.assertEqual(self.parse('01/08 ENEL 20.000')[0]['Fecha'],'01/08')
    def test_year_boundary(self):self.assertEqual(self.parse('31/12 ENEL 20.000',year=2026,month=1)[0]['Fecha'],'31/12/2025')
    def test_explicit_school(self):
        for label,value,cat in [('JORNADA EXTENDIDA',50000,'CSFJ (Jornada Extendida)'),('MATERIALES',90000,'CSFJ (Extras/Materiales)'),('MENSUALIDAD',500000,'CSFJ (Mensualidad)'),('CENTRO DE PADRES',40000,'CSFJ (Centro de Padres)'),('CENTRO PADRES',40000,'CSFJ (Centro de Padres)')]:
            with self.subTest(label=label):self.assertEqual(self.parse(f'01/08 COLEGIO FCO.JAVIER {label} ${value}')[0]['Categoría'],cat)
    def test_school_no_guess(self):self.assertEqual(self.parse('01/08 COLEGIO FCO.JAVIER $597626')[0]['Tipo'],'Revisar')
    def test_school_split(self):
        rows=self.parse('01/08 COLEGIO FCO.JAVIER $597626')
        split=split_school(rows,rows[0]['id'],{'CSFJ (Mensualidad)':500000,'CSFJ (Jornada Extendida)':50000,'CSFJ (Extras/Materiales)':27626,'CSFJ (Centro de Padres)':20000})
        self.assertEqual(sum(r['Monto'] for r in split),597626)
        vals,_=summarize(split,212600);self.assertEqual(sum(vals.values()),385026)
    def test_split_rejects_difference(self):
        rows=self.parse('01/08 COLEGIO FCO.JAVIER $10000')
        with self.assertRaises(ValueError):split_school(rows,rows[0]['id'],{'CSFJ (Mensualidad)':9000})
    def test_learned_fixed_not_lost(self):self.assertEqual(self.parse('01/08 LUIS MIGUEL CRUCES 45.000,00')[0]['Categoría'],'JARDINERO')
    def test_unknown_visible(self):self.assertEqual(self.parse('01/08 TIENDA NUEVA $12000')[0]['Tipo'],'Revisar')
    def test_invalid_amount_visible(self):self.assertIsNone(self.parse('01/08 TIENDA NUEVA monto ilegible')[0]['Monto'])
    def test_unknown_currency_visible(self):self.assertIsNone(self.parse('01/08 TIENDA NUEVA EUR 20,00')[0]['Monto'])
    def test_credit(self):self.assertEqual(self.parse('01/08 Abono por transferencia de JUMBO $10000')[0]['Tipo'],'Ingreso')
    def test_cc_payment_not_credit(self):self.assertNotEqual(self.parse('01/08 Cargo por Abono/Pago de Tarjeta $10000')[0]['Tipo'],'Ingreso')
    def test_negative_kept(self):self.assertEqual(self.parse('01/08 SPOTIFY $-10.000')[0]['Monto'],-10000)
    def test_quota(self):self.assertEqual(self.parse('SANTIAGO 01/08/26 0608 10679592 COLEGIO FCO.JAVIER $660.000 $741.780 02/06 $123.630')[0]['Monto'],123630)
    def test_overlap_not_duplicate(self):
        rows=self.parse('@@HADITAPP_DOCUMENT {"name":"a"}\n01/08 ANDY $27000\n@@HADITAPP_DOCUMENT {"name":"b"}\n01/08 ANDY $27000')
        self.assertEqual(len(rows),1)
    def test_identical_in_one_file_kept(self):self.assertEqual(len(self.parse('01/08 TIENDA $1000\n01/08 TIENDA $1000')),2)
    def test_period_validation(self):
        row=self.parse('01/07/2026 ENEL $10000',month=8,year=2026)[0]
        self.assertFalse(row['Período confirmado'])
        with self.assertRaises(ValueError):validate_records([row],final=True)
    def test_empty_input_errors(self):
        with self.assertRaises(ValueError):self.parse('')
    def test_pattern_stable(self):self.assertEqual(suggest_pattern('01/08 TIENDA EJEMPLO 10.000,00'),suggest_pattern('01/09 TIENDA EJEMPLO 11.000,00'))
    def test_saved_rule_wins(self):
        r=validate_rule(dict(match_text='SPOTIFY',category='Música',kind='Variable',owner='Personal',priority=100))
        rows=self.parse('01/08 SPOTIFY $10000',rules=effective_rules(seed_rules(),[r]))
        self.assertEqual(rows[0]['Categoría'],'Música')
    def test_disabled_override(self):
        rules=effective_rules(seed_rules(),[dict(match_text='SPOTIFY',enabled=False)])
        self.assertEqual(self.parse('01/08 SPOTIFY $10000',rules=rules)[0]['Tipo'],'Revisar')
    def test_fallback_retry(self):
        historical_rate.cache_clear()
        with patch('money.requests.get',side_effect=ValueError):
            self.assertEqual(exchange('01/08/2026',950),(Decimal('950'),True))
            self.assertEqual(exchange('01/08/2026',1000),(Decimal('1000'),True))
    def test_pdf_password_redacted(self):
        import pymupdf
        with pymupdf.open() as doc:
            doc.new_page().insert_text((72,72),'01/08 ENEL $10000')
            data=doc.tobytes(encryption=pymupdf.PDF_ENCRYPT_AES_256,owner_pw='owner',user_pw='correct')
        with self.assertRaises(ValueError) as e:extract_text_from_pdf(io.BytesIO(data),'private-test')
        self.assertNotIn('private-test',str(e.exception))
        self.assertIn('ENEL',extract_text_from_pdf(io.BytesIO(data),'correct'))
    def test_uppercase_pdf(self):
        f=io.BytesIO(b'fake');f.name='CARTOLA.PDF'
        with patch('processor_v3.extract_text_from_pdf',return_value='01/08 ENEL $10000'):
            self.assertIn('ENEL',extract_all_text([f],''))
    def test_csv_first_row(self):
        f=io.BytesIO(b'01/08,ENEL,10000\n02/08,ZAPPING,20000');f.name='test.csv'
        self.assertEqual(len(self.parse(extract_all_text([f],''))),2)
    def test_bad_rule(self):
        with self.assertRaises(ValueError):validate_rule(dict(match_text='123456',category='x',kind='Fijo',owner='Compartido'))

if __name__=='__main__':unittest.main()
