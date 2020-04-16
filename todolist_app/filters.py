import django_filters

from todolist_app.models import Todo, Priority


class TodoFilter(django_filters.FilterSet):
	priority = django_filters.ModelChoiceFilter(queryset=Priority.objects.all())

	class Meta:
		model = Todo
		fields = {
			'title': ['icontains'],
			'description': ['icontains'],
			'priority': [],
		}