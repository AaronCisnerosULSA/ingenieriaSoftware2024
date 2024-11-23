import unittest
from unittest.mock import patch, MagicMock
from models import get_users, get_user, add_user, delete_user, update_user

class TestModels(unittest.TestCase):

    @patch('models.User.query')
    def test_get_users(self, mock_query):
        mock_query.all.return_value = [
            MagicMock(id=1, name='John Doe', telefono='123456789'),
            MagicMock(id=2, name='Jane Doe', telefono='987654321')
        ]
        users = get_users()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].name, 'John Doe')
        self.assertEqual(users[1].telefono, '987654321')

    @patch('models.User.query')
    def test_get_user(self, mock_query):
        mock_user = MagicMock(id=1, name='John Doe', telefono='123456789')
        mock_query.get.return_value = mock_user
        user = get_user(1)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'John Doe')

    @patch('models.db.session')
    @patch('models.User')
    def test_add_user(self, mock_user_class, mock_session):
        mock_user = MagicMock(id=1, name='John Doe', telefono='123456789')
        mock_user_class.return_value = mock_user
        user = add_user(name='John Doe', telefono='123456789')
        mock_session.add.assert_called_once_with(mock_user)
        mock_session.commit.assert_called_once()
        self.assertEqual(user.name, 'John Doe')

    @patch('models.db.session')
    @patch('models.User.query')
    def test_delete_user(self, mock_query, mock_session):
        mock_user = MagicMock(id=1, name='John Doe', telefono='123456789')
        mock_query.get.return_value = mock_user
        user = delete_user(1)
        mock_session.delete.assert_called_once_with(mock_user)
        mock_session.commit.assert_called_once()
        self.assertEqual(user.name, 'John Doe')

    @patch('models.db.session')
    @patch('models.User.query')
    def test_update_user(self, mock_query, mock_session):
        mock_user = MagicMock(id=1, name='John Doe', telefono='123456789')
        mock_query.get.return_value = mock_user
        user = update_user(1, name='Jane Doe', telefono='987654321')
        self.assertEqual(user.name, 'Jane Doe')
        self.assertEqual(user.telefono, '987654321')
        mock_session.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
