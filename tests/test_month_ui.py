import unittest
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from processor_v3 import reconcile
import database


class MonthUITests(unittest.TestCase):
    def app(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=20)
        app.secrets['gcp_service_account'] = {}
        app.session_state.saved_rules = []
        app.session_state.rule_revision = 0
        app.session_state.current_month_str = 'Septiembre 2026'
        app.session_state.records = reconcile('19/09/2026 COMERCIO NUEVO $16000')
        app.run()
        app.radio[1].set_value('Movimientos').run()
        self.assertFalse(app.exception)
        return app

    def test_edit_does_not_learn_and_can_undo(self):
        app = self.app()
        next(x for x in app.text_input if x.label == 'Añadir nota a la descripción').set_value('Cabritas')
        next(x for x in app.text_input if x.label == 'Categoría').set_value('Gustitos')
        next(x for x in app.selectbox if x.label == 'Tipo de movimiento').set_value('Variable')
        next(x for x in app.selectbox if x.label == 'Responsable').set_value('Compartido')
        next(x for x in app.button if x.label == 'Aplicar solo a este movimiento').click().run()
        self.assertFalse(app.exception)
        self.assertTrue(app.session_state.records[0]['Descripción'].endswith(' — Cabritas'))
        self.assertEqual(app.session_state.saved_rules, [])
        self.assertTrue(app.session_state.month_dirty)
        app.radio[0].set_value('Reglas').run()
        app.radio[0].set_value('Mes actual').run()
        self.assertEqual(app.session_state.current_month_str, 'Septiembre 2026')
        app.radio[1].set_value('Movimientos').run()
        next(x for x in app.button if x.label == 'Deshacer última corrección').click().run()
        self.assertNotIn('Cabritas', app.session_state.records[0]['Descripción'])

    def test_save_failure_preserves_draft_and_success_clears_dirty(self):
        app = self.app()
        app.session_state.month_dirty = True
        with patch.object(database, 'get_db', return_value=object()), patch.object(database, 'save_reconciliation', side_effect=RuntimeError('offline')):
            next(x for x in app.button if x.label == 'Guardar cambios del mes').click().run()
        self.assertTrue(app.session_state.month_dirty)
        self.assertEqual(len(app.session_state.records), 1)
        with patch.object(database, 'get_db', return_value=object()), patch.object(database, 'save_reconciliation', return_value=True):
            next(x for x in app.button if x.label == 'Guardar cambios del mes').click().run()
        self.assertFalse(app.session_state.month_dirty)
        self.assertFalse(app.exception)
