import unittest
from unittest.mock import patch, MagicMock
from models import db, User, add_user, get_user, get_users, update_user, delete_user

class TestModels(unittest.TestCase):

    @patch('models.db.session')
    @patch('models.User')
    def test_add_user(self, mock_user_class, mock_session):
        # Configurar el comportamiento del mock de User
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.name = 'John Doe'
        mock_user.telefono = '123456789'
        mock_user_class.return_value = mock_user

        # Llamada a la función add_user
        user = add_user(name='John Doe', telefono='123456789')

        # Verificar que las funciones commit y add fueron llamadas correctamente
        mock_session.add.assert_called_once_with(mock_user)
        mock_session.commit.assert_called_once()

        # Asegurarse de que el nombre del usuario es 'John Doe'
        self.assertEqual(user.name, 'John Doe')


    @patch('models.db.session')
    @patch('models.User')
    def test_get_user(self, mock_user_class, mock_session):
        # Configuración del mock para devolver un usuario con atributos reales
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.name = 'John Doe'
        mock_user.telefono = '123456789'
        
        # Configurar el query para que devuelva el usuario simulado
        mock_user_class.query.get.return_value = mock_user

        # Llamada a la función get_user
        user = get_user(1)

        # Asegurarse de que se haya obtenido el usuario correctamente
        self.assertEqual(user.name, 'John Doe')
        self.assertEqual(user.telefono, '123456789')


    @patch('models.db.session')
    @patch('models.User')
    def test_get_users(self, mock_user_class, mock_session):
        # Configuración del mock para devolver una lista de usuarios
        mock_user1 = MagicMock(id=1, name='John Doe', telefono='123456789')
        mock_user2 = MagicMock(id=2, name='Jane Doe', telefono='987654321')
        mock_user_class.query.all.return_value = [mock_user1, mock_user2]

        # Llamada a la función get_users
        users = get_users()

        # Verificar que se devolvieron dos usuarios
        self.assertEqual(len(users), 2)
        mock_user_class.query.all.assert_called_once()

    @patch('models.db.session')
    @patch('models.User')
    def test_update_user(self, mock_user_class, mock_session):
        # Configuración de un usuario mock
        mock_user = MagicMock(id=1, name='John Doe', telefono='123456789')
        mock_user_class.query.get.return_value = mock_user

        # Llamada a la función update_user
        updated_user = update_user(1, 'Jane Doe', '987654321')

        # Asegurarse de que el nombre y teléfono del usuario se actualicen correctamente
        self.assertEqual(updated_user.name, 'Jane Doe')
        self.assertEqual(updated_user.telefono, '987654321')

        # Verificar que el commit haya sido llamado
        mock_session.commit.assert_called_once()

    @patch('models.db.session')
    @patch('models.User')
    def test_delete_user(self, mock_user_class, mock_session):
        # Crear un usuario mock con atributos reales
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.name = 'John Doe'
        mock_user.telefono = '123456789'
        
        # Configurar el query para que devuelva el usuario simulado
        mock_user_class.query.get.return_value = mock_user

        # Llamada a la función delete_user
        deleted_user = delete_user(1)

        # Verificar que las funciones session.delete y session.commit se llamaron
        mock_session.delete.assert_called_once_with(mock_user)
        mock_session.commit.assert_called_once()

        # Asegurarse de que el usuario eliminado tiene los atributos esperados
        self.assertEqual(deleted_user.name, 'John Doe')
        self.assertEqual(deleted_user.telefono, '123456789')


    @patch('models.db.session')
    @patch('models.User')
    def test_delete_user_not_found(self, mock_user_class, mock_session):
        # Configuración para que el usuario no sea encontrado
        mock_user_class.query.get.return_value = None

        # Llamada a la función delete_user
        deleted_user = delete_user(999)  # ID no existente

        # Verificar que se retorne None cuando no se encuentre el usuario
        self.assertIsNone(deleted_user)
        mock_session.commit.assert_not_called()
        mock_session.delete.assert_not_called()


if __name__ == '__main__':
    unittest.main()
