from django.contrib import admin
from django.urls import path, re_path
from accounts import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    re_path(r'^login$', views.login, name = 'login'),
    re_path(r'^logout$', views.logout, name = 'logout'),
    re_path(r'^send_login_email$', views.send_login_email, name = 'send_login_email')
]
