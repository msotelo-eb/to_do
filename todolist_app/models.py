from django.conf import settings
from django.db import models


class Priority(models.Model):

	name = models.CharField(max_length=20)
	order = models.IntegerField()

	def __str__(self):
		return 'id {}: {} (order {})'.format(
			self.id,
			self.name,
			self.order,
		)


class Todo(models.Model):

	title = models.CharField(max_length=20)
	description = models.CharField(max_length=50)
	assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned')
	done = models.BooleanField(default=False)
	created = models.DateField(auto_now_add=True)
	updated = models.DateField(auto_now=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created')
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated')
	priority = models.ForeignKey(Priority, on_delete=models.CASCADE)


