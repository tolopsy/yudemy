from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from courses.views import CourseListView

LOGIN_REDIRECT_URL = reverse_lazy('student_course_list')

urlpatterns = [
	path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
	path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('course/', include('courses.urls')),
    path('', CourseListView.as_view(), name='course_list'),
    path('student/', include('students.urls')),
    path('api/', include('courses.api.urls', namespace="api")),
    path('chat/', include('chat.urls', namespace='chat'))
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)