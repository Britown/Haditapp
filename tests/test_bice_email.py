import unittest
from bice_email import parse_transfer_email,enrich_transfers

class BiceTests(unittest.TestCase):
    def email(self,**kw):
        item=parse_transfer_email('Fecha 04/08/2026 Monto $54.000 Nombre Jossefa Herbas Lopez RUT 20.111.111-1 Banco Mercado Pago Mensaje Clases de agosto Operación Número 12345678','Transferencia realizada')
        item.update(kw);return item
    def row(self,**kw):
        row={'Fecha':'05/08/2026','Monto':54000,'Descripción':'Transferencia a Jossefa Herbas el 2026-08-04 a las 18:26 hrs.', '_Original':'05/08 Transferencia de REMITENTE desde Banco BICE a Jossefa Herbas Lopez Rut 20.111.111-1 a Cuenta Vista, el 2026-08-04 a las 18:26 hrs.','Categoría':'Por Revisar'}
        row.update(kw);return row
    def test_correct_identity_and_actual_date(self):
        original=self.row();result=enrich_transfers([original],[self.email()])[0]
        self.assertTrue(result['Descripción'].endswith('Mensaje BICE: Clases de agosto'))
        for key in ['Monto','_Original','Categoría']:self.assertEqual(result[key],original[key])
        self.assertEqual(enrich_transfers([result],[self.email()])[0],result)
    def test_same_amount_is_not_enough(self):
        for changes in [dict(name='OTRA PERSONA',rut='11 111 111 1'),dict(date='2026-08-05'),dict(amount=1000)]:
            row=self.row();self.assertEqual(enrich_transfers([row],[self.email(**changes)]),[row])
    def test_ambiguous_emails_or_rows_are_not_attached(self):
        row=self.row();item=self.email()
        self.assertEqual(enrich_transfers([row],[item,item]),[row])
        self.assertEqual(enrich_transfers([row,row],[item]),[row,row])
    def test_operation_identifier_and_subject_fallback(self):
        row=self.row(_Original='05/08 12345678 Cargo por transferencia a Rut 20.111.111-1, el 04/08/2026 a las 18:26')
        self.assertTrue(enrich_transfers([row],[self.email(message='',name='',rut='')])[0]['Descripción'].endswith('Transferencia realizada'))
    def test_date_required_and_spanish_date(self):
        self.assertIsNone(parse_transfer_email('Monto $1000 Nombre Persona RUT 11.111.111-1'))
        self.assertEqual(parse_transfer_email('Fecha 4 ago 2026 Monto $1.000 Nombre Persona RUT 11.111.111-1')['date'],'2026-08-04')
    def test_gmail_readonly_html_and_duplicate_message(self):
        from email.message import EmailMessage
        from unittest.mock import patch
        import gmail_fetcher as g
        msg=EmailMessage();msg['Subject']='Transferencia BICE';msg['Message-ID']='<test-bice>'
        msg.set_content('<p>Fecha 04/08/2026 Monto $54.000 Nombre Jossefa Herbas Lopez RUT 20.111.111-1 Banco BICE Mensaje Clases Operación Número 12345678</p>',subtype='html')
        calls=[]
        class Mail:
            def __init__(self,*a,**kw):pass
            def login(self,*a):pass
            def list(self):return 'OK',[]
            def select(self,*a,**kw):calls.append(kw)
            def search(self,*a):return 'OK',[b'1 2']
            def fetch(self,eid,mode):calls.append(mode);return 'OK',[(b'',msg.as_bytes())]
            def logout(self):pass
        with patch.object(g,'_credentials',return_value=('dummy','dummy')),patch.object(g.imaplib,'IMAP4_SSL',Mail):
            results=g.fetch_bice_transfers_from_gmail('Agosto 2026')
        self.assertEqual(len(results),1)
        self.assertEqual(results[0]['amount'],54000)
        self.assertIn({'readonly':True},calls)
        self.assertIn('(BODY.PEEK[])',calls)
