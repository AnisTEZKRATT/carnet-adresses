import unittest

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from view import CarnetAdressesView

class TestViewSimple(unittest.TestCase):
    
    def test_basique_view(self):
        view = CarnetAdressesView()
        
        view.set_inputs({
            "nom": "John",
            "prenom": "Doe"
        })
        
        data = view.get_inputs()
        self.assertEqual(data["nom"], "John")
        self.assertEqual(data["prenom"], "Doe")
        
        view.effacer_inputs()
        data = view.get_inputs()
        self.assertEqual(data["nom"], "")
        
        view.root.destroy()

if __name__ == '__main__':
    unittest.main()