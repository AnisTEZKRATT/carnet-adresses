import unittest
from unittest.mock import Mock

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller import CarnetAdressesController


class TestCarnetAdressesController(unittest.TestCase):
    
    def test_ajouter_contact(self):
        mock_model = Mock()
        mock_view = Mock()
        
        test_data = {
            "nom": "John",
            "prenom": "Doe",
            "telephone": "0123456789",
            "email": "john@test.com"
        }
        mock_view.get_inputs.return_value = test_data
        
        controller = CarnetAdressesController(mock_model, mock_view)
        controller.ajouter_contact()
        
        mock_model.ajouter_contact.assert_called_once_with(
            "John", "Doe", "0123456789", "john@test.com", ""
        )
    
    def test_recherche_contact(self):
        mock_model = Mock()
        mock_view = Mock()
        
        mock_view.get_inputs.return_value = {"nom": "Smith", "prenom": ""}
        
        controller = CarnetAdressesController(mock_model, mock_view)
        controller.rechercher_contact()
        
        mock_model.rechercher_contact.assert_called_once()
    
    def test_email_validation(self):
        mock_model = Mock()
        mock_view = Mock()
        controller = CarnetAdressesController(mock_model, mock_view)
        
        self.assertTrue(controller._email_valide("test@example.com"))
        self.assertFalse(controller._email_valide("invalid-email"))

if __name__ == '__main__':
    unittest.main()