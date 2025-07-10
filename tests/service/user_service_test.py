import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from fastapi import HTTPException

from service.user_service import UserService


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()

    def test_login_success(self):
        username = "test_user"
        password = "test_password"
        self.user_service.users_db = {username: password}
        expected_token = "test_token"
        with patch.object(self.user_service, 'create_token', return_value=expected_token):
            response = self.user_service.login(username, password)
            self.assertEqual(response['message'], "Login successful")
            self.assertEqual(response['token'], expected_token)

    def test_login_invalid_credentials(self):
        with self.assertRaises(HTTPException) as context:
            self.user_service.login("invalid_user", "invalid_password")
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid username or password")

    def test_register_success(self):
        username = "new_user"
        password = "new_password"
        response = self.user_service.register(username, password)
        self.assertEqual(response['message'], "Registration successful")
        self.assertEqual(self.user_service.users_db[username], password)

    def test_register_existing_user(self):
        username = "existing_user"
        password = "existing_password"
        self.user_service.users_db = {username: password}
        with self.assertRaises(HTTPException) as context:
            self.user_service.register(username, "new_password")
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Username already exists")

    def test_logout_success(self):
        token = "test_token"
        self.user_service.sessions[token] = datetime.utcnow()
        response = self.user_service.logout(token)
        self.assertEqual(response['message'], "Logout successful")
        self.assertNotIn(token, self.user_service.sessions)

    def test_get_user_details_success(self):
        username = "test_user"
        password = "test_password"
        self.user_service.users_db = {username: password}
        response = self.user_service.get_user_details(username)
        self.assertEqual(response['username'], username)
        self.assertEqual(response['password'], password)

    def test_get_user_details_not_found(self):
        with self.assertRaises(HTTPException) as context:
            self.user_service.get_user_details("non_existing_user")
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "User not found")

    def test_set_user_details_success(self):
        username = "test_user"
        password = "test_password"
        new_password = "new_password"
        self.user_service.users_db = {username: password}
        response = self.user_service.set_user_details(username, new_password)
        self.assertEqual(response['message'], "User details updated")
        self.assertEqual(self.user_service.users_db[username], new_password)

    def test_create_token(self):
        username = "test_user"
        expected_token = "test_token"
        with patch('jwt.encode', return_value=expected_token):
            token = self.user_service.create_token(username)
            self.assertEqual(token, expected_token)

    def test_verify_token_expired(self):
        token = "expired_token"
        self.user_service.sessions = {token: datetime.utcnow() - timedelta(minutes=20)}
        with self.assertRaises(HTTPException) as context:
            self.user_service.verify_token(token)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Token has expired")

    def test_verify_token_invalid(self):
        token = "invalid_token"
        with self.assertRaises(HTTPException) as context:
            self.user_service.verify_token(token)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid token")

    def test_decodeJWT(self):
        token = "test_token"
        expected_payload = {"sub": "test_user", "exp": datetime.utcnow() + timedelta(minutes=15)}
        with patch('jwt.decode', return_value=expected_payload):
            payload = self.user_service.decodeJWT(token)
            self.assertEqual(payload, expected_payload)


if __name__ == '__main__':
    unittest.main()
