from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from todolist_app.models import Todo
from .filters import TodoFilter


def logout_view(request):
	logout(request)


class TodoListView(LoginRequiredMixin, ListView):

	login_url = 'login'

	def get_queryset(self):
		return Todo.objects.filter(assigned_user=self.request.user)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filter'] = TodoFilter(self.request.GET, queryset=self.get_queryset())
		return context



class TodoCreateView(LoginRequiredMixin, CreateView):

	login_url = 'login'
	redirect_field_name = '/'
	model = Todo
	fields = [
		'title',
		'description',
		'done',
		'priority',
	]

	def get_success_url(self):
		return reverse('todo_detail', args=(self.object.id,))

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		form.instance.updated_by = self.request.user
		form.instance.assigned_user = self.request.user
		return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UpdateView):

	login_url = 'login'
	redirect_field_name = '/'
	model = Todo
	fields = [
		'title',
		'description',
		'assigned_user',
		'done',
		'created_by',
		'updated_by',
		'priority',
	]
	template_name_suffix = '_update_form'

	def get_object(self, queryset=None):
		todo = super().get_object()
		if todo.assigned_user != self.request.user:
			raise PermissionDenied
		return todo
	'''
	def get_queryset(self):
		return Todo.objects.filter(assigned_user=self.request.user)
	'''
	def get_success_url(self):
		return reverse('todo_list', args=(self.object.id,))


class TodoReassignView(LoginRequiredMixin, UpdateView):

	login_url = 'login'
	redirect_field_name = '/'
	model = Todo
	fields = [
		'assigned_user',
	]
	template_name_suffix = '_reassign_form'

	def get_object(self, queryset=None):
		todo = super().get_object()
		if todo.assigned_user != self.request.user:
			raise PermissionDenied
		return todo

	def get_success_url(self):
		return reverse('todo_list', args=(self.object.id,))


class TodoDetailView(LoginRequiredMixin, DetailView):

	login_url = 'login'
	redirect_field_name = '/'
	model = Todo
	success_url = reverse_lazy('todo_list')


class TodoDeleteView(LoginRequiredMixin, DeleteView):

	login_url = 'login'
	redirect_field_name = '/'
	model = Todo
	success_url = reverse_lazy('todo_list')

	def get_object(self, queryset=None):
		todo = super().get_object()
		if todo.assigned_user != self.request.user:
			raise PermissionDenied
		return todo
