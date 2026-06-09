from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import ToDo


class ToDoAPITests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username="tester", password="pass123")

    def test_list_requires_authentication(self) -> None:
        resp = self.client.get("/api/todos/")
        self.assertEqual(resp.status_code, 401)

    def test_create_and_list_authenticated(self) -> None:
        self.client.force_authenticate(user=self.user)
        resp = self.client.post("/api/todos/", {"title": "Buy milk", "description": "2 liters"}, format="json")
        self.assertEqual(resp.status_code, 201)
        # now list
        resp2 = self.client.get("/api/todos/")
        self.assertEqual(resp2.status_code, 200)
        data = resp2.json()
        self.assertTrue(any(item.get("title") == "Buy milk" for item in data))
