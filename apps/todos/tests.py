from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo


class TodoModelTests(TestCase):
    def test_create_todo(self) -> None:
        todo = Todo.objects.create(title="Test task", description="desc")
        self.assertIsInstance(todo, Todo)
        self.assertEqual(str(todo), "Test task")


class TodoViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.todo = Todo.objects.create(title="List task", description="list")

    def test_list_view_status_code(self) -> None:
        url = reverse('todos:todo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "List task")

    def test_create_view_post(self) -> None:
        url = reverse('todos:todo_create')
        data = {"title": "New Task", "description": "new"}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Todo.objects.filter(title="New Task").exists())
