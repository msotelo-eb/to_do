from django.urls import path, include

from todolist_app.views import TodoListView, TodoCreateView, TodoUpdateView, TodoDeleteView, TodoReassignView, \
	TodoDetailView
from django.contrib.auth import views as auth_views

urlpatterns =[
	path('', TodoListView.as_view(), name='todo_list'),
	path('new/', TodoCreateView.as_view(), name='todo_create'),
	path('edit/<pk>', TodoUpdateView.as_view(), name='todo_update'),
	path('detail/<pk>', TodoDetailView.as_view(), name='todo_detail'),
	path('reassign/<pk>', TodoReassignView.as_view(), name='todo_reassign'),
	path('delete/<pk>', TodoDeleteView.as_view(), name='todo_delete'),
	path('accounts/', include('django.contrib.auth.urls')),
	#path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]