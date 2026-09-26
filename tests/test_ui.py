import unittest
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import utils,database

class UITests(unittest.TestCase):
    def test_import_navigation_and_training(self):
        with patch.object(utils,'fetch_indicators',return_value=(37900,950)),patch.object(database,'save_rulebook',return_value=1),patch.object(database,'get_db',return_value=object()):
            app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=20)
            app.secrets['gcp_service_account']={}
            app.session_state.saved_rules=[];app.session_state.rule_revision=0
            app.run();self.assertFalse(app.exception)
            next(b for b in app.button if b.label=='✓').click().run()
            app.text_area[0].input('28/08 12345678 Cargo por transferencia a ANDY 27.000,00 1.022.689,00\nB.Estado, el 28/08/2026 a las 07:12\n29/08 COMERCIO NUEVO $15000')
            next(b for b in app.button if b.label=='Procesar Cartola Bancaria').click().run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state.resultados_fijos['PISCINA (Andy)'],27000)
            for page in ['Gastos Variables','Entrenar gastos','Gastos Fijos']:
                app.radio[0].set_value(page).run();self.assertFalse(app.exception,page)
            self.assertEqual(app.session_state.resultados_fijos['PISCINA (Andy)'],27000)
            app.radio[0].set_value('Entrenar gastos').run()
            next(x for x in app.text_input if x.label=='Comercio o destinatario que se repite').set_value('COMERCIO NUEVO')
            next(x for x in app.text_input if x.label=='Concepto o categoría').set_value('Nuevo fijo')
            next(b for b in app.button if b.label=='Guardar regla y aplicar').click().run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state.resultados_fijos['Nuevo fijo'],15000)
            self.assertEqual(app.session_state.saved_rules[0]['match_text'],'COMERCIO NUEVO')

class PersistenceTests(unittest.TestCase):
    def test_save_rule_and_reload_and_conflict(self):
        from rules import validate_rule
        class Snap:
            def __init__(self,data):self.data=data;self.exists=bool(data)
            def to_dict(self):return self.data.copy()
        class DB:
            def __init__(self):self.data={}
            def collection(self,*a):return self
            def document(self,*a):return self
            def get(self,**kw):return Snap(self.data)
            def transaction(self):return self
            def set(self,ref,data):self.data=data
        db=DB();rule=validate_rule(dict(match_text='COMERCIO NUEVO',kind='Fijo',category='Nuevo fijo',owner='Compartido'))
        with patch.object(database.firestore,'transactional',side_effect=lambda f:f):
            self.assertEqual(database.save_rulebook(db,[rule],0),1)
            self.assertEqual(database.load_rulebook(db)[0],[rule])
            with self.assertRaises(ValueError):database.save_rulebook(db,[rule],0)
