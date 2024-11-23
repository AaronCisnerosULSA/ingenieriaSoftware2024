import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestUserAPI(unittest.TestCase):

    @patch('models.add_user')
    def test_add_user(self, mock_add_user):
        # Configurar el mock para simular la respuesta de la base de datos
        mock_add_user.return_value = MagicMock(id=1, name='John Doe', telefono='123456789')
        
        with app.test_client() as client:
            response = client.post('/users/new', data={'name': 'John Doe', 'telefono': '123456789'})
        
        self.assertEqual(response.status_code, 302)
        mock_add_user.assert_called_once_with('John Doe', '123456789')

    @patch('models.get_users')
    def test_get_users(self, mock_get_users):
        mock_get_users.return_value = [MagicMock(id=1, name='John Doe', telefono='123456789')]
        
        with app.test_client() as client:
            response = client.get('/users')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('John Doe', response.data.decode())

    @patch('models.update_user')
    def test_edit_user(self, mock_update_user):
        mock_update_user.return_value = MagicMock(id=1, name='Jane Doe', telefono='987654321')
        
        with app.test_client() as client:
            response = client.post('/users/edit/1', data={'name': 'Jane Doe', 'telefono': '987654321'})
        
        self.assertEqual(response.status_code, 302)
        mock_update_user.assert_called_once_with(1, 'Jane Doe', '987654321')

    @patch('models.delete_user')
    def test_delete_user(self, mock_delete_user):
        mock_delete_user.return_value = MagicMock(id=1, name='John Doe', telefono='123456789')
        
        with app.test_client() as client:
            response = client.get('/users/delete/1')
        
        self.assertEqual(response.status_code, 302)
        mock_delete_user.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
