from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path('mine/', views.CourseManageListView.as_view(), name='manage_course'),
	path('create/', views.CourseCreateView.as_view(), name='create_course'),
    path('<pk>/edit/', views.CourseUpdateView.as_view(), name='update_course'),
    path('<pk>/delete/', views.CourseDeleteView.as_view(), name='delete_course'),
    path('<pk>/modules/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
    path('module/order/', views.ModuleOrderView.as_view(), name='module_order'),
    path('content/order/', views.ContentOrderView.as_view(), name='content_order'),
    path('module/<int:module_id>/content/<model_name>/create/', views.ModuleContentUpdateView.as_view(), name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/', views.ModuleContentUpdateView.as_view(), name='module_content_update'),
    path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),
    path('module/<int:module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),
    path('subject/<slug:subject_slug>/', views.CourseListView.as_view(), name="course_list_subject"),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
]
