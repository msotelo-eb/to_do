from django.contrib.auth.models import User
from django.test import Client, TestCase

from todolist_app.models import Todo, Priority


class TodoListTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.other_user = User.objects.create(username='othertestuser')
        self.other_user.set_password('12345')
        self.other_user.save()
        self.priority = Priority.objects.create(name="High", order=1)
        self.user_todo = Todo.objects.create(
            title="Task",
            assigned_user=self.user,
            created_by=self.user,
            updated_by=self.user,
            priority=self.priority
        )
        self.other_user_todo = Todo.objects.create(
            title="Task",
            assigned_user=self.other_user,
            created_by=self.other_user,
            updated_by=self.other_user,
            priority=self.priority
        )

    def test_todo_list_user_logged(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(response.context['object_list'][0].id, self.user_todo.id)

    def test_todo_list_user_not_logged(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 302)

    def test_todo_create_successfully(self):
        self.client.login(username='testuser', password='12345')
        todo_list_length = Todo.objects.count()
        response = self.client.post(
            '/new/',
            {
                'title': 'task',
                'description': 'desc',
                'done': True,
                'priority': self.priority.id,
            },
            follow=True,
        )
        id = response.context["object"].id
        self.assertEqual(Todo.objects.count(), todo_list_length+1)
        self.assertRedirects(response, f"/detail/{id}")
        self.assertEqual(response.status_code, 200)

    def test_todo_create_failed(self):

        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            '/new/',
            {
                'title': 'task',
                'description': 'desc',
                'done': True,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Todo.objects.filter(assigned_user=self.user).count(), 1)

    def test_todo_create_user_not_logged(self):
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 302)

