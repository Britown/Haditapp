import unittest
from processor_v3 import reconcile, summarize
from workflow import effective_rules, learn_variable_corrections
from rules import seed_rules
from variables_processor import process_unmatched_to_df


class FixedRoutingTests(unittest.TestCase):
    def test_saved_variable_gardener_goes_to_fixed(self):
        saved = [dict(match_text='LUIS MIGUEL CRUCES', category='JARDINERO',
                      kind='Variable', owner='Compartido', priority=100)]
        rows = reconcile('25/09/2026 Transferencia a Luis Miguel Cruces $18.000',
                         rules=effective_rules(seed_rules(), saved))
        self.assertEqual(rows[0]['Tipo'], 'Fijo')
        self.assertEqual(summarize(rows)[0]['JARDINERO'], 18000)
        self.assertTrue(process_unmatched_to_df(rows).empty)

    def test_learning_fixed_category_preserves_type(self):
        before = dict(Fecha='25/09/2026', Descripción='Transferencia a Luis Miguel Cruces',
                      Categoría='Por Revisar', Responsable='Personal', Monto=18000)
        after = dict(before, Categoría='JARDINERO', Responsable='Compartido')
        learned, count, _ = learn_variable_corrections([before], [after], [])
        self.assertEqual(count, 1)
        self.assertEqual(learned[0]['kind'], 'Fijo')
