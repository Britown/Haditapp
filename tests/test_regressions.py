import io
import unittest
from unittest.mock import patch
from email.message import EmailMessage
from processor_v3 import reconcile,summarize
from rules import validate_rule,seed_rules
from workflow import effective_rules,apply_rules
from variables_processor import process_unmatched_to_df
import gmail_fetcher as g

class Regressions(unittest.TestCase):
    def test_pool_saldo_followed_by_bank_date(self):
        rows=reconcile('28/08 12345678 Cargo por transferencia a ANDY 27.000,00 1.022.689,00\nB.Estado, el 28/08/2026 a las 07:12',year=2026)
        self.assertEqual(summarize(rows)[0]['PISCINA (Andy)'],27000)
    def test_international_reference_prefix(self):
        rows=reconcile('ESTADO DE CUENTA INTERNACIONAL DE TARJETA DE CRÉDITO\n0309 12345678901234567890123 02/09/26 PP*GOOGLE YOUTUBE SUBSCRI 4029357733 US 12,36 12,36\n0109 12345678901234567890456 01/09/26 Spotify P4652DD2C5 Stockholm SE 6.750,00 7,24',rate_lookup=lambda *a:(950,False))
        self.assertEqual([x['Monto'] for x in rows],[11742,6878])
    def test_grouped_six_digit_money_is_not_reference(self):
        self.assertEqual(reconcile('04/08 00273727 Cheque de Canje CASA MATRIZ 472.000,00')[0]['Monto'],472000)
    def test_summary_not_transaction(self):
        r=reconcile('31/07 Saldo Inicial 3.836.495,00\n01/08 ENEL $10000\nTOTAL TARJETA $10000')
        self.assertEqual(len(r),1)
    def test_distinct_school_amount_rules(self):
        rules=[validate_rule(dict(match_text='COLEGIO FCO JAVIER',amount=v,category=c,kind='Fijo',owner='Compartido')) for v,c in [(500000,'CSFJ (Mensualidad)'),(120000,'CSFJ (Jornada Extendida)')]]
        self.assertNotEqual(rules[0]['id'],rules[1]['id'])
        r=reconcile('01/08 COLEGIO FCO JAVIER $500000\n02/08 COLEGIO FCO JAVIER $120000',rules=effective_rules(seed_rules(),rules))
        self.assertEqual([x['Categoría'] for x in r],[x['category'] for x in rules])
    def test_confirmed_school_and_installment_end(self):
        raw='SANTIAGO 05/08/26 0608 12345678 COLEGIO FCO.JAVIER HUEC $551.405 $551.405 01/01 $551.405\nSANTIAGO 29/06/26 0309 12345679 COLEGIO FCO.JAVIER HUEC $660.000 $741.780 02/06 $123.630'
        rows=reconcile(raw,year=2026,rules=effective_rules(seed_rules(),[]))
        values,_=summarize(rows,212600)
        self.assertEqual(values['CSFJ (Mensualidad)'],338805)
        self.assertEqual(values['CSFJ (Jornada Extendida)'],123630)
        self.assertEqual(reconcile(raw,year=2027)[1]['Tipo'],'Revisar')
        self.assertEqual(apply_rules(rows,effective_rules(seed_rules(),[]),period='2027-01')[1]['Tipo'],'Revisar')
    def test_variables_keep_saved_classification(self):
        r=reconcile('01/08 COMERCIO $1000')
        r[0].update(Tipo='Variable',Categoría='Aprendida',Responsable='Compartido')
        self.assertEqual(process_unmatched_to_df(r).iloc[0]['Categoría'],'Aprendida')
    def test_gmail_all_attachments_and_same_month_reception(self):
        msg=EmailMessage();msg['Date']='Mon, 31 Aug 2026 12:00:00 +0000';msg.set_content('Test')
        msg.add_attachment(b'a',maintype='application',subtype='pdf',filename='nacional.pdf')
        msg.add_attachment(b'b',maintype='application',subtype='pdf',filename='internacional.pdf')
        class Mail:
            def __init__(self,*a,**kw):pass
            def login(self,*a):pass
            def list(self):return 'OK',[]
            def select(self,*a,**kw):pass
            def search(self,*a):return 'OK',[b'1']
            def fetch(self,*a):return 'OK',[(b'',msg.as_bytes())]
            def logout(self):pass
        with patch.object(g,'_credentials',return_value=('dummy','dummy')),patch.object(g.imaplib,'IMAP4_SSL',Mail),patch('processor_v3.extract_text_from_pdf',return_value='01/08/2026 ENEL $10000'):
            self.assertEqual(len(g.fetch_statement_pdfs_from_gmail('Agosto',2026)),2)
